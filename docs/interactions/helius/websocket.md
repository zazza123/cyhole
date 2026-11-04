# WebSocket

The WebSocket client pushes what happens on chain as it happens, where the HTTP endpoints have to be polled.
It serves the standard Solana subscriptions, which Helius offers on every plan, the free one included.

| Topic | Behaviour |
| --- | --- |
| Billing | Helius meters the data streamed (2 credits per 0.1 MB at the time of writing) and 1 credit for each connection opened, reconnections included. |
| Keep-alive | Helius closes a connection after 10 minutes without traffic; the client pings every `heartbeat` seconds (30 by default) and treats a missing pong as a dropped connection. |
| Reconnection | Opt-in with `reconnect = True`: the client reopens the connection with a doubling wait, sends the subscriptions again under the same ids, and yields a `HeliusWebSocketReconnected` marker. Notifications pushed while it was down are lost; the marker is the cue to catch up by polling. |
| API key | It is part of the URL. Every error the client raises or logs masks it, and the client's `repr` does not show the URL. |
| Not covered | Helius' enhanced subscriptions (`transactionSubscribe`) require a paid plan and are not part of this client. |

::: cyhole.helius.websocket
