"""Tests of the Helius WebSocket client, against a local server that plays Helius."""

import asyncio
import json
from typing import Any, AsyncIterator

import pytest
import pytest_asyncio
from aiohttp import WSMsgType, web

from cyhole.helius import Helius
from cyhole.helius.exception import HeliusRPCError, HeliusWebSocketClosed, HeliusWebSocketError
from cyhole.helius.param import HeliusNetwork, HeliusWebSocketCommitment
from cyhole.helius.schema import HeliusWebSocketNotification, HeliusWebSocketReconnected, LogsNotification
from cyhole.helius.websocket import HeliusWebSocket

API_KEY = "SECRET-KEY-123"


class FakeHelius:
    """A WebSocket server answering the standard subscriptions as Helius does."""

    def __init__(self) -> None:
        self.received: list[dict[str, Any]] = []
        self.api_keys: list[str | None] = []
        self.sockets: list[web.WebSocketResponse] = []
        self.next_subscription = 100
        self.pings = 0
        self.silent = False                        # never answer a request
        self.refuse: set[str] = set()              # methods answered with an error
        self.reject_handshakes = 0                 # next connections refused with HTTP 503
        self.notify_on_subscribe: str | None = None  # push one at once after the answer

    async def handler(self, request: web.Request) -> web.StreamResponse:
        self.api_keys.append(request.query.get("api-key"))
        if self.reject_handshakes > 0:
            self.reject_handshakes -= 1
            return web.Response(status = 503)
        ws = web.WebSocketResponse(autoping = False)
        await ws.prepare(request)
        self.sockets.append(ws)
        async for message in ws:
            if message.type == WSMsgType.PING:
                self.pings += 1
                await ws.pong(message.data)
            elif message.type == WSMsgType.TEXT:
                await self._answer(ws, json.loads(message.data))
        return ws

    async def _answer(self, ws: web.WebSocketResponse, request: dict[str, Any]) -> None:
        self.received.append(request)
        if self.silent:
            return
        method = request["method"]
        if method in self.refuse:
            await ws.send_str(json.dumps({
                "jsonrpc": "2.0", "id": request["id"],
                "error": {"code": -32602, "message": "Invalid param: not a public key"},
            }))
        elif method.endswith("Unsubscribe"):
            await ws.send_str(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": True}))
        else:
            self.next_subscription += 1
            await ws.send_str(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": self.next_subscription}))
            if self.notify_on_subscribe is not None:
                await ws.send_str(json.dumps(logs_notification(self.next_subscription, self.notify_on_subscribe)))

    async def push(self, payload: dict[str, Any]) -> None:
        await self.sockets[-1].send_str(json.dumps(payload))

    async def drop(self) -> None:
        await self.sockets[-1].close()

    def subscribes(self) -> list[dict[str, Any]]:
        return [r for r in self.received if r["method"] == "logsSubscribe"]


def logs_notification(subscription: int, signature: str, slot: int = 7) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "method": "logsNotification",
        "params": {
            "result": {
                "context": {"slot": slot},
                "value": {"signature": signature, "err": None, "logs": ["Program log: Instruction: Transfer"]},
            },
            "subscription": subscription,
        },
    }


@pytest_asyncio.fixture
async def helius() -> AsyncIterator[tuple[FakeHelius, str]]:
    fake = FakeHelius()
    app = web.Application()
    app.router.add_get("/", fake.handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = runner.addresses[0][1]
    yield fake, f"ws://127.0.0.1:{port}/?api-key={API_KEY}"
    await runner.cleanup()


async def next_message(ws: HeliusWebSocket, timeout: float = 2.0) -> Any:
    return await asyncio.wait_for(ws.__anext__(), timeout)


async def wait_until(condition: Any, timeout: float = 2.0) -> None:
    async def poll() -> None:
        while not condition():
            await asyncio.sleep(0.01)
    await asyncio.wait_for(poll(), timeout)


class TestHeliusWebSocketInteraction:

    def test_the_url_is_built_for_the_network(self) -> None:
        helius = Helius(api_key = API_KEY, network = HeliusNetwork.DEVNET)
        assert helius.url_websocket == f"wss://devnet.helius-rpc.com/?api-key={API_KEY}"

    def test_websocket_builds_a_client_not_yet_connected(self) -> None:
        ws = Helius(api_key = API_KEY).websocket(reconnect = True)
        assert isinstance(ws, HeliusWebSocket)
        assert not ws.connected
        assert API_KEY not in repr(ws)


class TestHeliusWebSocketSubscriptions:

    @pytest.mark.asyncio
    async def test_logs_subscribe_sends_the_documented_request(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url) as ws:
            subscription = await ws.logs_subscribe("Wallet111", commitment = HeliusWebSocketCommitment.PROCESSED)
        assert subscription == 1
        assert fake.subscribes()[0]["params"] == [{"mentions": ["Wallet111"]}, {"commitment": "processed"}]
        assert fake.subscribes()[0]["jsonrpc"] == "2.0"

    @pytest.mark.asyncio
    async def test_a_notification_is_yielded_typed_under_the_clients_id(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url) as ws:
            first = await ws.logs_subscribe("Wallet111")
            second = await ws.logs_subscribe("Wallet222")
            await fake.push(logs_notification(102, "Sig2", slot = 42))
            message = await next_message(ws)
        assert (first, second) == (1, 2)
        assert message == LogsNotification(
            subscription = 2, slot = 42, signature = "Sig2", err = None,
            logs = ["Program log: Instruction: Transfer"],
        )

    @pytest.mark.asyncio
    async def test_a_notification_right_after_the_answer_is_not_lost(self, helius) -> None:
        fake, url = helius
        fake.notify_on_subscribe = "SigAtOnce"
        async with HeliusWebSocket(url) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            message = await next_message(ws)
        assert isinstance(message, LogsNotification)
        assert (message.subscription, message.signature) == (subscription, "SigAtOnce")

    @pytest.mark.asyncio
    async def test_unsubscribe_ends_the_subscription(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            kept = await ws.logs_subscribe("Wallet222")
            assert await ws.logs_unsubscribe(subscription) is True
            assert await ws.logs_unsubscribe(subscription) is False
            await fake.push(logs_notification(101, "Dropped"))
            await fake.push(logs_notification(102, "Kept"))
            message = await next_message(ws)
            assert ws.subscriptions == [kept]
        assert fake.received[-1]["method"] == "logsUnsubscribe"
        assert fake.received[-1]["params"] == [101]
        assert message.signature == "Kept"

    @pytest.mark.asyncio
    async def test_an_unknown_notification_is_yielded_as_it_came(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            await fake.push({"jsonrpc": "2.0", "method": "slotNotification",
                             "params": {"result": {"slot": 9}, "subscription": 101}})
            message = await next_message(ws)
        assert message == HeliusWebSocketNotification(
            method = "slotNotification", subscription = subscription, result = {"slot": 9}
        )

    @pytest.mark.asyncio
    async def test_a_refused_subscription_raises_the_rpc_error(self, helius) -> None:
        fake, url = helius
        fake.refuse.add("logsSubscribe")
        async with HeliusWebSocket(url) as ws:
            with pytest.raises(HeliusRPCError) as error:
                await ws.logs_subscribe("not-an-address")
            assert ws.subscriptions == []
        assert error.value.code == -32602

    @pytest.mark.asyncio
    async def test_no_answer_raises_after_the_request_timeout(self, helius) -> None:
        fake, url = helius
        fake.silent = True
        async with HeliusWebSocket(url, request_timeout = 0.1) as ws:
            with pytest.raises(HeliusWebSocketError) as error:
                await ws.logs_subscribe("Wallet111")
        assert not isinstance(error.value, HeliusWebSocketClosed)


class TestHeliusWebSocketConnection:

    @pytest.mark.asyncio
    async def test_pings_are_sent_every_heartbeat(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, heartbeat = 0.05):
            await wait_until(lambda: fake.pings >= 2)

    @pytest.mark.asyncio
    async def test_closing_ends_the_iteration(self, helius) -> None:
        _, url = helius
        ws = HeliusWebSocket(url)
        await ws.connect()

        async def read_all() -> list[Any]:
            return [message async for message in ws]

        reader = asyncio.create_task(read_all())
        await asyncio.sleep(0.05)
        await ws.close()
        assert await asyncio.wait_for(reader, 2.0) == []
        with pytest.raises(HeliusWebSocketClosed):
            await ws.logs_subscribe("Wallet111")

    @pytest.mark.asyncio
    async def test_without_reconnect_a_drop_ends_the_iteration_with_an_error(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url) as ws:
            await ws.logs_subscribe("Wallet111")
            await fake.drop()
            with pytest.raises(HeliusWebSocketClosed):
                await next_message(ws)
            with pytest.raises(StopAsyncIteration):
                await next_message(ws)
            with pytest.raises(HeliusWebSocketClosed):
                await ws.logs_subscribe("Wallet222")

    @pytest.mark.asyncio
    async def test_a_drop_fails_a_pending_request_at_once(self, helius) -> None:
        fake, url = helius
        fake.silent = True
        async with HeliusWebSocket(url, request_timeout = 5.0) as ws:
            pending = asyncio.create_task(ws.logs_subscribe("Wallet111"))
            await wait_until(lambda: len(fake.received) == 1)
            await fake.drop()
            with pytest.raises(HeliusWebSocketClosed):
                await asyncio.wait_for(pending, 1.0)


class TestHeliusWebSocketReconnection:

    @pytest.mark.asyncio
    async def test_a_drop_reconnects_resubscribes_and_says_so(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            await fake.drop()
            marker = await next_message(ws)
            await fake.push(logs_notification(102, "AfterReconnect"))
            message = await next_message(ws)
        assert isinstance(marker, HeliusWebSocketReconnected)
        assert marker.attempts == 1
        assert marker.subscriptions == [subscription]
        assert marker.downtime_s >= 0
        assert [r["params"] for r in fake.subscribes()] == [
            [{"mentions": ["Wallet111"]}, {"commitment": "confirmed"}],
        ] * 2
        # The node gave a new id; the caller still sees its own.
        assert (message.subscription, message.signature) == (subscription, "AfterReconnect")

    @pytest.mark.asyncio
    async def test_reconnection_retries_until_the_node_takes_it(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            await ws.logs_subscribe("Wallet111")
            fake.reject_handshakes = 2
            await fake.drop()
            marker = await next_message(ws)
        assert marker.attempts == 3
        assert fake.api_keys == [API_KEY] * 4

    @pytest.mark.asyncio
    async def test_a_subscription_refused_on_reconnection_is_dropped(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            await ws.logs_subscribe("Wallet111")
            fake.refuse.add("logsSubscribe")
            await fake.drop()
            marker = await next_message(ws)
            assert ws.subscriptions == []
        assert marker.subscriptions == []

    @pytest.mark.asyncio
    async def test_a_request_during_the_reconnection_waits_for_it(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.2) as ws:
            fake.reject_handshakes = 1
            await fake.drop()
            await wait_until(lambda: not ws.connected)
            subscription = await ws.logs_subscribe("Wallet111")
            assert ws.connected
        assert subscription == 1


class TestHeliusWebSocketSecrets:

    @pytest.mark.asyncio
    async def test_a_refused_connection_does_not_show_the_key(self) -> None:
        ws = HeliusWebSocket(f"ws://127.0.0.1:1/?api-key={API_KEY}")
        with pytest.raises(HeliusWebSocketError) as error:
            await ws.connect()
        assert API_KEY not in str(error.value)
        assert API_KEY not in repr(error.value)

    @pytest.mark.asyncio
    async def test_a_refused_handshake_does_not_show_the_key(self, helius) -> None:
        fake, url = helius
        fake.reject_handshakes = 1
        with pytest.raises(HeliusWebSocketError) as error:
            await HeliusWebSocket(url).connect()
        assert "503" in str(error.value)
        assert API_KEY not in str(error.value)

    @pytest.mark.asyncio
    async def test_failed_reconnections_do_not_log_the_key(self, helius, caplog) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            fake.reject_handshakes = 2
            await fake.drop()
            await next_message(ws)
        assert caplog.records
        assert all(API_KEY not in record.getMessage() for record in caplog.records)
