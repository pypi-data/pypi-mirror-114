import websockets
import time


class Event:
    def __init__(self, websocket: websockets.WebSocketClientProtocol, channel: str):
        self.websocket = websocket
        self.channel = channel

    async def reply(self, message: str):
        await self._reply_raw(f"PRIVMSG #{self.channel} :{message}")

    async def _reply_raw(self, message: str):
        await self.websocket.send(f"{message}")

    async def _accept(self, handler):
        pass


class PrivMsgEvent(Event):
    # TODO put all of these into a seperate object
    badge_info: str
    badges: str
    client_nonce: str
    color: str
    display_name: str
    emotes: str
    flags: str
    id: str
    mod: int
    room_id: str
    subscriber: int
    tmi_sent_ts: time.struct_time
    turbo: int
    user_id: str
    user_type: str

    def __init__(self, websocket: websockets.WebSocketClientProtocol, channel: str, user: str, message: str):
        super().__init__(websocket, channel)
        self.user = user
        self.message = message

    async def _accept(self, handler):
        await handler.on_privmsg(self)


class JoinEvent(Event):
    user: str
    channel: str

    def __init__(self, websocket: websockets.WebSocketClientProtocol, channel: str, user: str):
        super().__init__(websocket, channel)
        self.user = user

    async def _accept(self, handler):
        handler.on_join(self)


class PartEvent(Event):
    user: str
    channel: str

    def __init__(self, websocket: websockets.WebSocketClientProtocol, channel: str, user: str):
        super().__init__(websocket, channel)
        self.user = user

    async def _accept(self, handler):
        handler.on_part(self)


class _PingEvent(Event):
    async def reply(self, message: str):
        await self._reply_raw('PONG :tmi.twitch.tv')

    async def _accept(self, handler):
        await handler._on_ping(self)


class EventHandler:
    async def on_privmsg(self, event: PrivMsgEvent):
        pass

    async def on_join(self, event: JoinEvent):
        pass

    async def on_part(self, event: JoinEvent):
        pass

    async def _on_ping(self, event: _PingEvent):
        await event.reply('')
