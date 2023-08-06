from .irc.IRCLexer import IRCLexer
from .irc.IRCParser import IRCParser
from .irc.IRCListener import IRCListener
from .irc.IRCVisitor import IRCVisitor

import antlr4.InputStream
import antlr4.CommonTokenStream


def parse(message: str) -> (IRCParser.MessageContext, bool):
    input = antlr4.InputStream(message)
    lexer = IRCLexer(input)
    tokens = antlr4.CommonTokenStream(lexer)
    parser = IRCParser(tokens)
    tree = parser.message()
    # TODO there probably is a better way of doing this
    was_successful = parser.getNumberOfSyntaxErrors() == 0
    return tree, was_successful
