"""Schemas of the messages yielded by the Helius WebSocket client."""

from typing import Any

from pydantic import BaseModel


class LogsNotification(BaseModel):
    """
    A transaction that mentions the subscribed address, as pushed by `logsSubscribe`.

    Helius sends one notification per transaction, as soon as it reaches the
    subscription's commitment. It carries the transaction's signature and logs,
    not the transaction itself: read it with `getTransaction` when its content
    is needed.

    Attributes:
        subscription: the id `logs_subscribe` returned for this subscription. It stays
            the same across reconnections of the client.
        slot: slot in which the transaction was processed.
        signature: signature of the transaction, base-58 encoded.
        err: the transaction's error object, `None` if the transaction succeeded.
        logs: log messages the transaction produced; empty if the node gave none
            (for example when the transaction failed before executing).
    """
    subscription: int
    slot: int
    signature: str
    err: Any = None
    logs: list[str] = []


class HeliusWebSocketNotification(BaseModel):
    """
    A notification of a method the client does not map to a dedicated schema.

    It is yielded as it came, rather than dropped, so that a newer notification
    type is not lost silently.

    Attributes:
        method: the notification's method name, e.g. `slotNotification`.
        subscription: the id of the subscription it belongs to, mapped to the id the
            client returned; `None` if the notification carries none.
        result: the `result` member of the notification's `params`, unchanged.
    """
    method: str
    subscription: int | None = None
    result: Any = None


class HeliusWebSocketDisconnected(BaseModel):
    """
    Marker yielded when the connection drops and the client starts reconnecting.

    From here until the next
    [`HeliusWebSocketReconnected`][cyhole.helius.schema.HeliusWebSocketReconnected]
    no notification arrives: a caller that relies on them can switch to polling
    meanwhile. It is yielded once per outage, however many attempts the
    reconnection takes.

    Attributes:
        close_code: the WebSocket close code of the dropped connection, `None` if it
            ended without a close frame (a network failure, a missing pong).
    """
    close_code: int | None = None


class HeliusWebSocketReconnected(BaseModel):
    """
    Marker yielded after the client reopened a dropped connection and sent its
    subscriptions again.

    Notifications pushed while the connection was down are lost: the marker is
    the caller's cue to catch up by other means, for example one call of
    `getSignaturesForAddress` per subscribed address. Every notification of the
    new connection is yielded after the marker, so the gap lies between the
    last notification before the marker and the first one after it.

    Attributes:
        attempts: connection attempts it took, the successful one included, counted
            from the drop even when the connection dropped again while the
            subscriptions were being sent.
        downtime_s: seconds between the drop and the moment the subscriptions were
            active again.
        subscriptions: ids of the subscriptions sent again and active.
        dropped: ids of the subscriptions the node refused for good (an invalid
            parameter, for example), which the client has forgotten. A failure that
            may pass, such as a timeout or an internal error, does not drop a
            subscription: the client reconnects and tries again.
    """
    attempts: int
    downtime_s: float
    subscriptions: list[int]
    dropped: list[int] = []
