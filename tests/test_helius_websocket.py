"""Tests of the Helius WebSocket client, against a local server that plays Helius."""

import asyncio
import json
from typing import Any, AsyncIterator

import pytest
import pytest_asyncio
from aiohttp import WSMsgType, web

from cyhole.helius import Helius
from cyhole.helius import websocket as websocket_module
from cyhole.helius.exception import (
    HeliusRPCError,
    HeliusWebSocketClosed,
    HeliusWebSocketError,
    HeliusWebSocketTimeout,
)
from cyhole.helius.param import HeliusNetwork, HeliusWebSocketCommitment
from cyhole.helius.schema import (
    HeliusWebSocketDisconnected,
    HeliusWebSocketNotification,
    HeliusWebSocketReconnected,
    LogsNotification,
)
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
        self.pong = True                           # answer pings
        self.kick = False                          # accept connections, then close them at once
        # What the next subscribe requests get, one entry each: an error code,
        # "silent" (no answer), "close" (the connection closes), or a delay in seconds.
        self.script: list[int | str | float] = []
        self._tasks: set[asyncio.Task[None]] = set()

    async def handler(self, request: web.Request) -> web.StreamResponse:
        self.api_keys.append(request.query.get("api-key"))
        if self.reject_handshakes > 0:
            self.reject_handshakes -= 1
            return web.Response(status = 503)
        ws = web.WebSocketResponse(autoping = False)
        await ws.prepare(request)
        if self.kick:
            await ws.close(code = 4008, message = b"too many connections")
            return ws
        self.sockets.append(ws)
        async for message in ws:
            if message.type == WSMsgType.PING:
                self.pings += 1
                if self.pong:
                    await ws.pong(message.data)
            elif message.type == WSMsgType.TEXT:
                task = asyncio.create_task(self._answer(ws, json.loads(message.data)))
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)
        return ws

    async def _answer(self, ws: web.WebSocketResponse, request: dict[str, Any]) -> None:
        self.received.append(request)
        if self.silent:
            return
        method = request["method"]
        if method.endswith("Subscribe") and self.script:
            step = self.script.pop(0)
            if step == "silent":
                return
            if step == "close":
                await ws.close()
                return
            if isinstance(step, int):
                await ws.send_str(json.dumps({
                    "jsonrpc": "2.0", "id": request["id"], "error": {"code": step, "message": "scripted"},
                }))
                return
            assert isinstance(step, float)
            await asyncio.sleep(step)
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

    def unsubscribes(self) -> list[dict[str, Any]]:
        return [r for r in self.received if r["method"] == "logsUnsubscribe"]


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


async def next_of(ws: HeliusWebSocket, kind: type, timeout: float = 2.0) -> Any:
    """The next message of type `kind`, skipping the others."""
    async def find() -> Any:
        while True:
            message = await ws.__anext__()
            if isinstance(message, kind):
                return message
    return await asyncio.wait_for(find(), timeout)


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
            with pytest.raises(HeliusWebSocketTimeout):
                await ws.logs_subscribe("Wallet111")

    @pytest.mark.asyncio
    async def test_a_late_answer_to_a_subscribe_ends_that_subscription_on_the_node(self, helius) -> None:
        fake, url = helius
        fake.script = [0.3]
        async with HeliusWebSocket(url, request_timeout = 0.1) as ws:
            with pytest.raises(HeliusWebSocketTimeout):
                await ws.logs_subscribe("Wallet111")
            await wait_until(lambda: fake.unsubscribes())
            await fake.push(logs_notification(101, "Unwanted"))
            await fake.push({"jsonrpc": "2.0", "method": "slotNotification", "params": {"result": 1}})
            message = await next_message(ws)
            assert ws.subscriptions == []
        assert fake.unsubscribes()[0]["params"] == [101]
        assert isinstance(message, HeliusWebSocketNotification)

    @pytest.mark.asyncio
    async def test_unexpected_payloads_are_dropped_and_the_client_goes_on(self, helius) -> None:
        fake, url = helius
        fake.script = [0.0, 0.3]
        async with HeliusWebSocket(url) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            pending = asyncio.create_task(ws.logs_subscribe("Wallet222"))
            await wait_until(lambda: len(fake.received) == 2)
            for payload in (
                {"jsonrpc": "2.0", "id": [1], "result": 5},
                {"jsonrpc": "2.0", "method": "logsNotification", "params": [1, 2]},
                {"jsonrpc": "2.0", "method": "logsNotification",
                 "params": {"subscription": 101, "result": {"context": 7, "value": "x"}}},
                [1, 2, 3],
                "not json",
            ):
                await fake.sockets[-1].send_str(payload if isinstance(payload, str) else json.dumps(payload))
            assert await asyncio.wait_for(pending, 2.0) == subscription + 1
            await fake.push(logs_notification(101, "StillHere"))
            message = await next_of(ws, LogsNotification)
        assert (message.subscription, message.signature) == (subscription, "StillHere")

    @pytest.mark.asyncio
    async def test_an_error_answer_without_id_is_logged(self, helius, caplog) -> None:
        fake, url = helius
        async with HeliusWebSocket(url) as ws:
            await ws.logs_subscribe("Wallet111")
            await fake.push({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
            await wait_until(lambda: any("Parse error" in r.getMessage() for r in caplog.records))


class TestHeliusWebSocketConnection:

    @pytest.mark.asyncio
    async def test_pings_are_sent_every_heartbeat(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, heartbeat = 0.05):
            await wait_until(lambda: fake.pings >= 2)

    @pytest.mark.asyncio
    async def test_pings_are_sent_on_a_busy_connection_too(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, heartbeat = 0.1) as ws:
            await ws.logs_subscribe("Wallet111")
            for i in range(40):
                await fake.push(logs_notification(101, f"Sig{i}"))
                await asyncio.sleep(0.01)
        assert fake.pings >= 2

    @pytest.mark.asyncio
    async def test_a_missing_pong_counts_as_a_drop(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, heartbeat = 0.1, reconnect_min_delay = 0.01) as ws:
            await ws.logs_subscribe("Wallet111")
            fake.pong = False
            await next_of(ws, HeliusWebSocketDisconnected)
            fake.pong = True
            marker = await next_of(ws, HeliusWebSocketReconnected)
        assert marker.subscriptions == [1]

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
    async def test_a_closed_client_cannot_connect_again(self, helius) -> None:
        _, url = helius
        ws = HeliusWebSocket(url)
        await ws.connect()
        await ws.close()
        with pytest.raises(HeliusWebSocketClosed):
            await ws.connect()

    @pytest.mark.asyncio
    async def test_closing_fails_a_request_waiting_for_the_reconnection_at_once(self, helius) -> None:
        fake, url = helius
        ws = HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 30.0)
        await ws.connect()
        await fake.drop()
        await wait_until(lambda: not ws.connected)
        waiting = asyncio.create_task(ws.logs_subscribe("Wallet111"))
        await asyncio.sleep(0.05)
        await ws.close()
        with pytest.raises(HeliusWebSocketClosed):
            await asyncio.wait_for(waiting, 0.5)

    @pytest.mark.asyncio
    async def test_close_lets_the_callers_cancellation_through(self, helius) -> None:
        fake, url = helius
        ws = HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 30.0)
        await ws.connect()
        await fake.drop()
        await wait_until(lambda: not ws.connected)
        closing = asyncio.create_task(ws.close())
        await asyncio.sleep(0)
        closing.cancel()
        with pytest.raises(asyncio.CancelledError):
            await closing
        # A second close finishes the job.
        await asyncio.wait_for(ws.close(), 2.0)

        async def read_all() -> list[Any]:
            return [message async for message in ws]

        assert await asyncio.wait_for(read_all(), 2.0) == [HeliusWebSocketDisconnected(close_code = 1000)]

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

    @pytest.mark.asyncio
    async def test_an_internal_failure_ends_the_iteration_with_an_error(self, helius, monkeypatch) -> None:
        fake, url = helius

        async def broken(*args: Any) -> None:
            raise RuntimeError("bug")

        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            await ws.logs_subscribe("Wallet111")
            monkeypatch.setattr(ws, "_resubscribe", broken)
            await fake.drop()
            with pytest.raises(HeliusWebSocketError, match = "RuntimeError"):
                await next_of(ws, LogsNotification)
            with pytest.raises(HeliusWebSocketClosed):
                await ws.logs_subscribe("Wallet222")


class TestHeliusWebSocketReconnection:

    @pytest.mark.asyncio
    async def test_a_drop_reconnects_resubscribes_and_says_so(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            await fake.drop()
            disconnected = await next_message(ws)
            marker = await next_message(ws)
            await fake.push(logs_notification(102, "AfterReconnect"))
            message = await next_message(ws)
        assert isinstance(disconnected, HeliusWebSocketDisconnected)
        assert isinstance(marker, HeliusWebSocketReconnected)
        assert marker.attempts == 1
        assert marker.subscriptions == [subscription]
        assert marker.dropped == []
        assert marker.downtime_s >= 0
        assert [r["params"] for r in fake.subscribes()] == [
            [{"mentions": ["Wallet111"]}, {"commitment": "confirmed"}],
        ] * 2
        # The node gave a new id; the caller still sees its own.
        assert (message.subscription, message.signature) == (subscription, "AfterReconnect")

    @pytest.mark.asyncio
    async def test_the_marker_comes_before_the_notifications_of_the_new_connection(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            await ws.logs_subscribe("Wallet111")
            await ws.logs_subscribe("Wallet222")
            fake.notify_on_subscribe = "AfterReconnect"
            await fake.drop()
            kinds = [type(await next_message(ws)).__name__ for _ in range(4)]
        assert kinds == [
            "HeliusWebSocketDisconnected", "HeliusWebSocketReconnected", "LogsNotification", "LogsNotification",
        ]

    @pytest.mark.asyncio
    async def test_reconnection_retries_until_the_node_takes_it(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            await ws.logs_subscribe("Wallet111")
            fake.reject_handshakes = 2
            await fake.drop()
            marker = await next_of(ws, HeliusWebSocketReconnected)
        assert marker.attempts == 3
        assert fake.api_keys == [API_KEY] * 4

    @pytest.mark.asyncio
    async def test_a_server_that_closes_at_once_is_retried_with_a_growing_wait(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.1) as ws:
            await ws.logs_subscribe("Wallet111")
            fake.kick = True
            opened = len(fake.api_keys)
            await fake.drop()
            await asyncio.sleep(1.0)
            attempts = len(fake.api_keys) - opened
        # Waits of 0.05-0.1, 0.1-0.2, 0.2-0.4, 0.4-0.8 s: at most 5 connections in a second.
        assert 2 <= attempts <= 5

    @pytest.mark.asyncio
    async def test_after_a_lasting_connection_the_first_attempt_is_immediate(self, helius, monkeypatch) -> None:
        fake, url = helius
        monkeypatch.setattr(websocket_module, "_STABLE_AFTER_S", 0.0)
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 30.0) as ws:
            await ws.logs_subscribe("Wallet111")
            await fake.drop()
            marker = await next_of(ws, HeliusWebSocketReconnected, timeout = 2.0)
        assert marker.attempts == 1

    @pytest.mark.asyncio
    async def test_a_subscription_refused_on_reconnection_is_dropped(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            dropped = await ws.logs_subscribe("Wallet111")
            kept = await ws.logs_subscribe("Wallet222")
            fake.script = [-32602]
            await fake.drop()
            marker = await next_of(ws, HeliusWebSocketReconnected)
            assert ws.subscriptions == [kept]
        assert marker.subscriptions == [kept]
        assert marker.dropped == [dropped]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("failure", [-32603, "silent"])
    async def test_a_temporary_failure_on_reconnection_keeps_the_subscription(self, helius, failure) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01, request_timeout = 0.2) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            fake.script = [failure]
            await fake.drop()
            marker = await next_of(ws, HeliusWebSocketReconnected, timeout = 3.0)
            assert ws.subscriptions == [subscription]
        assert marker.subscriptions == [subscription]
        assert marker.dropped == []
        assert marker.attempts == 2

    @pytest.mark.asyncio
    async def test_a_drop_during_the_resubscription_does_not_wait_the_request_timeout(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01, request_timeout = 5.0) as ws:
            subscription = await ws.logs_subscribe("Wallet111")
            await ws.logs_subscribe("Wallet222")
            fake.script = ["close"]
            await fake.drop()
            marker = await next_of(ws, HeliusWebSocketReconnected, timeout = 1.0)
        assert marker.attempts == 2
        assert marker.subscriptions == [subscription, subscription + 1]

    @pytest.mark.asyncio
    async def test_unsubscribing_during_the_resubscription_ends_it_on_the_node(self, helius) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            ids = [await ws.logs_subscribe(f"Wallet{i}") for i in range(3)]
            fake.script = [0.1, 0.1, 0.1]
            await fake.drop()
            await wait_until(lambda: len(fake.subscribes()) == 4)  # the first one sent again
            assert await ws.logs_unsubscribe(ids[0]) is True       # answered later
            assert await ws.logs_unsubscribe(ids[2]) is True       # not sent yet
            marker = await next_of(ws, HeliusWebSocketReconnected)
            await wait_until(lambda: fake.unsubscribes())
            new_id = fake.unsubscribes()[0]["params"][0]
            await fake.push(logs_notification(new_id, "Unwanted"))
            await fake.push(logs_notification(new_id + 1, "Wanted"))
            message = await next_of(ws, LogsNotification)
        assert marker.subscriptions == [ids[1]]
        assert len(fake.subscribes()) == 5
        assert (message.subscription, message.signature) == (ids[1], "Wanted")

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
        assert error.value.__context__ is None
        assert error.value.__cause__ is None

    @pytest.mark.asyncio
    async def test_a_refused_handshake_does_not_show_the_key(self, helius) -> None:
        fake, url = helius
        fake.reject_handshakes = 1
        with pytest.raises(HeliusWebSocketError) as error:
            await HeliusWebSocket(url).connect()
        assert "503" in str(error.value)
        assert API_KEY not in str(error.value)
        assert error.value.__context__ is None

    @pytest.mark.asyncio
    async def test_failed_reconnections_do_not_log_the_key(self, helius, caplog) -> None:
        fake, url = helius
        async with HeliusWebSocket(url, reconnect = True, reconnect_min_delay = 0.01) as ws:
            fake.reject_handshakes = 2
            await fake.drop()
            await next_of(ws, HeliusWebSocketReconnected)
        assert caplog.records
        assert all(API_KEY not in record.getMessage() for record in caplog.records)
