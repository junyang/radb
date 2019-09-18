# Generated from RAParser.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .RAParser import RAParser
else:
    from RAParser import RAParser

# This class defines a complete generic visitor for a parse tree produced by RAParser.

class RAParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RAParser#andExpr.
    def visitAndExpr(self, ctx:RAParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#numberLiteralValExpr.
    def visitNumberLiteralValExpr(self, ctx:RAParser.NumberLiteralValExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#likeExpr.
    def visitLikeExpr(self, ctx:RAParser.LikeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#funcExpr.
    def visitFuncExpr(self, ctx:RAParser.FuncExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#plusMinusExpr.
    def visitPlusMinusExpr(self, ctx:RAParser.PlusMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#compareExpr.
    def visitCompareExpr(self, ctx:RAParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#orExpr.
    def visitOrExpr(self, ctx:RAParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#attrRef.
    def visitAttrRef(self, ctx:RAParser.AttrRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#multDivExpr.
    def visitMultDivExpr(self, ctx:RAParser.MultDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#concatExpr.
    def visitConcatExpr(self, ctx:RAParser.ConcatExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#valExprParenthesized.
    def visitValExprParenthesized(self, ctx:RAParser.ValExprParenthesizedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#isNotNullExpr.
    def visitIsNotNullExpr(self, ctx:RAParser.IsNotNullExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#isNullExpr.
    def visitIsNullExpr(self, ctx:RAParser.IsNullExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#stringLiteralValExpr.
    def visitStringLiteralValExpr(self, ctx:RAParser.StringLiteralValExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#notExpr.
    def visitNotExpr(self, ctx:RAParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#listOfValExprs.
    def visitListOfValExprs(self, ctx:RAParser.ListOfValExprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#listOfIDs.
    def visitListOfIDs(self, ctx:RAParser.ListOfIDsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#crossExpr.
    def visitCrossExpr(self, ctx:RAParser.CrossExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#relExprParenthesized.
    def visitRelExprParenthesized(self, ctx:RAParser.RelExprParenthesizedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#projectExpr.
    def visitProjectExpr(self, ctx:RAParser.ProjectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#relRef.
    def visitRelRef(self, ctx:RAParser.RelRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#intersectExpr.
    def visitIntersectExpr(self, ctx:RAParser.IntersectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#selectExpr.
    def visitSelectExpr(self, ctx:RAParser.SelectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#diffExpr.
    def visitDiffExpr(self, ctx:RAParser.DiffExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#joinExpr.
    def visitJoinExpr(self, ctx:RAParser.JoinExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#aggrExpr.
    def visitAggrExpr(self, ctx:RAParser.AggrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#renameExpr.
    def visitRenameExpr(self, ctx:RAParser.RenameExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#unionExpr.
    def visitUnionExpr(self, ctx:RAParser.UnionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#definition.
    def visitDefinition(self, ctx:RAParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#listCommand.
    def visitListCommand(self, ctx:RAParser.ListCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#clearCommand.
    def visitClearCommand(self, ctx:RAParser.ClearCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#saveCommand.
    def visitSaveCommand(self, ctx:RAParser.SaveCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#sourceCommand.
    def visitSourceCommand(self, ctx:RAParser.SourceCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#helpCommand.
    def visitHelpCommand(self, ctx:RAParser.HelpCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#quitCommand.
    def visitQuitCommand(self, ctx:RAParser.QuitCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#sqlexecCommand.
    def visitSqlexecCommand(self, ctx:RAParser.SqlexecCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#statement.
    def visitStatement(self, ctx:RAParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RAParser#program.
    def visitProgram(self, ctx:RAParser.ProgramContext):
        return self.visitChildren(ctx)



del RAParser