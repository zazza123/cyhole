"""Async client for the standard Solana WebSocket subscriptions served by Helius."""

import asyncio
import json
import logging
import random
import time
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from functools import partial
from types import TracebackType
from typing import Any

import aiohttp
from pydantic import ValidationError

from ..core.client import redact
from ..helius.exception import (
    HeliusRPCError,
    HeliusWebSocketClosed,
    HeliusWebSocketError,
    HeliusWebSocketTimeout,
)
from ..helius.param import HeliusWebSocketCommitment
from ..helius.schema.websocket import (
    LogsNotification,
    HeliusWebSocketDisconnected,
    HeliusWebSocketNotification,
    HeliusWebSocketReconnected,
)

log = logging.getLogger(__name__)

HeliusWebSocketMessage = (
    LogsNotification | HeliusWebSocketNotification | HeliusWebSocketDisconnected | HeliusWebSocketReconnected
)
"""What iterating a [`HeliusWebSocket`][cyhole.helius.websocket.HeliusWebSocket] yields."""

_END = object()  # the client was closed: iteration stops

# A connection that lasted this long was healthy: the wait between reconnection
# attempts starts again from `reconnect_min_delay`, and the first attempt is
# immediate. A shorter one keeps the wait growing, so a node that accepts and
# then closes every connection is not hammered.
_STABLE_AFTER_S = 60.0

# JSON-RPC errors that will not pass by retrying: a subscription the node
# refuses with one of these on reconnection is dropped.
_PERMANENT_RPC_ERRORS = frozenset({-32600, -32601, -32602})

# client id -> (subscribe method, its params, unsubscribe method)
_Subscription = tuple[str, list[Any], str]


@dataclass
class _Pending:
    """A request sent and waiting for its answer."""
    future: asyncio.Future[Any]
    # Called with the result as the answer is read, before the next message.
    on_result: Callable[[Any], None] | None = None
    # Called with the result of an answer that comes after the request timed out.
    on_late: Callable[[Any], None] | None = None


@dataclass
class _Outage:
    """A dropped connection, from the drop until the subscriptions are active again."""
    started: float
    immediate: bool  # the first reconnection attempt does not wait
    attempts: int = 0
    dropped: list[int] = field(default_factory = list)


class HeliusWebSocket:
    """
    Async client for the standard Solana WebSocket subscriptions served by Helius.

    A subscription pushes a notification as soon as something happens, where an HTTP
    client has to poll: `logsSubscribe` on an address, for example, tells of every
    transaction that mentions it, without a `getSignaturesForAddress` call a minute.
    The standard methods are served on every Helius plan, the free one included, and
    billed by the data streamed (2 credits per 0.1 MB at the time of writing) plus
    1 credit for each connection opened.

    Build it with [`Helius.websocket`][cyhole.helius.Helius.websocket] and
    use it as an async context manager. Subscribe, then iterate it to receive the
    notifications of every subscription, in the order they arrive:

    ```python
    import asyncio
    from cyhole.helius import Helius
    from cyhole.helius.schema import LogsNotification, HeliusWebSocketReconnected

    helius = Helius(api_key="your-api-key")

    async def main():
        async with helius.websocket(reconnect=True) as ws:
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
    `reconnect = True` the client yields a
    [`HeliusWebSocketDisconnected`][cyhole.helius.schema.HeliusWebSocketDisconnected]
    marker, opens a new connection, sends its subscriptions again, and yields a
    [`HeliusWebSocketReconnected`][cyhole.helius.schema.HeliusWebSocketReconnected]
    marker. Every notification of the new connection comes after that marker.
    Subscription ids stay the ones the subscribe methods returned. Notifications
    pushed while the connection was down are lost: the marker is the cue to catch up.

    The waits between attempts start at `reconnect_min_delay` seconds and double up to
    `reconnect_max_delay`; each one is drawn between half and all of its value, so that
    clients dropped together do not come back together. The wait keeps growing over a
    connection that drops again within a minute, and starts over, with an immediate
    first attempt, after one that lasted longer. A subscription the node refuses for
    good on reconnection is dropped and listed in the marker; a failure that may pass,
    such as a timeout, makes the client reconnect and try again.

    **Keep-alive.** Helius closes a connection after 10 minutes without traffic and
    expects a ping at least once a minute: the client sends one every `heartbeat`
    seconds, busy or idle, and treats a pong missing for half that time as a dropped
    connection.

    **API key.** The key is part of the URL. It is masked in every error the client
    raises or logs, and the client's `repr` does not show the URL.

    **Errors.** A message of unexpected shape is logged and dropped. An unexpected
    error inside the client ends the iteration with a
    [`HeliusWebSocketError`][cyhole.helius.exception.HeliusWebSocketError] instead of
    leaving it waiting.

    Notifications wait in an unbounded queue until they are read, so a consumer that
    stops reading makes it grow. A closed client cannot be opened again: build a new one.
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
                [`Helius.websocket`][cyhole.helius.Helius.websocket] builds it.
            reconnect: reopen a dropped connection and send the subscriptions again,
                instead of ending the iteration with `HeliusWebSocketClosed`.
            heartbeat: seconds between two pings; Helius expects one at least once a minute.
            request_timeout: seconds to wait for the answer to a subscribe or unsubscribe
                request, and for a dropped connection to come back before a request fails.
            reconnect_min_delay: the first wait between reconnection attempts, in seconds;
                it doubles at each attempt that fails.
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
        self._background: set[asyncio.Task[None]] = set()
        self._connected = asyncio.Event()
        self._stopped = asyncio.Event()  # the runner ended or `close` was called
        self._stop_reason = "the client is closed"
        self._closing = False
        self._closed = False
        self._finished = False
        self._queue: asyncio.Queue[Any] = asyncio.Queue()

        self._delay = reconnect_min_delay
        self._healthy_since = 0.0
        self._outage: _Outage | None = None
        # Notifications read while the subscriptions are being sent again, yielded after the marker.
        self._holding: list[HeliusWebSocketMessage] | None = None

        self._next_request_id = 0
        self._pending: dict[int, _Pending] = {}
        self._next_subscription_id = 0
        self._subscriptions: dict[int, _Subscription] = {}
        self._joining: dict[int, _Subscription] = {}  # subscribe requests waiting for their answer
        self._server_by_client: dict[int, int] = {}
        self._client_by_server: dict[int, int] = {}

    def __repr__(self) -> str:
        """The client's state, without the URL and so without the API key."""
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
        """Open the connection; see `connect`."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the client; see `close`."""
        await self.close()

    async def connect(self) -> None:
        """
        Open the connection. Called by `async with`; call it directly only when not
        using the client as a context manager, and then call `close` when done.
        Calling it on a connected client does nothing.

        Raises:
            HeliusWebSocketClosed: the client was closed; a closed client cannot be
                opened again.
            HeliusWebSocketError: the connection could not be opened.
        """
        if self._closing:
            raise HeliusWebSocketClosed("the client was closed: build a new one")
        if self._session is not None:
            return
        self._session = aiohttp.ClientSession()
        try:
            await self._open()
        except BaseException:
            await self._session.close()
            self._session = None
            raise
        self._healthy_since = time.monotonic()
        self._runner = asyncio.create_task(self._run(), name = "cyhole.helius.websocket")

    async def close(self) -> None:
        """
        Close the connection and end the iteration. Pending requests, and requests
        waiting for a reconnection, fail with `HeliusWebSocketClosed`. Closing twice is
        harmless; if a `close` is cancelled, the next one finishes the job.
        """
        if self._closed:
            return
        self._closing = True
        if self._stop_reason == "the client is closed" or not self._stopped.is_set():
            self._stop_reason = "the client was closed"
        self._stopped.set()
        if self._ws is not None and not self._ws.closed:
            await self._ws.close()
        tasks = [task for task in (self._runner, self._reading, *self._background) if task is not None]
        for task in tasks:
            task.cancel()
        if tasks:
            # `wait` does not raise what the tasks raise, but lets a cancellation of
            # the caller through.
            await asyncio.wait(tasks)
        for task in tasks:
            if not task.cancelled():
                task.exception()  # retrieved, so asyncio does not report it as lost
        self._connected.clear()
        self._fail_pending(HeliusWebSocketClosed("the client was closed"))
        if self._session is not None:
            await self._session.close()
        self._closed = True
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
            HeliusWebSocketTimeout: no answer within `request_timeout`. If the answer
                comes later, the client ends the subscription on the node.
        """
        level = commitment.value if isinstance(commitment, HeliusWebSocketCommitment) else commitment
        params: list[Any] = [{"mentions": [mentions]}, {"commitment": level}]
        return await self._subscribe("logsSubscribe", params, "logsUnsubscribe")

    async def logs_unsubscribe(self, subscription: int) -> bool:
        """
        This function refers to the **logsUnsubscribe** WebSocket method.

        Ends a subscription made with `logs_subscribe`. Its notifications already
        received may still be yielded; later ones are dropped. The client forgets
        the subscription even when the request fails: the node may then keep
        streaming it, billed, until the connection closes.

        Parameters:
            subscription: the id `logs_subscribe` returned.

        Returns:
            `True` if the subscription was active, `False` if the id is unknown.

        Raises:
            HeliusRPCError: the node refused the request.
            HeliusWebSocketTimeout: no answer within `request_timeout`.
        """
        return await self._unsubscribe(subscription)

    async def _subscribe(self, method: str, params: list[Any], unsubscribe_method: str) -> int:
        """
        Send a subscribe request and return the client id of the new subscription.

        The subscription becomes active when its answer is read, in `_accept`; until
        then it waits in `_joining`, out of reach of a resubscription.

        Parameters:
            method: the subscribe method, e.g. `logsSubscribe`.
            params: its JSON-RPC params, also sent again on reconnection.
            unsubscribe_method: the method that ends it, e.g. `logsUnsubscribe`.

        Returns:
            the client id of the subscription.
        """
        self._next_subscription_id += 1
        client_id = self._next_subscription_id
        self._joining[client_id] = (method, params, unsubscribe_method)
        try:
            await self._request(
                method,
                params,
                on_result = partial(self._accept, client_id, unsubscribe_method),
                on_late = partial(self._end_on_node, unsubscribe_method),
            )
        finally:
            self._joining.pop(client_id, None)
        return client_id

    async def _unsubscribe(self, subscription: int) -> bool:
        """
        Forget a subscription and end it on the node if it is active there.

        Parameters:
            subscription: the client id of the subscription.

        Returns:
            `True` if the subscription was known, `False` otherwise.
        """
        entry = self._subscriptions.pop(subscription, None)
        if entry is None:
            return False
        server_id = self._server_by_client.pop(subscription, None)
        if server_id is not None:
            self._client_by_server.pop(server_id, None)
        if server_id is None or not self.connected:
            # Not on the node: the connection it lived on is gone, or it is being sent
            # again and `_accept` will end it as soon as the node answers.
            return True
        try:
            await self._request(entry[2], [server_id], wait = False)
        except HeliusWebSocketClosed:
            pass  # dropped meanwhile: the subscription went with the connection
        return True

    def _accept(self, client_id: int, unsubscribe_method: str, result: Any) -> None:
        """
        Map the node's id of a subscription to the client's, as its answer is read.

        A subscription the caller ended while the answer was on its way is ended on
        the node instead.

        Parameters:
            client_id: the client id of the subscription.
            unsubscribe_method: the method that ends it on the node.
            result: the answer's result, the node's subscription id.

        Raises:
            ValueError: the result is not a subscription id.
        """
        server_id = _subscription_id(result)
        joining = self._joining.pop(client_id, None)
        if joining is not None:
            self._subscriptions[client_id] = joining
        if client_id not in self._subscriptions:
            self._end_on_node(unsubscribe_method, server_id)
            return
        self._server_by_client[client_id] = server_id
        self._client_by_server[server_id] = client_id

    def _end_on_node(self, unsubscribe_method: str, result: Any) -> None:
        """
        End on the node a subscription the client does not want, without waiting.

        Parameters:
            unsubscribe_method: the method that ends it.
            result: the node's subscription id, as its answer carried it.
        """
        try:
            server_id = _subscription_id(result)
        except ValueError:
            return
        ws = self._ws

        async def end() -> None:
            if self._ws is not ws or not self.connected:
                return  # the connection it lived on is gone, and the subscription with it
            try:
                await self._request(unsubscribe_method, [server_id], wait = False)
            except (HeliusWebSocketError, HeliusRPCError) as error:
                log.warning("helius websocket: unwanted subscription %d not ended: %s", server_id, error)

        self._spawn(end(), "cyhole.helius.websocket.unsubscribe")

    # ─── iteration ────────────────────────────────────────────────────────────

    def __aiter__(self) -> "HeliusWebSocket":
        """The client is its own iterator: see `__anext__`."""
        return self

    async def __anext__(self) -> HeliusWebSocketMessage:
        """
        The next notification or marker, waiting for it.

        Raises:
            StopAsyncIteration: the client was closed.
            HeliusWebSocketClosed: the connection dropped and `reconnect` is off.
            HeliusWebSocketError: the client stopped on an unexpected error.
        """
        if self._finished:
            raise StopAsyncIteration
        item = await self._queue.get()
        if item is _END:
            self._finished = True
            raise StopAsyncIteration
        if isinstance(item, HeliusWebSocketError):
            self._finished = True
            raise item
        return item

    def _emit(self, message: HeliusWebSocketMessage) -> None:
        """Queue a notification, or hold it while the subscriptions are sent again."""
        if self._holding is not None:
            self._holding.append(message)
        else:
            self._queue.put_nowait(message)

    # ─── connection ───────────────────────────────────────────────────────────

    async def _open(self) -> None:
        """
        Open a connection.

        Raises:
            HeliusWebSocketError: it could not be opened. The aiohttp error is not
                chained, since it carries the URL and with it the API key.
        """
        assert self._session is not None
        try:
            self._ws = await self._session.ws_connect(self._url, heartbeat = self._heartbeat)
        except (aiohttp.ClientError, OSError, asyncio.TimeoutError) as error:
            message = redact(str(error)) or type(error).__name__
        else:
            self._connected.set()
            return
        raise HeliusWebSocketError(f"could not open the WebSocket connection: {message}")

    async def _run(self) -> None:
        """Serve the connections until the client is closed or stops; never raises."""
        try:
            await self._serve()
        except Exception as error:  # a bug, or a case not foreseen: end the iteration, do not hang it
            message = f"the client stopped on an unexpected error: {type(error).__name__}: {redact(str(error))}"
            log.error("helius websocket: %s", message)
            self._stop_reason = message
            self._queue.put_nowait(HeliusWebSocketError(message))
            if self._ws is not None and not self._ws.closed:
                await self._ws.close()
        finally:
            self._stopped.set()
            self._connected.clear()
            self._fail_pending(HeliusWebSocketClosed(self._stop_reason))

    async def _serve(self) -> None:
        """Read each connection; on a drop, reconnect and resubscribe, or end the iteration."""
        assert self._ws is not None
        ws = self._ws
        while True:
            self._reading = asyncio.create_task(self._read(ws), name = "cyhole.helius.websocket.read")
            if self._outage is not None:
                await self._resubscribe(ws)
            await self._reading
            if self._closing:
                return
            if not self._reconnect:
                self._stop_reason = "the connection was dropped"
                self._queue.put_nowait(HeliusWebSocketClosed("the connection was dropped"))
                return
            self._server_by_client.clear()
            self._client_by_server.clear()
            if self._outage is None:
                now = time.monotonic()
                stable = now - self._healthy_since >= _STABLE_AFTER_S
                if stable:
                    self._delay = self._reconnect_min_delay
                self._outage = _Outage(started = now, immediate = stable)
                self._holding = []
                log.warning("helius websocket: connection dropped (close code %s), reconnecting", ws.close_code)
                self._queue.put_nowait(HeliusWebSocketDisconnected(close_code = ws.close_code))
            else:
                log.warning(
                    "helius websocket: connection dropped again while reconnecting (close code %s)", ws.close_code
                )
            if not await self._reopen():
                return
            assert self._ws is not None
            ws = self._ws

    async def _reopen(self) -> bool:
        """
        Open a new connection, waiting a growing time between attempts.

        Returns:
            `True` once connected, `False` if the client was closed meanwhile.
        """
        outage = self._outage
        assert outage is not None
        while not self._closing:
            if outage.immediate:
                outage.immediate = False
            else:
                await asyncio.sleep(self._delay * random.uniform(0.5, 1.0))
                self._delay = min(self._delay * 2, self._reconnect_max_delay)
                if self._closing:
                    break
            outage.attempts += 1
            try:
                await self._open()
                return True
            except HeliusWebSocketError as error:
                log.warning("helius websocket: reconnection attempt %d failed (%s)", outage.attempts, error)
        return False

    async def _resubscribe(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        """
        Send every subscription again on a new connection, then yield the marker and
        the notifications held meanwhile.

        A subscription the node refuses for good is dropped. On any other failure the
        connection is closed, so that `_serve` reconnects and tries again; then neither
        the marker nor the held notifications are yielded yet.

        Parameters:
            ws: the new connection.
        """
        outage = self._outage
        assert outage is not None
        sent: list[int] = []
        for client_id in list(self._subscriptions):
            entry = self._subscriptions.get(client_id)
            if entry is None:
                continue  # unsubscribed while the others were being sent
            method, params, unsubscribe_method = entry
            try:
                await self._request(
                    method,
                    params,
                    on_result = partial(self._accept, client_id, unsubscribe_method),
                    on_late = partial(self._end_on_node, unsubscribe_method),
                    wait = False,
                )
            except HeliusWebSocketClosed:
                return  # dropped again: `_serve` reconnects
            except HeliusRPCError as error:
                if error.code in _PERMANENT_RPC_ERRORS:
                    log.warning("helius websocket: subscription %d dropped, refused on reconnection: %s", client_id, error)
                    self._subscriptions.pop(client_id, None)
                    outage.dropped.append(client_id)
                    continue
                log.warning("helius websocket: subscription %d not sent again (%s), reconnecting", client_id, error)
                await ws.close()
                return
            except HeliusWebSocketError as error:  # no answer in time, or an unexpected one
                log.warning("helius websocket: subscription %d not sent again (%s), reconnecting", client_id, error)
                await ws.close()
                return
            if client_id in self._subscriptions:
                sent.append(client_id)
        self._queue.put_nowait(HeliusWebSocketReconnected(
            attempts = outage.attempts,
            downtime_s = round(time.monotonic() - outage.started, 3),
            subscriptions = sent,
            dropped = outage.dropped,
        ))
        held, self._holding = self._holding or [], None
        for message in held:
            self._queue.put_nowait(message)
        self._outage = None
        self._healthy_since = time.monotonic()

    async def _read(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        """
        Dispatch the connection's messages until it closes, pinging it meanwhile.

        Parameters:
            ws: the connection.
        """
        pinging = asyncio.create_task(self._ping(ws), name = "cyhole.helius.websocket.ping")
        try:
            async for message in ws:
                if message.type == aiohttp.WSMsgType.TEXT:
                    try:
                        self._dispatch(message.data)
                    except Exception as error:  # one bad message must not stop the client
                        log.warning("helius websocket: a message of unexpected shape was dropped (%s)", type(error).__name__)
                elif message.type == aiohttp.WSMsgType.ERROR:
                    break
        except (aiohttp.ClientError, OSError, asyncio.TimeoutError) as error:
            log.warning("helius websocket: read failed: %s", redact(str(error)) or type(error).__name__)
        finally:
            pinging.cancel()
            # Here, not in the caller: a request waiting for its answer, such as a
            # subscription sent again after a reconnection, must fail at once.
            self._connected.clear()
            self._fail_pending(HeliusWebSocketClosed("the connection was dropped"))

    async def _ping(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        """
        Ping the connection every `heartbeat` seconds until it closes.

        aiohttp's own heartbeat pings only a connection that received nothing for that
        long, so a busy stream would send no frame at all; this one pings regardless.
        The missing pong is still detected by aiohttp's heartbeat.

        Parameters:
            ws: the connection.
        """
        while not ws.closed:
            await asyncio.sleep(self._heartbeat)
            try:
                await ws.ping()
            except Exception:  # closing: the reader sees the drop
                return

    def _dispatch(self, data: str) -> None:
        """
        Route a text message: an answer to `_answer`, a notification to the queue.

        Parameters:
            data: the message, a JSON-RPC answer or notification.
        """
        try:
            payload = json.loads(data)
        except ValueError:
            log.warning("helius websocket: a message that is not JSON was dropped")
            return
        if not isinstance(payload, dict):
            log.warning("helius websocket: a message that is not a JSON object was dropped")
            return
        if "id" in payload and ("result" in payload or "error" in payload):
            self._answer(payload)
            return
        method = payload.get("method")
        if isinstance(method, str):
            params = payload.get("params")
            message = self._notification(method, params if isinstance(params, dict) else {})
            if message is not None:
                self._emit(message)

    def _answer(self, payload: dict[str, Any]) -> None:
        """
        Settle the request an answer belongs to.

        Parameters:
            payload: the JSON-RPC answer, with an `id` and a `result` or an `error`.
        """
        request_id = payload.get("id")
        error = payload.get("error")
        if not isinstance(request_id, int) or isinstance(request_id, bool):
            # JSON-RPC answers a request it could not read with a null id: no request
            # can be told, and the one waiting fails on its timeout.
            log.warning("helius websocket: an answer to no known request: %s", redact(str(error or payload.get("result"))))
            return
        entry = self._pending.pop(request_id, None)
        if entry is None:
            return
        if entry.future.done():  # timed out: the caller has gone
            if entry.on_late is not None and error is None:
                entry.on_late(payload.get("result"))
            return
        if error is not None:
            if isinstance(error, dict):
                code, message, data = error.get("code"), error.get("message"), error.get("data")
            else:
                code, message, data = None, error, None
            entry.future.set_exception(HeliusRPCError(code if isinstance(code, int) else 0, str(message or ""), data))
            return
        result = payload.get("result")
        if entry.on_result is not None:
            # Before the next message is read: a notification can follow the answer at once.
            try:
                entry.on_result(result)
            except (TypeError, ValueError):
                entry.future.set_exception(HeliusWebSocketError(f"unexpected answer: {result!r}"))
                return
        entry.future.set_result(result)

    def _notification(self, method: str, params: dict[str, Any]) -> HeliusWebSocketMessage | None:
        """
        Build the message to yield for a notification.

        Parameters:
            method: the notification's method, e.g. `logsNotification`.
            params: its params, with the node's `subscription` id and the `result`.

        Returns:
            the typed notification, a `HeliusWebSocketNotification` for a method or a
                shape the client does not know, or `None` for a subscription that is
                not active (ended, or of a previous connection).
        """
        server_id = params.get("subscription")
        client_id = self._client_by_server.get(server_id) if isinstance(server_id, int) else None
        if server_id is not None and client_id is None:
            return None
        result = params.get("result")
        if method == "logsNotification" and client_id is not None and isinstance(result, dict):
            value, context = result.get("value"), result.get("context")
            if isinstance(value, dict) and isinstance(context, dict):
                try:
                    return LogsNotification.model_validate({
                        "subscription": client_id,
                        "slot": context.get("slot"),
                        "signature": value.get("signature"),
                        "err": value.get("err"),
                        "logs": value.get("logs") or [],
                    })
                except ValidationError:
                    pass  # not the shape documented: yielded as it came
        return HeliusWebSocketNotification(method = method, subscription = client_id, result = result)

    async def _request(
        self,
        method: str,
        params: list[Any],
        on_result: Callable[[Any], None] | None = None,
        on_late: Callable[[Any], None] | None = None,
        wait: bool = True,
    ) -> Any:
        """
        Send a JSON-RPC request and wait for its answer.

        Parameters:
            method: the method, e.g. `logsSubscribe`.
            params: its params.
            on_result: called with the result as the answer is read, before the next
                message; a `TypeError` or `ValueError` it raises fails the request.
            on_late: called with the result of an answer that comes after the request
                timed out, on the same connection.
            wait: with `reconnect` on, wait for a dropped connection to come back
                rather than failing at once. Only the caller's own requests wait: the
                client's, sent while it reconnects, must not wait for itself.

        Returns:
            the answer's result.

        Raises:
            HeliusRPCError: the node answered with an error.
            HeliusWebSocketClosed: the client is closed, or the connection dropped
                before the answer, or did not come back within `request_timeout`.
            HeliusWebSocketTimeout: no answer within `request_timeout`.
        """
        if self._closing or self._stopped.is_set():
            raise HeliusWebSocketClosed(self._stop_reason)
        if self._session is None:
            raise HeliusWebSocketClosed("the client is not connected: call `connect` first")
        if not self.connected:
            if not (self._reconnect and wait):
                raise HeliusWebSocketClosed("the connection was dropped")
            await self._wait_for_connection(method)
        ws = self._ws
        assert ws is not None
        self._next_request_id += 1
        request_id = self._next_request_id
        future: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[request_id] = _Pending(future, on_result, on_late)
        failure: HeliusWebSocketError
        try:
            await ws.send_str(json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}))
            result = await asyncio.wait_for(future, timeout = self._request_timeout)
        except (aiohttp.ClientError, ConnectionError) as error:
            self._pending.pop(request_id, None)
            failure = HeliusWebSocketClosed(f"{method}: {redact(str(error)) or type(error).__name__}")
        except asyncio.TimeoutError:
            if on_late is None:
                self._pending.pop(request_id, None)
            failure = HeliusWebSocketTimeout(f"{method}: no answer within {self._request_timeout} s")
        except BaseException:
            self._pending.pop(request_id, None)
            raise
        else:
            return result
        # Raised outside the `except` block, so that the aiohttp error, which may carry
        # the URL, is not chained as its context.
        raise failure

    async def _wait_for_connection(self, method: str) -> None:
        """
        Wait for a dropped connection to come back.

        Parameters:
            method: the method of the request waiting, for the error message.

        Raises:
            HeliusWebSocketClosed: the client was closed meanwhile, or the connection
                did not come back within `request_timeout`.
        """
        waiters = [
            asyncio.ensure_future(self._connected.wait()),
            asyncio.ensure_future(self._stopped.wait()),
        ]
        try:
            await asyncio.wait(waiters, timeout = self._request_timeout, return_when = asyncio.FIRST_COMPLETED)
        finally:
            for waiter in waiters:
                waiter.cancel()
        if self._closing or self._stopped.is_set():
            raise HeliusWebSocketClosed(self._stop_reason)
        if not self.connected:
            raise HeliusWebSocketClosed(f"{method}: not reconnected within {self._request_timeout} s")

    def _fail_pending(self, error: HeliusWebSocketClosed) -> None:
        """
        Fail every request waiting for its answer; their connection is gone.

        Parameters:
            error: the error each one raises.
        """
        pending, self._pending = self._pending, {}
        for entry in pending.values():
            if not entry.future.done():
                entry.future.set_exception(error)

    def _spawn(self, coroutine: Coroutine[Any, Any, None], name: str) -> None:
        """
        Run a coroutine in a task the client cancels on `close`.

        Parameters:
            coroutine: what to run.
            name: the task's name.
        """
        task = asyncio.create_task(coroutine, name = name)
        self._background.add(task)
        task.add_done_callback(self._background.discard)


def _subscription_id(result: Any) -> int:
    """
    The node's subscription id in a subscribe answer.

    Parameters:
        result: the answer's result.

    Returns:
        the id.

    Raises:
        ValueError: the result is not an integer id.
    """
    if not isinstance(result, int) or isinstance(result, bool):
        raise ValueError(f"not a subscription id: {result!r}")
    return result
