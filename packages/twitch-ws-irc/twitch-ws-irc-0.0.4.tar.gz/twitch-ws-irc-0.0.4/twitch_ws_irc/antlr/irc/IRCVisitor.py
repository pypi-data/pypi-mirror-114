# Generated from IRC.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .IRCParser import IRCParser
else:
    from IRCParser import IRCParser

# This class defines a complete generic visitor for a parse tree produced by IRCParser.

class IRCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IRCParser#message.
    def visitMessage(self, ctx:IRCParser.MessageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#ping.
    def visitPing(self, ctx:IRCParser.PingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#privmsg.
    def visitPrivmsg(self, ctx:IRCParser.PrivmsgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#join.
    def visitJoin(self, ctx:IRCParser.JoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#part.
    def visitPart(self, ctx:IRCParser.PartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#cap_ack.
    def visitCap_ack(self, ctx:IRCParser.Cap_ackContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#names_reply.
    def visitNames_reply(self, ctx:IRCParser.Names_replyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#names_reply_end.
    def visitNames_reply_end(self, ctx:IRCParser.Names_reply_endContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#userstate.
    def visitUserstate(self, ctx:IRCParser.UserstateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#roomstate.
    def visitRoomstate(self, ctx:IRCParser.RoomstateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#hosttarget.
    def visitHosttarget(self, ctx:IRCParser.HosttargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#notice.
    def visitNotice(self, ctx:IRCParser.NoticeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#sender.
    def visitSender(self, ctx:IRCParser.SenderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#sender_short.
    def visitSender_short(self, ctx:IRCParser.Sender_shortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#channel.
    def visitChannel(self, ctx:IRCParser.ChannelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#key_value_list.
    def visitKey_value_list(self, ctx:IRCParser.Key_value_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#key_value.
    def visitKey_value(self, ctx:IRCParser.Key_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IRCParser#word.
    def visitWord(self, ctx:IRCParser.WordContext):
        return self.visitChildren(ctx)



del IRCParser