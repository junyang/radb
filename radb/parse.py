from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from radb.RALexer import RALexer
from radb.RAParser import RAParser as RAParserBase
from radb.RAParserVisitor import RAParserVisitor

import radb.parse
from radb import utils

import logging
logger = logging.getLogger('ra')

######################################################################

def fixLiteralNames():
    """Go through the base (ANTLR-generated) RAParser and produce a new
    list of more meaningful literal token names.
    """
    names = list()
    for i, (literal, symbolic) in enumerate(zip(RAParserBase.literalNames,
                                                RAParserBase.symbolicNames)):
        if symbolic == '<INVALID>' or literal != '<INVALID>':
            # the literal name is already fine here:
            name = literal
        elif i in (RAParserBase.WS, RAParserBase.COMMENT,
                   RAParserBase.STRING, RAParserBase.NUMBER, RAParserBase.ID):
            # there is no canonoical literal representation for these
            # tokens, so use their symbolic names:
            name = '<{}>'.format(symbolic)
        else:
            # a canonoical literal representation can derived as
            # follows because of the conventions followed by
            # RALexer.g4:
            name = "'{}'".format(symbolic.lower().replace('_', ' '))
        names.append(name)
    return names

class RAParser(RAParserBase):
    """A subclass overriding the base (ANTLR-generated) RAParser's
    literalNames class attribute to provide more meaningful literal
    token names.

    When a token has multiple possible literal representations (e.g.,
    RAParser.NOT can be 'not' or 'NOT'), ANTLR4 assign '<INVALID>' as
    its literal name, which is very misleading in error-reporting.
    Thus, we fix RAParser.literalNames here (while we are at it, we
    also makes it possible to recover the canonical literal
    representation if there is one (e.g., RAParser.IS_NOT_NULL would
    be 'is not null').
    """
    literalNames = fixLiteralNames()

def literal(i):
    return RAParser.literalNames[i][1:-1] # to strip the surrounding quotes

def symbolic(i):
    return RAParser.symbolicNames[i]

def sqlstr_to_str(ss):
    return ss[1:-1].replace("''", "'")

def str_to_sqlstr(s):
    return "'" + s.replace("'", "''") + "'"

######################################################################

class ParsingError(Exception):
    pass

class RAErrorListener(ErrorListener):
    def __init__(self):
        super(RAErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParsingError('line {}:{} {}'.format(line, column, msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise ParsingError('ambiguity: {}'.format(configs))

    def reportAttemptingFullContext(self, recognizer,
                                    dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise ParsingError('attempting full context: {}'.format(configs))

    def reportContextSensitivity(self, recognizer,
                                 dfa, startIndex, stopIndex, prediction, configs):
        raise ParsingError('context sensitivity: {}'.format(configs))

######################################################################

class ASTBuilder(RAParserVisitor):

    def visitStringLiteralValExpr(self, ctx):
        return radb.ast.RAString(ctx.STRING().getText())

    def visitNumberLiteralValExpr(self, ctx):
        return radb.ast.RANumber(ctx.NUMBER().getText())

    def visitValExprParenthesized(self, ctx):
        return self.visit(ctx.valExpr())

    def visitFuncExpr(self, ctx):
        return radb.ast.FuncValExpr(ctx.ID().getText(),
                                    list() if ctx.listOfValExprs() is None else\
                                    self.visit(ctx.listOfValExprs()))

    def visitAttrRef(self, ctx):
        if ctx.getChildCount() == 1:
            return radb.ast.AttrRef(None, ctx.ID(0).getText())
        else:
            return radb.ast.AttrRef(ctx.ID(0).getText(), ctx.ID(1).getText())

    def visitValExprBinaryOp(self, ctx):
        left = self.visit(ctx.valExpr(0))
        op = ctx.getChild(1).symbol.type
        right = self.visit(ctx.valExpr(1))
        return radb.ast.ValExprBinaryOp(left, op, right)

    def visitValExprUnaryOp(self, ctx, op_idx=0):
        op = ctx.getChild(op_idx).symbol.type
        input = self.visit(ctx.valExpr())
        return radb.ast.ValExprUnaryOp(op, input)

    def visitMultDivExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitPlusMinusExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitConcatExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitCompareExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitLikeExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitIsNullExpr(self, ctx):
        return self.visitValExprUnaryOp(ctx, op_idx=1)

    def visitIsNotNullExpr(self, ctx):
        return self.visitValExprUnaryOp(ctx, op_idx=1)

    def visitNotExpr(self, ctx):
        return self.visitValExprUnaryOp(ctx)

    def visitAndExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitOrExpr(self, ctx):
        return self.visitValExprBinaryOp(ctx)

    def visitListOfValExprs(self, ctx):
        valExprs = list() if ctx.listOfValExprs() is None else self.visit(ctx.listOfValExprs())
        valExprs.insert(0, self.visit(ctx.valExpr()))
        return valExprs

    def visitListOfIDs(self, ctx):
        ids = list() if ctx.listOfIDs() is None else self.visit(ctx.listOfIDs())
        ids.insert(0, ctx.ID().getText())
        return ids

    def visitRelExprParenthesized(self, ctx):
        return self.visit(ctx.relExpr())

    def visitRelRef(self, ctx):
        return radb.ast.RelRef(ctx.ID().getText())

    def visitRenameExpr(self, ctx):
        return radb.ast.Rename(None if ctx.ID() is None else ctx.ID().getText(),
                               None if ctx.listOfIDs() is None else self.visit(ctx.listOfIDs()),
                               self.visit(ctx.relExpr()))

    def visitProjectExpr(self, ctx):
        return radb.ast.Project(self.visit(ctx.listOfValExprs()), self.visit(ctx.relExpr()))

    def visitSelectExpr(self, ctx):
        return radb.ast.Select(self.visit(ctx.valExpr()), self.visit(ctx.relExpr()))

    def visitCrossExpr(self, ctx):
        left = self.visit(ctx.relExpr(0))
        right = self.visit(ctx.relExpr(1))
        return radb.ast.Cross(left, right)

    def visitJoinExpr(self, ctx):
        left = self.visit(ctx.relExpr(0))
        cond = None if ctx.valExpr() is None else self.visit(ctx.valExpr())
        right = self.visit(ctx.relExpr(1))
        return radb.ast.Join(left, cond, right)

    def visitCrossExpr(self, ctx):
        left = self.visit(ctx.relExpr(0))
        right = self.visit(ctx.relExpr(1))
        return radb.ast.Cross(left, right)

    def visitUnionExpr(self, ctx):
        left = self.visit(ctx.relExpr(0))
        right = self.visit(ctx.relExpr(1))
        return radb.ast.Union(left, right)

    def visitDiffExpr(self, ctx):
        left = self.visit(ctx.relExpr(0))
        right = self.visit(ctx.relExpr(1))
        return radb.ast.Diff(left, right)

    def visitIntersectExpr(self, ctx):
        left = self.visit(ctx.relExpr(0))
        right = self.visit(ctx.relExpr(1))
        return radb.ast.Intersect(left, right)

    def visitDefinition(self, ctx):
        return radb.ast.Define(ctx.ID().getText(), self.visit(ctx.relExpr()))

    def visitListCommand(self, ctx):
        return radb.ast.Command(RAParser.LIST)

    def visitQuitCommand(self, ctx):
        return radb.ast.Command(RAParser.QUIT)

    def visitClearCommand(self, ctx):
        return radb.ast.CommandClear(view=(None if ctx.ID() is None else ctx.ID().getText()),
                                     force=(ctx.FORCE() is not None))

    def visitSaveCommand(self, ctx):
        return radb.ast.CommandSave(force=(ctx.FORCE() is not None),
                                    view=(None if ctx.ID() is None else ctx.ID().getText()),
                                    filename=(None if ctx.STRING() is None else\
                                              ctx.STRING().getText()))

    def visitSourceCommand(self, ctx):
        return radb.ast.CommandSource(ctx.STRING().getText())

    def visitSqlexecCommand(self, ctx):
        s = ctx.SQLEXEC_TEXT().getText().strip()
        s = utils.lreplace(s, literal(RAParser.ARG_L), '')
        s = utils.rreplace(s, literal(RAParser.ARG_R), '')
        return radb.ast.CommandSqlexec(s)

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitProgram(self, ctx):
        return [ self.visit(statement) for statement in ctx.statement() ]

######################################################################

def one_statement_from_string(s):
    lexer = RALexer(InputStream(s))
    lexer._listeners = [RAErrorListener()]
    parser = RAParser(CommonTokenStream(lexer))
    parser._listeners = [RAErrorListener()]
    tree = parser.statement()
    # from antlr4.tree.Trees import Trees
    # print(Trees.toStringTree(tree, None, parser))
    ast = ASTBuilder().visit(tree)
    return ast

def statements_from_file(filename):
    lexer = RALexer(FileStream(filename))
    lexer._listeners = [RAErrorListener()]
    parser = RAParser(CommonTokenStream(lexer))
    parser._listeners = [RAErrorListener()]
    tree = parser.program()
    asts = ASTBuilder().visit(tree)
    return asts

######################################################################

def statement_state_transition(state, line, i):
    char = line[i]
    char2 = line[i:i+2]
    if state == 'normal' or state is None:
        if char == literal(RAParser.TERMINATOR):
            state = None
            if i+1 < len(line):
                line = line[0:i+1] # ignore rest of line
                logger.warning('rest of the line after "{}" (character {}) ignored'\
                               .format(literal(RAParser.TERMINATOR), i+1))
        elif char == "'":
            state = 'in_string'
        elif char2 == '//':
            i = len(line)-1 # effectively ignore rest of line
        elif char2 == '/*':
            state = 'in_comment'
            i += 1 # skip an extra char
        else:
            state = 'normal'
    elif state == 'in_string':
        if char2 == "''":
            i += 1 # skip an extra char
        elif char == "'":
            state = 'normal'
        else:
            pass
    elif state == 'in_comment':
        if char2 == '*/':
            state = 'normal'
            i += 1 # skip an extra char
        else:
            pass
    else:
        assert False
    return state, line, i+1

def is_input_buffer_empty(input_buffer):
    return all(line == '' or line.isspace() for line in input_buffer)

def statement_string_from_stdin(echo=False):
    prompts = { None: 'ra> ',
                'normal' : '..> ',
                'in_string' : '.s> ',
                'in_comment' : '.c> ' }
    states = set(prompts.keys())
    state = None
    input_buffer = list()
    try:
        while True:
            line = input(prompts[state])
            if echo:
                print(line)
            i = 0
            while i < len(line):
                state, line, i = statement_state_transition(state, line, i)
            input_buffer.append(line)
            if state is None:
                if not is_input_buffer_empty(input_buffer):
                    yield '\n'.join(input_buffer)
                input_buffer = list()
    except EOFError:
        if not is_input_buffer_empty(input_buffer):
            # treat as if a teminator has been entered
            input_buffer.append(literal(RAParser.TERMINATOR))
            yield '\n'.join(input_buffer);
        return

class RACompleter:
    def __init__(self):
        self.words = list()
        for i, w in enumerate(RAParser.literalNames):
            if w.startswith("'\\"):
                w = w.strip("'")
                if i in (RAParser.RENAME, RAParser.PROJECT, RAParser.SELECT, RAParser.JOIN):
                    self.words.append('{}{} {} '.format(w,
                                                        literal(RAParser.ARG_L),
                                                        literal(RAParser.ARG_R)))
                elif i in (RAParser.LIST, RAParser.QUIT):
                    self.words.append('{}{}'.format(w, literal(RAParser.TERMINATOR)))
                elif i == RAParser.SOURCE:
                    self.words.append("{} ''{}".format(w, literal(RAParser.TERMINATOR)))
                elif i == RAParser.SQLEXEC:
                    self.words.append('{}{} {}{}'.format(w,
                                                         literal(RAParser.ARG_L),
                                                         literal(RAParser.ARG_R),
                                                         literal(RAParser.TERMINATOR)))
                else:
                    self.words.append(w + ' ')
                if i == RAParser.JOIN: # join gets two completion options (theta + natural)
                    self.words.append(w + ' ')
        self.prefix = None
    def complete(self, prefix, index):
        if prefix != self.prefix:
            self.matching_words = [ w for w in self.words if w.startswith(prefix) ]
            self.prefix = prefix
        try:
            return self.matching_words[index]
        except IndexError:
            return None

