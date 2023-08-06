# Twitch WS IRC

## how to install
You can install the lib with pip from this repo directly.
```
pip install git+ssh://git@gitlab.com/henny022/twitch-ws-irc.git#egg=twitch-ws-irc
```

## how to use
proper examples will follow

- make an Event Handler
```python
from twitch_ws_irc.events import *

class ExampleEventHandler(EventHandler):
    async def on_privmsg(self, event: PrivMsgEvent):
        print(f"{event.user}: {event.message}")
        if event.message == '!test':
            await event.reply(f"hey {event.user}")
        if event.message == '!stop':
            await event.reply('bye')
            await event.websocket.close()
```

- start the bot
```python
from twitch_ws_irc.client import TwitchWSIRCClient

async def bot():
    client = TwitchWSIRCClient('twitch token', 'twitch username', 'target channel')
    await client.start(ExampleEventHandler())
    await client.join()

```