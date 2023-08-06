import asyncio

import websockets

from . import antlr
from . import events
from .irc_visitor import ChatVisitor


class TwitchWSIRCClient:
    __websocket: websockets.WebSocketClientProtocol = None
    __queue: asyncio.Queue = None
    __produce = None
    __consume = None

    def __init__(self, token: str, name: str, channel: str, log: bool = False, debug: bool = False):
        self.uri = 'wss://irc-ws.chat.twitch.tv:443'
        self.token = token
        self.name = name
        self.channel = channel
        if log:
            self.log = open('log.txt', 'w')
        else:
            self.log = None
        self.debug = debug

    async def start(self, event_handler: events.EventHandler):
        self.__websocket = await websockets.connect(self.uri)
        await self.__send(f"PASS oauth:{self.token}")
        await self.__send(f"NICK {self.name}")
        print(await self.__websocket.recv())
        await self.__send('CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership')
        await self.__send(f"JOIN #{self.channel}")
        self.__queue = asyncio.Queue()
        self.__produce = asyncio.create_task(self.__producer(self.__queue))
        self.__consume = asyncio.create_task(self.__consumer(event_handler, self.__queue))

    async def send_message(self, message: str):
        return await self.__send(f"PRIVMSG #{self.channel} :{message}")

    async def stop(self):
        if self.debug:
            print('stopping')
        await self.__websocket.close()
        await self.join()
        if self.log:
            self.log.close()
        if self.debug:
            print('stopped')

    async def join(self):
        await asyncio.gather(self.__produce)
        await self.__queue.join()
        self.__consume.cancel()

    async def __producer(self, queue: asyncio.Queue):
        async for messages in self.__websocket:
            for message in messages.splitlines():
                message = message.strip('\r\n')
                if self.log:
                    self.log.write(f"{message}\n")
                if self.debug:
                    print(f"> {message}")
                tree, successful_parse = antlr.parse(message)
                if successful_parse:
                    event = ChatVisitor(message, self.__websocket, self.channel).visit(tree)
                    if event:
                        await queue.put(event)

    async def __consumer(self, event_handler: events.EventHandler, queue: asyncio.Queue):
        while queue:
            event = await queue.get()
            if event:
                await event._accept(event_handler)
                queue.task_done()

    async def __send(self, message: str):
        if self.debug:
            print(f"< {message}")
        return await self.__websocket.send(message)
