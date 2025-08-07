# Generated from Grammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GrammarParser import GrammarParser
else:
    from GrammarParser import GrammarParser

# This class defines a complete listener for a parse tree produced by GrammarParser.
class GrammarListener(ParseTreeListener):

    # Enter a parse tree produced by GrammarParser#start.
    def enterStart(self, ctx:GrammarParser.StartContext):
        pass

    # Exit a parse tree produced by GrammarParser#start.
    def exitStart(self, ctx:GrammarParser.StartContext):
        pass


    # Enter a parse tree produced by GrammarParser#advisoryExpr.
    def enterAdvisoryExpr(self, ctx:GrammarParser.AdvisoryExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#advisoryExpr.
    def exitAdvisoryExpr(self, ctx:GrammarParser.AdvisoryExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#paramExpr.
    def enterParamExpr(self, ctx:GrammarParser.ParamExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#paramExpr.
    def exitParamExpr(self, ctx:GrammarParser.ParamExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#mathExpr.
    def enterMathExpr(self, ctx:GrammarParser.MathExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#mathExpr.
    def exitMathExpr(self, ctx:GrammarParser.MathExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#ifExpr.
    def enterIfExpr(self, ctx:GrammarParser.IfExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#ifExpr.
    def exitIfExpr(self, ctx:GrammarParser.IfExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#atomExpr.
    def enterAtomExpr(self, ctx:GrammarParser.AtomExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#atomExpr.
    def exitAtomExpr(self, ctx:GrammarParser.AtomExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#boolExpr.
    def enterBoolExpr(self, ctx:GrammarParser.BoolExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#boolExpr.
    def exitBoolExpr(self, ctx:GrammarParser.BoolExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#parenExpr.
    def enterParenExpr(self, ctx:GrammarParser.ParenExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#parenExpr.
    def exitParenExpr(self, ctx:GrammarParser.ParenExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#roundExpr.
    def enterRoundExpr(self, ctx:GrammarParser.RoundExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#roundExpr.
    def exitRoundExpr(self, ctx:GrammarParser.RoundExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#concatExpr.
    def enterConcatExpr(self, ctx:GrammarParser.ConcatExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#concatExpr.
    def exitConcatExpr(self, ctx:GrammarParser.ConcatExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#comparExpr.
    def enterComparExpr(self, ctx:GrammarParser.ComparExprContext):
        pass

    # Exit a parse tree produced by GrammarParser#comparExpr.
    def exitComparExpr(self, ctx:GrammarParser.ComparExprContext):
        pass


    # Enter a parse tree produced by GrammarParser#atom.
    def enterAtom(self, ctx:GrammarParser.AtomContext):
        pass

    # Exit a parse tree produced by GrammarParser#atom.
    def exitAtom(self, ctx:GrammarParser.AtomContext):
        pass



del GrammarParser