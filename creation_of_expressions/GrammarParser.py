# Generated from Grammar.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,36,98,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,71,8,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,91,8,1,10,
        1,12,1,94,9,1,1,2,1,2,1,2,0,1,2,3,0,2,4,0,9,1,0,4,7,1,0,9,10,1,0,
        11,12,1,0,14,16,1,0,19,20,1,0,17,18,1,0,21,22,1,0,25,30,1,0,33,35,
        110,0,6,1,0,0,0,2,70,1,0,0,0,4,95,1,0,0,0,6,7,3,2,1,0,7,1,1,0,0,
        0,8,9,6,1,-1,0,9,10,5,1,0,0,10,11,3,2,1,0,11,12,5,2,0,0,12,71,1,
        0,0,0,13,14,5,3,0,0,14,71,3,2,1,16,15,16,7,0,0,0,16,17,5,1,0,0,17,
        18,3,2,1,0,18,19,5,8,0,0,19,20,3,2,1,0,20,21,5,2,0,0,21,71,1,0,0,
        0,22,23,7,1,0,0,23,24,5,1,0,0,24,25,3,2,1,0,25,26,5,8,0,0,26,27,
        3,2,1,0,27,28,5,8,0,0,28,29,3,2,1,0,29,30,5,8,0,0,30,31,3,2,1,0,
        31,32,5,8,0,0,32,33,3,2,1,0,33,34,5,2,0,0,34,71,1,0,0,0,35,36,7,
        2,0,0,36,37,5,1,0,0,37,38,3,2,1,0,38,39,5,8,0,0,39,40,3,2,1,0,40,
        41,5,2,0,0,41,71,1,0,0,0,42,43,7,3,0,0,43,44,5,1,0,0,44,45,3,2,1,
        0,45,46,5,2,0,0,46,71,1,0,0,0,47,48,7,4,0,0,48,71,3,2,1,8,49,50,
        5,23,0,0,50,71,3,2,1,6,51,52,5,31,0,0,52,53,3,2,1,0,53,54,5,8,0,
        0,54,55,3,2,1,0,55,56,5,8,0,0,56,57,3,2,1,0,57,58,5,2,0,0,58,71,
        1,0,0,0,59,60,5,32,0,0,60,61,3,2,1,0,61,62,5,8,0,0,62,63,3,2,1,0,
        63,64,5,8,0,0,64,65,3,2,1,0,65,66,5,8,0,0,66,67,3,2,1,0,67,68,5,
        2,0,0,68,71,1,0,0,0,69,71,3,4,2,0,70,8,1,0,0,0,70,13,1,0,0,0,70,
        15,1,0,0,0,70,22,1,0,0,0,70,35,1,0,0,0,70,42,1,0,0,0,70,47,1,0,0,
        0,70,49,1,0,0,0,70,51,1,0,0,0,70,59,1,0,0,0,70,69,1,0,0,0,71,92,
        1,0,0,0,72,73,10,12,0,0,73,74,5,13,0,0,74,91,3,2,1,13,75,76,10,10,
        0,0,76,77,7,5,0,0,77,91,3,2,1,11,78,79,10,9,0,0,79,80,7,4,0,0,80,
        91,3,2,1,10,81,82,10,7,0,0,82,83,7,6,0,0,83,91,3,2,1,8,84,85,10,
        5,0,0,85,86,5,24,0,0,86,91,3,2,1,6,87,88,10,4,0,0,88,89,7,7,0,0,
        89,91,3,2,1,5,90,72,1,0,0,0,90,75,1,0,0,0,90,78,1,0,0,0,90,81,1,
        0,0,0,90,84,1,0,0,0,90,87,1,0,0,0,91,94,1,0,0,0,92,90,1,0,0,0,92,
        93,1,0,0,0,93,3,1,0,0,0,94,92,1,0,0,0,95,96,7,8,0,0,96,5,1,0,0,0,
        3,70,90,92
    ]

class GrammarParser ( Parser ):

    grammarFileName = "Grammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'#'", "'TrendSecond'", 
                     "'Trend'", "'Avg'", "'Median'", "','", "'Integral'", 
                     "'IntegralLebesgue'", "'Round'", "'Str'", "'^'", "'sqr2'", 
                     "'sqr3'", "'Abs'", "'*'", "'/'", "'+'", "'-'", "'AND'", 
                     "'OR'", "'NOT'", "'_'", "'>'", "'>='", "'<'", "'<='", 
                     "'='", "'!='", "'If('", "'Advisory('" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "DECIMAL", "BOOL", "STR", "WS" ]

    RULE_start = 0
    RULE_expr = 1
    RULE_atom = 2

    ruleNames =  [ "start", "expr", "atom" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    T__24=25
    T__25=26
    T__26=27
    T__27=28
    T__28=29
    T__29=30
    T__30=31
    T__31=32
    DECIMAL=33
    BOOL=34
    STR=35
    WS=36

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def getRuleIndex(self):
            return GrammarParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = GrammarParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GrammarParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AdvisoryExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.check = None # ExprContext
            self.code = None # ExprContext
            self.level = None # ExprContext
            self.text = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdvisoryExpr" ):
                listener.enterAdvisoryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdvisoryExpr" ):
                listener.exitAdvisoryExpr(self)


    class ParamExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.param = None # ExprContext
            self.time = None # ExprContext
            self.reference = None # ExprContext
            self.below = None # ExprContext
            self.exponent = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamExpr" ):
                listener.enterParamExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamExpr" ):
                listener.exitParamExpr(self)


    class MathExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMathExpr" ):
                listener.enterMathExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMathExpr" ):
                listener.exitMathExpr(self)


    class IfExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.check = None # ExprContext
            self.isTrue = None # ExprContext
            self.isFalse = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfExpr" ):
                listener.enterIfExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfExpr" ):
                listener.exitIfExpr(self)


    class AtomExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(GrammarParser.AtomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtomExpr" ):
                listener.enterAtomExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtomExpr" ):
                listener.exitAtomExpr(self)


    class BoolExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolExpr" ):
                listener.enterBoolExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolExpr" ):
                listener.exitBoolExpr(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(GrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)


    class RoundExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.value = None # ExprContext
            self.decimals = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoundExpr" ):
                listener.enterRoundExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoundExpr" ):
                listener.exitRoundExpr(self)


    class ConcatExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConcatExpr" ):
                listener.enterConcatExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConcatExpr" ):
                listener.exitConcatExpr(self)


    class ComparExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GrammarParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(GrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparExpr" ):
                listener.enterComparExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparExpr" ):
                listener.exitComparExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = GrammarParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = GrammarParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 9
                self.match(GrammarParser.T__0)
                self.state = 10
                self.expr(0)
                self.state = 11
                self.match(GrammarParser.T__1)
                pass
            elif token in [3]:
                localctx = GrammarParser.ParamExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 13
                localctx.op = self.match(GrammarParser.T__2)
                self.state = 14
                localctx.param = self.expr(16)
                pass
            elif token in [4, 5, 6, 7]:
                localctx = GrammarParser.ParamExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 15
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 240) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 16
                self.match(GrammarParser.T__0)
                self.state = 17
                localctx.param = self.expr(0)
                self.state = 18
                self.match(GrammarParser.T__7)
                self.state = 19
                localctx.time = self.expr(0)
                self.state = 20
                self.match(GrammarParser.T__1)
                pass
            elif token in [9, 10]:
                localctx = GrammarParser.ParamExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 22
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==9 or _la==10):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 23
                self.match(GrammarParser.T__0)
                self.state = 24
                localctx.param = self.expr(0)
                self.state = 25
                self.match(GrammarParser.T__7)
                self.state = 26
                localctx.time = self.expr(0)
                self.state = 27
                self.match(GrammarParser.T__7)
                self.state = 28
                localctx.reference = self.expr(0)
                self.state = 29
                self.match(GrammarParser.T__7)
                self.state = 30
                localctx.below = self.expr(0)
                self.state = 31
                self.match(GrammarParser.T__7)
                self.state = 32
                localctx.exponent = self.expr(0)
                self.state = 33
                self.match(GrammarParser.T__1)
                pass
            elif token in [11, 12]:
                localctx = GrammarParser.RoundExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 35
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==11 or _la==12):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 36
                self.match(GrammarParser.T__0)
                self.state = 37
                localctx.value = self.expr(0)
                self.state = 38
                self.match(GrammarParser.T__7)
                self.state = 39
                localctx.decimals = self.expr(0)
                self.state = 40
                self.match(GrammarParser.T__1)
                pass
            elif token in [14, 15, 16]:
                localctx = GrammarParser.MathExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 42
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 114688) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 43
                self.match(GrammarParser.T__0)
                self.state = 44
                localctx.right = self.expr(0)
                self.state = 45
                self.match(GrammarParser.T__1)
                pass
            elif token in [19, 20]:
                localctx = GrammarParser.MathExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 47
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==19 or _la==20):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 48
                localctx.right = self.expr(8)
                pass
            elif token in [23]:
                localctx = GrammarParser.BoolExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 49
                localctx.op = self.match(GrammarParser.T__22)
                self.state = 50
                localctx.right = self.expr(6)
                pass
            elif token in [31]:
                localctx = GrammarParser.IfExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 51
                self.match(GrammarParser.T__30)
                self.state = 52
                localctx.check = self.expr(0)
                self.state = 53
                self.match(GrammarParser.T__7)
                self.state = 54
                localctx.isTrue = self.expr(0)
                self.state = 55
                self.match(GrammarParser.T__7)
                self.state = 56
                localctx.isFalse = self.expr(0)
                self.state = 57
                self.match(GrammarParser.T__1)
                pass
            elif token in [32]:
                localctx = GrammarParser.AdvisoryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 59
                self.match(GrammarParser.T__31)
                self.state = 60
                localctx.check = self.expr(0)
                self.state = 61
                self.match(GrammarParser.T__7)
                self.state = 62
                localctx.code = self.expr(0)
                self.state = 63
                self.match(GrammarParser.T__7)
                self.state = 64
                localctx.level = self.expr(0)
                self.state = 65
                self.match(GrammarParser.T__7)
                self.state = 66
                localctx.text = self.expr(0)
                self.state = 67
                self.match(GrammarParser.T__1)
                pass
            elif token in [33, 34, 35]:
                localctx = GrammarParser.AtomExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 69
                self.atom()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 92
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 90
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = GrammarParser.MathExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 72
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 73
                        localctx.op = self.match(GrammarParser.T__12)
                        self.state = 74
                        localctx.right = self.expr(13)
                        pass

                    elif la_ == 2:
                        localctx = GrammarParser.MathExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 75
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 76
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==17 or _la==18):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 77
                        localctx.right = self.expr(11)
                        pass

                    elif la_ == 3:
                        localctx = GrammarParser.MathExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 78
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 79
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==19 or _la==20):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 80
                        localctx.right = self.expr(10)
                        pass

                    elif la_ == 4:
                        localctx = GrammarParser.BoolExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 81
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 82
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==21 or _la==22):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 83
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 5:
                        localctx = GrammarParser.ConcatExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 84
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 85
                        localctx.op = self.match(GrammarParser.T__23)
                        self.state = 86
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 6:
                        localctx = GrammarParser.ComparExprContext(self, GrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 87
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 88
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2113929216) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 89
                        localctx.right = self.expr(5)
                        pass

             
                self.state = 94
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DECIMAL(self):
            return self.getToken(GrammarParser.DECIMAL, 0)

        def BOOL(self):
            return self.getToken(GrammarParser.BOOL, 0)

        def STR(self):
            return self.getToken(GrammarParser.STR, 0)

        def getRuleIndex(self):
            return GrammarParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)




    def atom(self):

        localctx = GrammarParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 60129542144) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 4)
         




