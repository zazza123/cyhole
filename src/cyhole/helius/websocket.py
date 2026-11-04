"""Async client for the standard Solana WebSocket subscriptions served by Helius."""

import asyncio
import json
import logging
import time
from collections.abc import Callable
from functools import partial
from types import TracebackType
from typing import Any

import aiohttp

from ..core.client import redact
from ..helius.exception import HeliusRPCError, HeliusWebSocketClosed, HeliusWebSocketError
from ..helius.param import HeliusWebSocketCommitment
from ..helius.schema.websocket import (
    LogsNotification,
    HeliusWebSocketNotification,
    HeliusWebSocketReconnected,
)

log = logging.getLogger(__name__)

HeliusWebSocketMessage = LogsNotification | HeliusWebSocketNotification | HeliusWebSocketReconnected
"""What iterating a [`HeliusWebSocket`][cyhole.helius.websocket.HeliusWebSocket] yields."""

_END = object()  # the client was closed: iteration stops


class HeliusWebSocket:
    """
    Async client for the standard Solana WebSocket subscriptions served by Helius.

    A subscription pushes a notification as soon as something happens, where an HTTP
    client has to poll: `logsSubscribe` on an address, for example, tells of every
    transaction that mentions it, without a `getSignaturesForAddress` call a minute.
    The standard methods are served on every Helius plan, the free one included, and
    billed by the data streamed (2 credits per 0.1 MB at the time of writing) plus
    1 credit for each connection opened.

    Build it with [`Helius.websocket`][cyhole.helius.interaction.Helius.websocket] and
    use it as an async context manager. Subscribe, then iterate it to receive the
    notifications of every subscription, in the order they arrive:

    ```python
    import asyncio
    from cyhole.helius import Helius
    from cyhole.helius.schema import LogsNotification, HeliusWebSocketReconnected

    helius = Helius(api_key="your-api-key")

    async def main():
        async with helius.websocket(reconnect = True) as ws:
            await ws.logs_subscribe("WalletAddressHere")
            async for message in ws:
                if isinstance(message, LogsNotification):
                    print(message.slot, message.signature)
                elif isinstance(message, HeliusWebSocketReconnected):
                    print("back after", message.downtime_s, "s: catch up by polling")

    asyncio.run(main())
    ```

    **Reconnection.** With `reconnect = False` a dropped connection ends the iteration
    with [`HeliusWebSocketClosed`][cyhole.helius.exception.HeliusWebSocketClosed]. With
    `reconnect = True` the client opens a new connection, waiting from
    `reconnect_min_delay` to `reconnect_max_delay` seconds between attempts, sends its
    subscriptions again, and yields a
    [`HeliusWebSocketReconnected`][cyhole.helius.schema.HeliusWebSocketReconnected]
    marker. Subscription ids stay the ones the subscribe methods returned. Notifications
    pushed while the connection was down are lost: the marker is the cue to catch up.

    **Keep-alive.** Helius closes a connection after 10 minutes without traffic and
    expects a ping at least once a minute: the client sends one every `heartbeat`
    seconds, and treats a missing pong as a dropped connection.

    **API key.** The key is part of the URL. It is masked in every error the client
    raises or logs, and the client's `repr` does not show the URL.

    Notifications wait in an unbounded queue until they are read, so a consumer that
    stops reading makes it grow.
    """

    def __init__(
        self,
        url: str,
        reconnect: bool = False,
        heartbeat: float = 30.0,
        request_timeout: float = 10.0,
        reconnect_min_delay: float = 1.0,
        reconnect_max_delay: float = 60.0,
    ) -> None:
        """
        Parameters:
            url: the WebSocket endpoint, with the API key, e.g.
                `wss://mainnet.helius-rpc.com/?api-key=...`;
                [`Helius.websocket`][cyhole.helius.interaction.Helius.websocket] builds it.
            reconnect: reopen a dropped connection and send the subscriptions again,
                instead of ending the iteration with `HeliusWebSocketClosed`.
            heartbeat: seconds between two pings; Helius expects one at least once a minute.
            request_timeout: seconds to wait for the answer to a subscribe or unsubscribe
                request, and for a dropped connection to come back before a request fails.
            reconnect_min_delay: seconds before the second reconnection attempt; the wait
                doubles at each failed attempt.
            reconnect_max_delay: the longest wait between two reconnection attempts, in seconds.
        """
        self._url = url
        self._reconnect = reconnect
        self._heartbeat = heartbeat
        self._request_timeout = request_timeout
        self._reconnect_min_delay = reconnect_min_delay
        self._reconnect_max_delay = reconnect_max_delay

        self._session: aiohttp.ClientSession | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._runner: asyncio.Task[None] | None = None
        self._reading: asyncio.Task[None] | None = None
        self._connected = asyncio.Event()
        self._closing = False
        self._finished = False
        self._queue: asyncio.Queue[Any] = asyncio.Queue()

        self._next_request_id = 0
        self._pending: dict[int, tuple[asyncio.Future[Any], Callable[[Any], None] | None]] = {}
        self._next_subscription_id = 0
        # client id -> (subscribe method, its params, unsubscribe method)
        self._subscriptions: dict[int, tuple[str, list[Any], str]] = {}
        self._server_by_client: dict[int, int] = {}
        self._client_by_server: dict[int, int] = {}

    def __repr__(self) -> str:
        return (
            f"HeliusWebSocket(connected = {self.connected}, "
            f"subscriptions = {len(self._subscriptions)}, reconnect = {self._reconnect})"
        )

    @property
    def connected(self) -> bool:
        """`True` while a connection is open."""
        return self._connected.is_set()

    @property
    def subscriptions(self) -> list[int]:
        """Ids of the active subscriptions, as the subscribe methods returned them."""
        return list(self._subscriptions)

    # ─── lifecycle ────────────────────────────────────────────────────────────

    async def __aenter__(self) -> "HeliusWebSocket":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

    async def connect(self) -> None:
        """
        Open the connection. Called by `async with`; call it directly only when not
        using the client as a context manager, and then call `close` when done.

        Raises:
            HeliusWebSocketError: the connection could not be opened.
        """
        if self._session is not None:
            return
        self._session = aiohttp.ClientSession()
        try:
            await self._open()
        except BaseException:
            await self._session.close()
            self._session = None
            raise
        self._runner = asyncio.create_task(self._run(), name = "cyhole.helius.websocket")

    async def close(self) -> None:
        """
        Close the connection and end the iteration. Pending requests fail with
        `HeliusWebSocketClosed`. Closing twice is harmless.
        """
        if self._closing:
            return
        self._closing = True
        if self._ws is not None:
            await self._ws.close()
        for task in (self._runner, self._reading):
            if task is not None and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        self._connected.clear()
        self._fail_pending(HeliusWebSocketClosed("the client was closed"))
        if self._session is not None:
            await self._session.close()
        self._queue.put_nowait(_END)

    # ─── subscriptions ────────────────────────────────────────────────────────

    async def logs_subscribe(
        self,
        mentions: str,
        commitment: HeliusWebSocketCommitment | str = HeliusWebSocketCommitment.CONFIRMED,
    ) -> int:
        """
        This function refers to the **logsSubscribe** WebSocket method.

        Subscribes to the transactions that mention an address, as signer or as any
        other account. Each one is pushed as a
        [`LogsNotification`][cyhole.helius.schema.LogsNotification] with its signature,
        slot, error and logs, as soon as it reaches `commitment`. It is the push
        counterpart of polling `getSignaturesForAddress`.

        Parameters:
            mentions: the address, base-58 encoded. Solana accepts a single address per
                subscription: subscribe once per address.
            commitment: the commitment level a transaction must reach before it is
                pushed; one of [`HeliusWebSocketCommitment`][cyhole.helius.param.HeliusWebSocketCommitment].
                Default `confirmed`.

        Returns:
            the subscription id, to pass to `logs_unsubscribe`. It stays the same
                across reconnections.

        Raises:
            HeliusRPCError: the node refused the subscription.
            HeliusWebSocketClosed: the connection is closed, or dropped before the answer.
            HeliusWebSocketError: no answer within `request_timeout`.
        """
        level = commitment.value if isinstance(commitment, HeliusWebSocketCommitment) else commitment
        params: list[Any] = [{"mentions": [mentions]}, {"commitment": level}]
        return await self._subscribe("logsSubscribe", params, "logsUnsubscribe")

    async def logs_unsubscribe(self, subscription: int) -> bool:
        """
        This function refers to the **logsUnsubscribe** WebSocket method.

        Ends a subscription made with `logs_subscribe`. Its notifications already
        received may still be yielded; later ones are dropped.

        Parameters:
            subscription: the id `logs_subscribe` returned.

        Returns:
            `True` if the subscription was active, `False` if the id is unknown.

        Raises:
            HeliusRPCError: the node refused the request.
            HeliusWebSocketError: no answer within `request_timeout`.
        """
        return await self._unsubscribe(subscription)

    async def _subscribe(self, method: str, params: list[Any], unsubscribe_method: str) -> int:
        self._next_subscription_id += 1
        client_id = self._next_subscription_id
        await self._request(method, params, on_result = lambda result: self._map(client_id, result))
        self._subscriptions[client_id] = (method, params, unsubscribe_method)
        return client_id

    async def _unsubscribe(self, subscription: int) -> bool:
        entry = self._subscriptions.pop(subscription, None)
        if entry is None:
            return False
        server_id = self._server_by_client.pop(subscription, None)
        if server_id is not None:
            self._client_by_server.pop(server_id, None)
        if server_id is None or not self.connected:
            return True  # nothing left on the node: the connection it lived on is gone
        try:
            await self._request(entry[2], [server_id])
        except HeliusWebSocketClosed:
            pass  # dropped meanwhile: the subscription went with the connection
        return True

    def _map(self, client_id: int, result: Any) -> None:
        server_id = int(result)
        self._server_by_client[client_id] = server_id
        self._client_by_server[server_id] = client_id

    # ─── iteration ────────────────────────────────────────────────────────────

    def __aiter__(self) -> "HeliusWebSocket":
        return self

    async def __anext__(self) -> HeliusWebSocketMessage:
        if self._finished:
            raise StopAsyncIteration
        item = await self._queue.get()
        if item is _END:
            self._finished = True
            raise StopAsyncIteration
        if isinstance(item, HeliusWebSocketClosed):
            self._finished = True
            raise item
        return item

    # ─── connection ───────────────────────────────────────────────────────────

    async def _open(self) -> None:
        assert self._session is not None
        try:
            self._ws = await self._session.ws_connect(self._url, heartbeat = self._heartbeat)
        except (aiohttp.ClientError, OSError, asyncio.TimeoutError) as error:
            # aiohttp's errors carry the URL, and with it the API key.
            raise HeliusWebSocketError(
                f"could not open the WebSocket connection: {redact(str(error)) or type(error).__name__}"
            ) from None
        self._connected.set()

    async def _run(self) -> None:
        """Read the open connection; on a drop, reconnect or end the iteration."""
        reconnected: tuple[float, int] | None = None
        while True:
            assert self._ws is not None
            self._reading = asyncio.create_task(self._read(self._ws))
            if reconnected is not None:
                dropped_at, reopened_after = reconnected
                reconnected = None
                sent = await self._resubscribe()
                if sent is not None:
                    self._queue.put_nowait(HeliusWebSocketReconnected(
                        attempts = reopened_after,
                        downtime_s = round(time.monotonic() - dropped_at, 3),
                        subscriptions = sent,
                    ))
            await self._reading
            if self._closing:
                return
            if not self._reconnect:
                self._queue.put_nowait(HeliusWebSocketClosed("the connection was dropped"))
                return
            log.warning("helius websocket: connection dropped, reconnecting")
            dropped_at = time.monotonic()
            attempts = await self._reopen()
            if attempts is None:
                return
            reconnected = (dropped_at, attempts)

    async def _reopen(self) -> int | None:
        """Open a new connection, retrying with a doubling wait; `None` if closed meanwhile."""
        delay = self._reconnect_min_delay
        attempts = 0
        while not self._closing:
            attempts += 1
            try:
                await self._open()
                return attempts
            except HeliusWebSocketError as error:
                log.warning("helius websocket: reconnection attempt %d failed (%s); next in %.1f s", attempts, error, delay)
            await asyncio.sleep(delay)
            delay = min(delay * 2, self._reconnect_max_delay)
        return None

    async def _resubscribe(self) -> list[int] | None:
        """Send every subscription again; `None` if the connection dropped meanwhile."""
        self._server_by_client.clear()
        self._client_by_server.clear()
        sent: list[int] = []
        for client_id, (method, params, _) in list(self._subscriptions.items()):
            try:
                await self._request(method, params, on_result = partial(self._map, client_id))
            except HeliusWebSocketClosed:
                return None
            except HeliusWebSocketError as error:  # refused, or no answer
                log.warning("helius websocket: subscription %d dropped, not accepted on reconnection: %s", client_id, error)
                self._subscriptions.pop(client_id, None)
                continue
            except HeliusRPCError as error:
                log.warning("helius websocket: subscription %d dropped, refused on reconnection: %s", client_id, error)
                self._subscriptions.pop(client_id, None)
                continue
            sent.append(client_id)
        return sent

    async def _read(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        """Dispatch the connection's messages until it closes."""
        try:
            async for message in ws:
                if message.type == aiohttp.WSMsgType.TEXT:
                    self._dispatch(message.data)
                elif message.type == aiohttp.WSMsgType.ERROR:
                    break
        except (aiohttp.ClientError, OSError, asyncio.TimeoutError) as error:
            log.warning("helius websocket: read failed: %s", redact(str(error)) or type(error).__name__)
        finally:
            # Here, not in the caller: a request waiting for its answer, such as a
            # subscription sent again after a reconnection, must fail at once.
            self._connected.clear()
            self._fail_pending(HeliusWebSocketClosed("the connection was dropped"))

    def _dispatch(self, data: str) -> None:
        try:
            payload = json.loads(data)
        except ValueError:
            log.warning("helius websocket: a message that is not JSON was dropped")
            return
        if not isinstance(payload, dict):
            return
        if "id" in payload and ("result" in payload or "error" in payload):
            self._answer(payload)
            return
        method = payload.get("method")
        if isinstance(method, str):
            message = self._notification(method, payload.get("params") or {})
            if message is not None:
                self._queue.put_nowait(message)

    def _answer(self, payload: dict[str, Any]) -> None:
        entry = self._pending.pop(payload["id"], None)
        if entry is None:
            return
        future, on_result = entry
        if future.done():
            return
        error = payload.get("error")
        if isinstance(error, dict):
            future.set_exception(HeliusRPCError(error.get("code", 0), error.get("message", ""), error.get("data")))
            return
        result = payload.get("result")
        if on_result is not None:
            # Before the next message is read: a notification can follow the answer at once.
            try:
                on_result(result)
            except (TypeError, ValueError):
                future.set_exception(HeliusWebSocketError(f"unexpected answer: {result!r}"))
                return
        future.set_result(result)

    def _notification(self, method: str, params: dict[str, Any]) -> HeliusWebSocketMessage | None:
        server_id = params.get("subscription")
        client_id = self._client_by_server.get(server_id) if isinstance(server_id, int) else None
        if server_id is not None and client_id is None:
            return None  # a subscription ended, or one of a previous connection
        result = params.get("result")
        if method == "logsNotification" and isinstance(result, dict) and client_id is not None:
            value = result.get("value") or {}
            try:
                return LogsNotification.model_validate({
                    "subscription": client_id,
                    "slot": (result.get("context") or {}).get("slot"),
                    "signature": value.get("signature"),
                    "err": value.get("err"),
                    "logs": value.get("logs") or [],
                })
            except ValueError:
                pass  # not the shape documented: yielded as it came
        return HeliusWebSocketNotification(method = method, subscription = client_id, result = result)

    async def _request(
        self, method: str, params: list[Any], on_result: Callable[[Any], None] | None = None
    ) -> Any:
        if self._closing or self._session is None:
            raise HeliusWebSocketClosed("the client is closed")
        if not self.connected:
            if not self._reconnect:
                raise HeliusWebSocketClosed("the connection was dropped")
            try:
                await asyncio.wait_for(self._connected.wait(), timeout = self._request_timeout)
            except asyncio.TimeoutError:
                raise HeliusWebSocketClosed(f"{method}: not reconnected within {self._request_timeout} s") from None
        assert self._ws is not None
        self._next_request_id += 1
        request_id = self._next_request_id
        future: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[request_id] = (future, on_result)
        try:
            await self._ws.send_str(json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}))
            return await asyncio.wait_for(future, timeout = self._request_timeout)
        except (aiohttp.ClientError, ConnectionError) as error:
            raise HeliusWebSocketClosed(f"{method}: {redact(str(error)) or type(error).__name__}") from None
        except asyncio.TimeoutError:
            raise HeliusWebSocketError(f"{method}: no answer within {self._request_timeout} s") from None
        finally:
            self._pending.pop(request_id, None)

    def _fail_pending(self, error: HeliusWebSocketClosed) -> None:
        pending, self._pending = self._pending, {}
        for future, _ in pending.values():
            if not future.done():
                future.set_exception(error)
