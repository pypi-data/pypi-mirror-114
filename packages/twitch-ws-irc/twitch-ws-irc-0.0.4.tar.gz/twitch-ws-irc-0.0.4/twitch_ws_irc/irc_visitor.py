from . import events
from .antlr import IRCVisitor, IRCParser
import websockets
import time


class ChatVisitor(IRCVisitor):
    def __init__(self, message: str, websocket: websockets.WebSocketClientProtocol, channel: str):
        self.message = message
        self.websocket = websocket
        self.channel = channel

    def visitPrivmsg(self, ctx: IRCParser.PrivmsgContext):
        chat_message = self.message.replace(ctx.getText(), '')
        from_user = ctx.sender().username.text
        key_value_pairs = {
            pair.key.getText(): pair.value.getText() if pair.value is not None else ''
            for pair in ctx.key_value_list().key_value()
        }
        event = events.PrivMsgEvent(self.websocket, self.channel, from_user, chat_message)
        event.badge_info = key_value_pairs.get('badge-info', '')
        event.badges = key_value_pairs.get('badges', '')
        event.client_nonce = key_value_pairs.get('client-nonce', '')
        event.color = key_value_pairs.get('color', '')
        event.display_name = key_value_pairs.get('display-name', '')
        event.emotes = key_value_pairs.get('emotes', '')
        event.flags = key_value_pairs.get('flags', '')
        event.id = key_value_pairs.get('id', '')
        event.mod = int(key_value_pairs.get('mod', '0'))
        event.room_id = key_value_pairs.get('room-id', '')
        event.subscriber = int(key_value_pairs.get('subscriber', '0'))
        event.tmi_sent_ts = time.localtime(int(key_value_pairs.get('tmi-sent-ts', '0'))/1000)
        event.turbo = int(key_value_pairs.get('turbo', '0'))
        event.user_id = key_value_pairs.get('user-id', '')
        event.user_type = key_value_pairs.get('user-type', '')
        return event

    def visitPing(self, ctx: IRCParser.PingContext, *args, **kwargs):
        return events._PingEvent(self.websocket, self.channel)
