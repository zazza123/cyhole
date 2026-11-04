# WebSocket

The WebSocket client pushes what happens on chain as it happens, where the HTTP endpoints have to be polled.
It serves the standard Solana subscriptions, which Helius offers on every plan, the free one included.

| Topic | Behaviour |
| --- | --- |
| Billing | Helius meters the data streamed (2 credits per 0.1 MB at the time of writing) and 1 credit for each connection opened, reconnections included. |
| Keep-alive | Helius closes a connection after 10 minutes without traffic and expects a ping at least once a minute. The client pings every `heartbeat` seconds (30 by default), on a busy connection too, and treats a pong missing for half that time as a dropped connection. |
| Reconnection | Opt-in with `reconnect = True`. At the drop the client yields a `HeliusWebSocketDisconnected` marker; it then reopens the connection, sends the subscriptions again under the same ids, and yields a `HeliusWebSocketReconnected` marker, before any notification of the new connection. Notifications pushed while it was down are lost; the marker is the cue to catch up by polling. |
| Reconnection waits | They start at `reconnect_min_delay`, double up to `reconnect_max_delay`, and are drawn between half and all of their value. A connection that drops again within a minute keeps the wait growing, so a node that accepts and closes every connection costs at most one connection (1 credit) per `reconnect_max_delay`; after one that lasted longer the first attempt is immediate. |
| Failed resubscriptions | A subscription the node refuses for good (an invalid parameter) is dropped and listed in the marker's `dropped`. Any other failure, such as a timeout, makes the client reconnect and try again. |
| Errors | A message of unexpected shape is logged and dropped. An unexpected error inside the client ends the iteration with `HeliusWebSocketError`. A request with no answer in time raises `HeliusWebSocketTimeout`; if the node later confirms a subscription nobody waits for, the client ends it. |
| API key | It is part of the URL. Every error the client raises or logs masks it, and the client's `repr` does not show the URL. |
| Not covered | Helius' enhanced subscriptions (`transactionSubscribe`) require a paid plan and are not part of this client. |

::: cyhole.helius.websocket
