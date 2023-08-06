# Generated from IRC.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .IRCParser import IRCParser
else:
    from IRCParser import IRCParser

# This class defines a complete listener for a parse tree produced by IRCParser.
class IRCListener(ParseTreeListener):

    # Enter a parse tree produced by IRCParser#message.
    def enterMessage(self, ctx:IRCParser.MessageContext):
        pass

    # Exit a parse tree produced by IRCParser#message.
    def exitMessage(self, ctx:IRCParser.MessageContext):
        pass


    # Enter a parse tree produced by IRCParser#ping.
    def enterPing(self, ctx:IRCParser.PingContext):
        pass

    # Exit a parse tree produced by IRCParser#ping.
    def exitPing(self, ctx:IRCParser.PingContext):
        pass


    # Enter a parse tree produced by IRCParser#privmsg.
    def enterPrivmsg(self, ctx:IRCParser.PrivmsgContext):
        pass

    # Exit a parse tree produced by IRCParser#privmsg.
    def exitPrivmsg(self, ctx:IRCParser.PrivmsgContext):
        pass


    # Enter a parse tree produced by IRCParser#join.
    def enterJoin(self, ctx:IRCParser.JoinContext):
        pass

    # Exit a parse tree produced by IRCParser#join.
    def exitJoin(self, ctx:IRCParser.JoinContext):
        pass


    # Enter a parse tree produced by IRCParser#part.
    def enterPart(self, ctx:IRCParser.PartContext):
        pass

    # Exit a parse tree produced by IRCParser#part.
    def exitPart(self, ctx:IRCParser.PartContext):
        pass


    # Enter a parse tree produced by IRCParser#cap_ack.
    def enterCap_ack(self, ctx:IRCParser.Cap_ackContext):
        pass

    # Exit a parse tree produced by IRCParser#cap_ack.
    def exitCap_ack(self, ctx:IRCParser.Cap_ackContext):
        pass


    # Enter a parse tree produced by IRCParser#names_reply.
    def enterNames_reply(self, ctx:IRCParser.Names_replyContext):
        pass

    # Exit a parse tree produced by IRCParser#names_reply.
    def exitNames_reply(self, ctx:IRCParser.Names_replyContext):
        pass


    # Enter a parse tree produced by IRCParser#names_reply_end.
    def enterNames_reply_end(self, ctx:IRCParser.Names_reply_endContext):
        pass

    # Exit a parse tree produced by IRCParser#names_reply_end.
    def exitNames_reply_end(self, ctx:IRCParser.Names_reply_endContext):
        pass


    # Enter a parse tree produced by IRCParser#userstate.
    def enterUserstate(self, ctx:IRCParser.UserstateContext):
        pass

    # Exit a parse tree produced by IRCParser#userstate.
    def exitUserstate(self, ctx:IRCParser.UserstateContext):
        pass


    # Enter a parse tree produced by IRCParser#roomstate.
    def enterRoomstate(self, ctx:IRCParser.RoomstateContext):
        pass

    # Exit a parse tree produced by IRCParser#roomstate.
    def exitRoomstate(self, ctx:IRCParser.RoomstateContext):
        pass


    # Enter a parse tree produced by IRCParser#hosttarget.
    def enterHosttarget(self, ctx:IRCParser.HosttargetContext):
        pass

    # Exit a parse tree produced by IRCParser#hosttarget.
    def exitHosttarget(self, ctx:IRCParser.HosttargetContext):
        pass


    # Enter a parse tree produced by IRCParser#notice.
    def enterNotice(self, ctx:IRCParser.NoticeContext):
        pass

    # Exit a parse tree produced by IRCParser#notice.
    def exitNotice(self, ctx:IRCParser.NoticeContext):
        pass


    # Enter a parse tree produced by IRCParser#sender.
    def enterSender(self, ctx:IRCParser.SenderContext):
        pass

    # Exit a parse tree produced by IRCParser#sender.
    def exitSender(self, ctx:IRCParser.SenderContext):
        pass


    # Enter a parse tree produced by IRCParser#sender_short.
    def enterSender_short(self, ctx:IRCParser.Sender_shortContext):
        pass

    # Exit a parse tree produced by IRCParser#sender_short.
    def exitSender_short(self, ctx:IRCParser.Sender_shortContext):
        pass


    # Enter a parse tree produced by IRCParser#channel.
    def enterChannel(self, ctx:IRCParser.ChannelContext):
        pass

    # Exit a parse tree produced by IRCParser#channel.
    def exitChannel(self, ctx:IRCParser.ChannelContext):
        pass


    # Enter a parse tree produced by IRCParser#key_value_list.
    def enterKey_value_list(self, ctx:IRCParser.Key_value_listContext):
        pass

    # Exit a parse tree produced by IRCParser#key_value_list.
    def exitKey_value_list(self, ctx:IRCParser.Key_value_listContext):
        pass


    # Enter a parse tree produced by IRCParser#key_value.
    def enterKey_value(self, ctx:IRCParser.Key_valueContext):
        pass

    # Exit a parse tree produced by IRCParser#key_value.
    def exitKey_value(self, ctx:IRCParser.Key_valueContext):
        pass


    # Enter a parse tree produced by IRCParser#word.
    def enterWord(self, ctx:IRCParser.WordContext):
        pass

    # Exit a parse tree produced by IRCParser#word.
    def exitWord(self, ctx:IRCParser.WordContext):
        pass


