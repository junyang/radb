import os
import sys
import itertools

from radb.utils import CustomJSONSerializable, lreplace
from radb.typesys import ValType, AttrSpec, RelType, TypeSysError
from radb.parse import RAParser as sym
from radb.parse import literal, symbolic, sqlstr_to_str, str_to_sqlstr
from radb.parse import statements_from_file, one_statement_from_string

import logging
logger = logging.getLogger('ra')

######################################################################

class Context:
    def __init__(self, db, check, views):
        self.db = db
        self.check = check
        self.views = views

class StatementContext(Context):
    def __init__(self, context: Context, root: 'RelType'):
        super(StatementContext, self).__init__(context.db, context.check, context.views)
        self.tmps = 0
        self.root = root
    def new_tmp(self):
        self.tmps += 1
        return self.tmps-1

######################################################################

def execute_from_file(filename, context, echo=False):
    for ast in statements_from_file(filename):
        if echo:
            print(str(ast) + literal(sym.TERMINATOR))
        ast.validate(context)
        logger.info('statement validated:')
        for line in ast.info():
            logger.info(line)
        ast.execute(context)

class ExecutionError(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, message, node, relexpr=None):
        assert isinstance(message, str)
        self.message = message
        assert isinstance(node, Node)
        self.node = node
        assert relexpr is None or isinstance(relexpr, RelExpr)
        self.relexpr = relexpr
        if self.relexpr is not None and self.relexpr != self.node:
            full_message = 'in {}:\n{}\ncontext: {}'.format(self.node, self.message, self.relexpr)
        else:
            full_message = 'in {}:\n{}'.format(self.node, self.message)
        super(Exception, self).__init__(full_message)

######################################################################

class Node(CustomJSONSerializable):
    pass

class paren: # a decorator for ValExpr and RelExpr
    def __init__(self, expr):
        assert isinstance(expr, ValExpr) or isinstance(expr, RelExpr)
        self.expr = expr
    def can_omit_paren(self):
        return any(isinstance(self.expr, cls) for cls in (Literal, AttrRef, RelRef))
    def __str__(self):
        return ('{}' if self.can_omit_paren() else\
                literal(sym.PAREN_L) + '{}' + literal(sym.PAREN_R))\
                .format(self.expr)
    def info(self):
        return ('{}' if self.can_omit_paren() else '({})').format(self.expr.info())
    def sql(self, relexpr=None):
        return ('{}' if self.can_omit_paren() else '({})')\
            .format(self.expr.sql() if relexpr is None else self.expr.sql(relexpr))

######################################################################

class ValExpr(Node):
    def __init__(self, inputs=list()):
        assert isinstance(inputs, list)
        assert all(isinstance(input, ValExpr) for input in inputs)
        self.inputs = inputs
    def validateSubtree(self, context: StatementContext, relexpr: 'RelExpr'):
        """Validate this value expression (in the scope of the given RelExpr)
        and set its type (as a ValType), using the input RelTypes of
        the RelExpr to resolve attribute references.
        """
        raise NotImplementedError
    def info(self):
        raise NotImplementedError
    def sql(self, relexpr):
        raise NotImplementedError

class Literal(ValExpr):
    def info(self):
        return str(self)
    def sql(self, relexpr):
        return str(self)

class RAString(Literal):
    def __init__(self, val):
        super(RAString, self).__init__()
        assert isinstance(val, str) # include SQL quotes and escapes
        self.val = val
    def __str__(self):
        return self.val
    def validateSubtree(self, context: StatementContext, relexpr):
        self.type = ValType.STRING

class RANumber(Literal):
    def __init__(self, val):
        super(RANumber, self).__init__()
        assert isinstance(val, str) # still represent as a string
        self.val = val
    def __str__(self):
        return self.val
    def validateSubtree(self, context: StatementContext, relexpr):
        self.type = ValType.NUMBER

class FuncValExpr(ValExpr):
    def __init__(self, func, args):
        super(FuncValExpr, self).__init__()
        assert isinstance(func, str)
        self.func = func
        assert isinstance(args, list) and all(isinstance(arg, ValExpr) for arg in args)
        self.args = args
    def __str__(self):
        return self.func + literal(sym.PAREN_L) +\
            ', '.join(str(arg) for arg in self.args) +\
            literal(sym.PAREN_R)
    def validateSubtree(self, context: StatementContext, relexpr):
        argtypes = list()
        for arg in self.args:
            arg.validateSubtree(context, relexpr)
            argtypes.append(arg.type)
        try:
            self.type = context.check.function_call(self.func, argtypes)
        except TypeSysError as e:
            raise ValidationError(str(e), self, relexpr) from e
    def info(self):
        return self.func + literal(sym.PAREN_L) +\
            ', '.join(arg.info() for arg in self.args) +\
            literal(sym.PAREN_R)
    def sql(self, relexpr):
        return self.func + literal(sym.PAREN_L) +\
            ', '.join(arg.sql(relexpr) for arg in self.args) +\
            literal(sym.PAREN_R)

class AttrRef(ValExpr):
    def __init__(self, rel, name):
        super(AttrRef, self).__init__()
        assert rel is None or isinstance(rel, str)
        assert isinstance(name, str)
        self.rel = rel
        self.name = name
    def __str__(self):
        if self.rel is None:
            return self.name
        else:
            return self.rel + literal(sym.DOT) + self.name
    def validateSubtree(self, context: StatementContext, relexpr):
        """Validate this attribute reference (in the scope of the given
        RelExpr) and set its type (as a ValType) and internal
        reference (used in translation), using the input RelTypes of
        the RelExpr to resolve attribute references.
        """
        self.type = None
        self.internal_ref = None
        for ridx, relinput in enumerate(relexpr.inputs):
            for aidx, attrspec in enumerate(relinput.type.attrs):
                if self.name == attrspec.name and\
                   (self.rel is None or self.rel == attrspec.rel):
                    if self.internal_ref is not None:
                        raise ValidationError('ambiguous attribute reference', self, relexpr)
                    self.type = attrspec.type
                    self.internal_ref = (ridx, aidx)
        if self.internal_ref is None:
            raise ValidationError('invalid attribute reference', self, relexpr)
    def info(self):
        return '{}[{}.{}]'.format(self, *self.internal_ref)
    def sql(self, relexpr):
        ridx, aidx = self.internal_ref
        return '{}.{}'.format(relexpr.inputs[ridx].type.sql_rel(),
                              relexpr.inputs[ridx].type.sql_attr(aidx))

class ValExprBinaryOp(ValExpr):
    def __init__(self, left, op, right):
        assert isinstance(left, ValExpr)
        assert op in (sym.STAR, sym.SLASH, sym.PLUS, sym.MINUS,
                      sym.LT, sym.LE, sym.EQ, sym.NE, sym.GE, sym.GT,
                      sym.CONCAT,
                      sym.AND, sym.OR,
                      sym.LIKE)
        assert isinstance(right, ValExpr)
        super(ValExprBinaryOp, self).__init__([left, right])
        self.op = op
    def __str__(self):
        return '{} {} {}'.format(paren(self.inputs[0]), literal(self.op), paren(self.inputs[1]))
    def validateSubtree(self, context: StatementContext, relexpr):
        self.inputs[0].validateSubtree(context, relexpr)
        self.inputs[1].validateSubtree(context, relexpr)
        try:
            self.type = context.check.function_call(symbolic(self.op),
                                                    [self.inputs[0].type, self.inputs[1].type])
        except TypeSysError as e:
            raise ValidationError(str(e), self, relexpr) from e
    def info(self):
        return '{} {} {}'.format(paren(self.inputs[0]).info(),
                                 literal(self.op),
                                 paren(self.inputs[1]).info())
    def sql(self, relexpr):
        return '{} {} {}'.format(paren(self.inputs[0]).sql(relexpr),
                                 literal(self.op),
                                 paren(self.inputs[1]).sql(relexpr))

class ValExprUnaryOp(ValExpr):
    def __init__(self, op, input):
        assert isinstance(input, ValExpr)
        assert op in (sym.NOT, sym.IS_NULL, sym.IS_NOT_NULL)
        self.op = op
        super(ValExprUnaryOp, self).__init__([input])
    def __str__(self):
        fmt = '{input} {op}' if self.op in (sym.IS_NULL, sym.IS_NOT_NULL) else '{op} {input}'
        return fmt.format(op=literal(self.op), input=paren(self.inputs[0]))
    def validateSubtree(self, context: StatementContext, relexpr):
        self.inputs[0].validateSubtree(context, relexpr)
        try:
            self.type = context.check.function_call(symbolic(self.op), [self.inputs[0].type])
        except TypeSysError as e:
            raise ValidationError(str(e), self, relexpr) from e
    def info(self):
        fmt = '{input} {op}' if self.op in (sym.IS_NULL, sym.IS_NOT_NULL) else '{op} {input}'
        return fmt.format(op=literal(self.op), input=paren(self.inputs[0]).info())
    def sql(self, relexpr):
        fmt = '{input} {op}' if self.op in (sym.IS_NULL, sym.IS_NOT_NULL) else '{op} {input}'
        return fmt.format(op=literal(self.op), input=paren(self.inputs[0]).sql(relexpr))

######################################################################

class RelExpr(Node):
    def __init__(self, inputs=list()):
        assert isinstance(inputs, list)
        assert all(isinstance(input, RelExpr) for input in inputs)
        self.inputs = inputs
    def validate(self, context: Context):
        self.validateSubtree(StatementContext(context, self))
    def validateSubtree(self, context: StatementContext):
        """Validate this value expression and set its type (as a RelType),
        using the given context to resolve relation references.
        """
        pass
    def validationError(self, message):
        return ValidationError(message, self, self)
    def find_views(self):
        if isinstance(self, RelRef):
            return set() if self.view is None else {self.rel}
        else:
            views = set()
            for input in self.inputs:
                views |= input.find_views()
            return views
    def info(self):
        raise NotImplementedError
    def sql(self):
        raise NotImplementedError
    def execute(self, context):
        blocks = [block for block in self.sql()]
        assert(len(blocks) > 0)
        query = 'WITH ' + ',\n     '.join(blocks)
        query += '\nSELECT * FROM {}'.format(self.type.sql_rel())
        logger.debug('SQL generated:\n' + query)
        try:
            print('({})'.format(', '.join(self.type.str_attr_names_and_types())))
            context.db.execute_and_print_result(query)
        except Exception as e:
            raise ExecutionError('SQL error in translated query:\n{}\n{}'.format(query, e)) from e
    @staticmethod
    def from_view_def(view_def):
        return one_statement_from_string(view_def + literal(sym.TERMINATOR))

class RelRef(RelExpr):
    def __init__(self, rel):
        super(RelRef, self).__init__()
        assert isinstance(rel, str)
        self.rel = rel
    def __str__(self):
        return self.rel
    def validateSubtree(self, context: StatementContext):
        # first check if this is a table in dbms:
        if context.db.table_exists(self.rel):
            attrspecs = [AttrSpec(self.rel, attr, type)\
                         for attr, type in context.db.describe(self.rel)]
            self.type = RelType(context.new_tmp(), attrspecs)
            self.view = None
            return
        # then check if this is a view defined in this session:
        view_def = context.views.raw_def(self.rel)
        if view_def is not None:
            self.view = RelExpr.from_view_def(view_def)
            self.view.validateSubtree(context)
            attrspecs = [AttrSpec(self.rel, attrspec.name, attrspec.type)\
                         for attrspec in self.view.type.attrs]
            self.type = RelType(self.view.type.tmp, attrspecs) # don't create a new temp relation
            return
        # reference is not found:
        raise self.validationError('relation {} does not exist'.format(self.rel))
    def info(self):
        if self.view is None:
            yield 'RELATION {} => {}'.format(self, self.type)
        else:
            yield 'VIEW {} => {}'.format(self, self.type)
            for i, line in enumerate(self.view.info()):
                yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        if self.view is None:
            yield '{}({}) AS (SELECT * FROM {})'\
                .format(self.type.sql_rel(), ', '.join(self.type.sql_attrs()), self.rel)
        else:
            for block in self.view.sql():
                yield block

class Rename(RelExpr):
    def __init__(self, relname, attrnames, input):
        assert relname is not None or attrnames is not None
        assert relname is None or isinstance(relname, str)
        assert attrnames is None or\
            (isinstance(attrnames, list) and len(attrnames) > 0 and\
             all(isinstance(name, str) for name in attrnames))
        assert isinstance(input, RelExpr)
        super(Rename, self).__init__([input])
        self.relname = relname
        self.attrnames = attrnames
    def __str__(self):
        s = literal(sym.RENAME) + literal(sym.ARG_L)
        if self.relname is not None:
            s += self.relname + literal(sym.COLON) + ' '
        if self.attrnames is None:
            s += literal(sym.STAR)
        else:
            s += ', '.join(name for name in self.attrnames)
        s += literal(sym.ARG_R) + ' ' + str(paren(self.inputs[0]))
        return s
    def validateSubtree(self, context: StatementContext):
        self.inputs[0].validateSubtree(context)
        if self.attrnames is not None:
            if len(self.attrnames) != len(self.inputs[0].type.attrs):
                raise self.validationError('renaming {} attribute(s) but the input has {}'\
                                           .format(len(self.attrnames),
                                                   len(self.inputs[0].type.attrs)))
            if len(self.attrnames) != len(set(self.attrnames)):
                logger.warning('{}: duplicate attribute names when renaming: {}'\
                               .format(self, ', '.join(self.attrnames)))
        else:
            for a1, a2 in itertools.combinations(self.inputs[0].type.attrs, 2):
                if a1.name == a2.name and not a1.can_be_confused_with(a2):
                    logger.warning('{}: attributes {} and {} become confused after renaming'\
                                   .format(self, a1.str_ref_only(), a2.str_ref_only()))
        attrspecs = list()
        if self.attrnames is not None:
            for name, attrspec in zip(self.attrnames, self.inputs[0].type.attrs):
                attrspecs.append(AttrSpec(self.relname, name, attrspec.type))
        else:
            for attrspec in self.inputs[0].type.attrs:
                attrspecs.append(AttrSpec(self.relname, attrspec.name, attrspec.type))
        self.type = RelType(self.inputs[0].type.tmp, attrspecs) # don't create a new temp relation
    def info(self):
        yield '{} => {}'.format(symbolic(sym.RENAME), self.type)
        for i, line in enumerate(self.inputs[0].info()):
            yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        for block in self.inputs[0].sql(): # don't create a new temp relation
            yield block

class Project(RelExpr):
    def __init__(self, attrs, input):
        assert isinstance(attrs, list)
        assert all(isinstance(attr, ValExpr) for attr in attrs)
        assert isinstance(input, RelExpr)
        super(Project, self).__init__([input])
        self.attrs = attrs
    def __str__(self):
        return literal(sym.PROJECT) + literal(sym.ARG_L) +\
            ', '.join(str(attr) for attr in self.attrs) +\
            literal(sym.ARG_R) + ' ' + str(paren(self.inputs[0]))
    def validateSubtree(self, context: StatementContext):
        self.inputs[0].validateSubtree(context)
        output_attrspecs = list()
        for attr in self.attrs:
            attr.validateSubtree(context, self)
            if isinstance(attr, AttrRef):
                _, aidx = attr.internal_ref
                output_attrspecs.append(self.inputs[0].type.attrs[aidx])
            else:
                output_attrspecs.append(AttrSpec(None, None, attr.type))
        self.type = RelType(context.new_tmp(), output_attrspecs)
    def info(self):
        yield '{} => {}'.format(symbolic(sym.PROJECT), self.type)
        for attr in self.attrs:
            yield '|' + attr.info()
        for i, line in enumerate(self.inputs[0].info()):
            yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        for block in self.inputs[0].sql():
            yield block
        yield '{}({}) AS (SELECT DISTINCT {} FROM {})'\
            .format(self.type.sql_rel(), ', '.join(self.type.sql_attrs()),
                    ', '.join(attr.sql(self) for attr in self.attrs),
                    self.inputs[0].type.sql_rel())

class Select(RelExpr):
    def __init__(self, cond, input):
        assert isinstance(cond, ValExpr)
        assert isinstance(input, RelExpr)
        super(Select, self).__init__([input])
        self.cond = cond
    def __str__(self):
        return literal(sym.SELECT) + literal(sym.ARG_L) + str(self.cond) + literal(sym.ARG_R) +\
            ' ' + str(paren(self.inputs[0]))
    def validateSubtree(self, context: StatementContext):
        self.inputs[0].validateSubtree(context)
        self.cond.validateSubtree(context, self)
        if self.cond.type != ValType.BOOLEAN:
            raise self.validationError('selection condition {} has type {}; boolean expected'\
                                       .format(self.cond, self.cond.type.value))
        self.type = RelType(context.new_tmp(), self.inputs[0].type.attrs)
    def info(self):
        yield '{} => {}'.format(symbolic(sym.SELECT), self.type)
        yield '|' + self.cond.info()
        for i, line in enumerate(self.inputs[0].info()):
            yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        for block in self.inputs[0].sql():
            yield block
        yield '{}({}) AS (SELECT * FROM {} WHERE {})'\
            .format(self.type.sql_rel(), ', '.join(self.type.sql_attrs()),
                    self.inputs[0].type.sql_rel(),
                    self.cond.sql(self))

class Join(RelExpr):
    def __init__(self, left, cond, right):
        assert isinstance(left, RelExpr)
        assert cond is None or isinstance(cond, ValExpr)
        assert isinstance(right, RelExpr)
        super(Join, self).__init__([left, right])
        self.cond = cond
    def __str__(self):
        cond = '' if self.cond is None else\
               literal(sym.ARG_L) + str(self.cond) + literal(sym.ARG_R)
        return '{} {}{} {}'.format(paren(self.inputs[0]),
                                   literal(sym.JOIN), cond,
                                   paren(self.inputs[1]))
    def validateSubtree(self, context: StatementContext):
        self.inputs[0].validateSubtree(context)
        self.inputs[1].validateSubtree(context)
        if self.cond is None:
            self.pairs = list()
            for i0, a0 in enumerate(self.inputs[0].type.attrs):
                if a0.name is None:
                    continue
                matches = [(i1, a1) for i1, a1 in enumerate(self.inputs[1].type.attrs)\
                           if a0.name == a1.name]
                if len(matches) > 1:
                    raise self.validationError('ambiguity in natural join: {} from the left input'
                                               ' matches multiple attributes on the right'\
                                               .format(a0.str_ref_only()))

                elif len(matches) == 1:
                    i1, a1 = matches[0]
                    try:
                        context.check.function_call(symbolic(sym.EQ), [a0.type, a1.type])
                    except TypeSysError as e:
                        raise self.validationError('natural join cannot equate {} and {}'\
                                                   .format(a0, a1))
                    self.pairs.append((i0, i1))
            if len(self.pairs) == 0:
                logger.warning('{}: no attributes with matching names found;'
                               ' natural join degnerates into cross product'.format(self))
            for i0, i1 in self.pairs:
                if any((j0, j1) for j0, j1 in self.pairs if j0 != i0 and j1 == i1):
                    raise self.validationError('ambiguity in natural join: {} from the right input'
                                               ' matches multiple attributes on the left'\
                                               .format(self.inputs[1].type.attrs[i1]\
                                                       .str_ref_only()))
            attrspecs = list()
            for a0 in self.inputs[0].type.attrs:
                attrspecs.append(a0)
            for i1, a1 in enumerate(self.inputs[1].type.attrs):
                if not any(i1 == i for _, i in self.pairs):
                    attrspecs.append(a1)
                    if any(a1.can_be_confused_with(a0) for a0 in self.inputs[0].type.attrs):
                        # this shouldn't happen under natural join rule, but oh well:
                        logger.warning('{}: attribute {} becomes confused with others'
                                       ' in the join output'\
                                       .format(self, a1.str_ref_only()))
            self.type = RelType(context.new_tmp(), attrspecs)
        else:
            self.cond.validateSubtree(context, self)
            if self.cond.type != ValType.BOOLEAN:
                raise self.validationError('join condition {} has type {}; boolean expected'\
                                           .format(self.cond, self.cond.type.value))
            for a0, a1 in itertools.product(self.inputs[0].type.attrs, self.inputs[1].type.attrs):
                if a0.can_be_confused_with(a1):
                    logger.warning('{}: attributes {} from the left input and {} from the right'
                                   ' become confused in the join output'\
                                   .format(self, a0.str_ref_only(), a1.str_ref_only()))
            self.type = RelType(context.new_tmp(),
                                self.inputs[0].type.attrs + self.inputs[1].type.attrs)
    def info(self):
        yield '{} => {}'.format(symbolic(sym.JOIN), self.type)
        if self.cond is not None:
            yield '|' + self.cond.info()
        elif len(self.pairs) == 0:
            yield '|inferred: cross product with no join condition'
        else:
            for i0, i1 in self.pairs:
                yield '|inferred: {}[0.{}] = {}[1.{}]'\
                    .format(self.inputs[0].type.attrs[i0].str_ref_only(), i0,
                            self.inputs[1].type.attrs[i1].str_ref_only(), i1)
        for i, line in enumerate(self.inputs[0].info()):
            yield ('\\_' if i == 0 else '| ') + line
        for i, line in enumerate(self.inputs[1].info()):
            yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        for block in self.inputs[0].sql():
            yield block
        for block in self.inputs[1].sql():
            yield block
        select = '*'
        where = ''
        if self.cond is None:
            if len(self.pairs) > 0:
                attrs = ['{}.{}'.format(self.inputs[0].type.sql_rel(), attr)\
                          for attr in self.inputs[0].type.sql_attrs()]
                attrs += ['{}.{}'.format(self.inputs[1].type.sql_rel(), attr)\
                           for i, attr in enumerate(self.inputs[1].type.sql_attrs())\
                           if all(i != i1 for _, i1 in self.pairs)]
                select = ', '.join(attrs)
                eqs = ['{}.{} = {}.{}'.format(self.inputs[0].type.sql_rel(),
                                              self.inputs[0].type.sql_attr(i0),
                                              self.inputs[1].type.sql_rel(),
                                              self.inputs[1].type.sql_attr(i1))\
                       for i0, i1 in self.pairs]
                where = ' WHERE {}'.format(' AND '.join(eqs))
        else:
            where = ' WHERE {}'.format(self.cond.sql(self))
        yield '{}({}) AS (SELECT {} FROM {}, {}{})'\
            .format(self.type.sql_rel(), ', '.join(self.type.sql_attrs()),
                    select,
                    self.inputs[0].type.sql_rel(), self.inputs[1].type.sql_rel(),
                    where)

class Cross(RelExpr):
    def __init__(self, left, right):
        assert isinstance(left, RelExpr)
        assert isinstance(right, RelExpr)
        super(Cross, self).__init__([left, right])
    def __str__(self):
        return '{} {} {}'.format(paren(self.inputs[0]), literal(sym.CROSS), paren(self.inputs[1]))
    def validateSubtree(self, context: StatementContext):
        self.inputs[0].validateSubtree(context)
        self.inputs[1].validateSubtree(context)
        for a0, a1 in itertools.product(self.inputs[0].type.attrs, self.inputs[1].type.attrs):
            if a0.can_be_confused_with(a1):
                logger.warning('{}: attributes {} from the left input and {} from the right'
                               ' become confused in the cross product output'\
                               .format(self, a0.str_ref_only(), a1.str_ref_only()))
        self.type = RelType(context.new_tmp(),
                            self.inputs[0].type.attrs + self.inputs[1].type.attrs)
    def info(self):
        yield '{} => {}'.format(symbolic(sym.CROSS), self.type)
        for i, line in enumerate(self.inputs[0].info()):
            yield ('\\_' if i == 0 else '| ') + line
        for i, line in enumerate(self.inputs[1].info()):
            yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        for block in self.inputs[0].sql():
            yield block
        for block in self.inputs[1].sql():
            yield block
        yield '{}({}) AS (SELECT * FROM {}, {})'\
            .format(self.type.sql_rel(), ', '.join(self.type.sql_attrs()),
                    self.inputs[0].type.sql_rel(), self.inputs[1].type.sql_rel())

class SetOp(RelExpr):
    def __init__(self, left, right):
        assert isinstance(left, RelExpr)
        assert isinstance(right, RelExpr)
        super(SetOp, self).__init__([left, right])
    def op(self):
        if isinstance(self, Union):
            return sym.UNION
        elif isinstance(self, Diff):
            return sym.DIFF
        elif isinstance(self, Intersect):
            return sym.INTERSECT
        else:
            assert False
    def sql_op(self):
        if isinstance(self, Union):
            return 'UNION'
        elif isinstance(self, Diff):
            return 'EXCEPT'
        elif isinstance(self, Intersect):
            return 'INTERSECT'
        else:
            assert False
    def __str__(self):
        return '{} {} {}'.format(paren(self.inputs[0]),
                                 literal(self.op()),
                                 paren(self.inputs[1]))
    def validateSubtree(self, context: StatementContext):
        self.inputs[0].validateSubtree(context)
        self.inputs[1].validateSubtree(context)
        if len(self.inputs[0].type.attrs) != len(self.inputs[1].type.attrs):
            raise self.validationError('input relations to a set operation'
                                       ' do not have the same number of attributes')
        for i, (a0, a1) in enumerate(zip(self.inputs[0].type.attrs, self.inputs[1].type.attrs)):
            if a0.type != a1.type:
                raise self.validationError('input attributes at position {} have'
                                           ' different types: {} vs. {}'.format(i, a0, a1))
            if a0.name != a1.name:
                logger.warning('{}: input attributes at position {} have'
                               ' different names: {} vs. {}'.format(self, i,
                                                                    a0.str_ref_only(),
                                                                    a1.str_ref_only()))
        self.type = RelType(context.new_tmp(), self.inputs[0].type.attrs)
    def info(self):
        yield '{} => {}'.format(symbolic(self.op()), self.type)
        for i, line in enumerate(self.inputs[0].info()):
            yield ('\\_' if i == 0 else '| ') + line
        for i, line in enumerate(self.inputs[1].info()):
            yield ('\\_' if i == 0 else '  ') + line
    def sql(self):
        for block in self.inputs[0].sql():
            yield block
        for block in self.inputs[1].sql():
            yield block
        # interestingly, in the SQL below, parentheses around the two
        # SELECT subqueries are not needed, and SQLite in fact would
        # not like them:
        yield '{}({}) AS (SELECT * FROM {} {} SELECT * FROM {})'\
            .format(self.type.sql_rel(), ', '.join(self.type.sql_attrs()),
                    self.inputs[0].type.sql_rel(),
                    self.sql_op(),
                    self.inputs[1].type.sql_rel())

class Union(SetOp):
    pass

class Diff(SetOp):
    pass

class Intersect(SetOp):
    pass

class Define(Node):
    def __init__(self, view, definition):
        assert isinstance(view, str)
        assert isinstance(definition, RelExpr)
        self.view = view
        self.definition = definition
    def __str__(self):
        return '{} {} {}'.format(self.view, literal(sym.GETS), self.definition)
    def validate(self, context):
        if context.db.table_exists(self.view):
            raise ValidationError('{} is a database relation'.format(self.view), self)
        if context.views.raw_def(self.view) is None:
            self.definition.validate(context)
        else:
            dependents = context.views.find_dependents(self.view, recurse=True)
            # validate this definition without previously dependent views:
            tmp_context = Context(context.db, context.check, context.views.clone())
            tmp_context.views.clear(self.view) # which removes dependents too
            try:
                self.definition.validate(tmp_context)
            except ValidationError as e:
                if isinstance(e.node, RelRef) and\
                   (e.node.rel in dependents or e.node.rel == self.view):
                    raise ValidationError('{} and {} are circularly defined'\
                                          .format(self.view, e.node.rel), self)\
                                          from e
                else:
                    raise
            # now, with the new definition, try validating dependents:
            tmp_context.views = context.views.clone()
            tmp_context.views.register(self.view,
                                       str(self.definition), self.definition.find_views())
            for v in dependents:
                try:
                    ast = RelExpr.from_view_def(tmp_context.views.raw_def(v))
                    ast.validate(tmp_context)
                except ValidationError as e:
                    raise ValidationError('view definition of {} is broken'
                                          ' by the new defintion of {}:\n{}'\
                                          .format(v, self.view, e), self)\
                                          from e
    def info(self):
        views = self.definition.find_views()
        yield 'VIEW {} depends on '.format(self.view) +\
            ('no other views' if len(views) == 0 else ', '.join(views))
        yield literal(sym.GETS)
        for line in self.definition.info():
            yield line
    def execute(self, context):
        context.views.register(self.view, str(self.definition), self.definition.find_views())
        print('view {} defined'.format(self.view))

class Command(Node):
    def __init__(self, cmd):
        assert cmd in (sym.LIST, sym.QUIT)
        self.cmd = cmd
    def __str__(self):
        return literal(self.cmd)
    def validate(self, context):
        pass
    def info(self):
        yield symbolic(self.cmd)
    def execute(self, context):
        if self.cmd == sym.LIST:
            print('database relations:')
            for table in context.db.list():
                attrs = ['{}:{}'.format(attr, type.value)\
                         for attr, type in context.db.describe(table)]
                print('  {}({})'.format(table, ', '.join(attrs)))
            if len(context.views.list()) > 0:
                print('views defined:')
                for view in context.views.list():
                    raw_def = context.views.raw_def(view)
                    ast = RelExpr.from_view_def(raw_def)
                    logging.disable(logging.WARNING)
                    ast.validate(context)
                    logging.disable(logging.NOTSET)
                    print('  {}({}) {} {}'.format(view,
                                                  ', '.join(ast.type.str_attr_names_and_types()),
                                                  literal(sym.GETS), raw_def))
        elif self.cmd == sym.QUIT:
            sys.exit(0)

class CommandClear(Command):
    def __init__(self, force=False, view=None):
        assert isinstance(force, bool)
        self.force = force
        assert view is None or isinstance(view, str)
        self.view = view
    def __str__(self):
        return literal(sym.CLEAR) +\
            (literal(sym.FORCE) if self.force else '') + ' ' +\
            (literal(sym.STAR) if self.view is None else self.view)
    def validate(self, context):
        if self.view is not None:
            if context.views.raw_def(self.view) is None:
                raise ValidationError('view {} is not defined'.format(self.view), self)
            if not self.force:
                dependents = context.views.find_dependents(self.view)
                if len(dependents) > 0:
                    raise ValidationError('view {} is used in defining others ({});'
                                          ' to clear them all, use {} after {}'\
                                          .format(self.view, ', '.join(dependents),
                                                  literal(sym.FORCE), literal(sym.CLEAR)), self)
    def info(self):
        yield lreplace(str(self), literal(sym.CLEAR), symbolic(sym.CLEAR))
    def execute(self, context):
        views_cleared = context.views.list() if self.view is None else\
                        context.views.find_dependents(self.view) | {self.view}
        if len(views_cleared) == 0:
            print('no views to clear')
        else:
            context.views.clear(self.view)
            print('views cleared: {}'.format(', '.join(views_cleared)))

class CommandSave(Command):
    def __init__(self, force=False, view=None, filename=None):
        assert isinstance(force, bool)
        self.force = force
        assert view is None or isinstance(view, str)
        self.view = view
        assert filename is None or isinstance(filename, str)
        if filename is None:
            self.filename = '{}.ra'.format('views' if self.view is None else self.view)
        else:
            self.filename = sqlstr_to_str(filename)
    def __str__(self):
        return literal(sym.SAVE) +\
            (literal(sym.FORCE) if self.force else '') + ' ' +\
            (literal(sym.STAR) if self.view is None else self.view) + ' ' +\
            str_to_sqlstr(self.filename)
    def validate(self, context):
        if self.view is not None and context.views.raw_def(self.view) is None:
            raise ValidationError('view {} is not defined'.format(self.view), self)
        if not self.force and os.path.isfile(self.filename):
            raise ValidationError('file {} already exists; to overwrite use {} after {}'\
                                  .format(self.filename, literal(sym.FORCE), literal(sym.SAVE)),
                                  self)
    def info(self):
        yield lreplace(str(self), literal(sym.SAVE), symbolic(sym.SAVE))
    def execute(self, context):
        views = context.views.topo(self.view)
        try:
            with open(self.filename, 'w') as f:
                for v in views:
                    print('{} {} {};'.format(v, literal(sym.GETS), context.views.raw_def(v)),
                          file=f)
            print('wrote file {}'.format(self.filename))
        except Exception as e:
            raise ExecutionError('writing to {} failed'.format(self.filename), self) from e

class CommandSource(Command):
    def __init__(self, filename):
        assert isinstance(filename, str)
        self.filename = sqlstr_to_str(filename)
    def __str__(self):
        return literal(sym.SOURCE) + ' ' + str_to_sqlstr(self.filename)
    def validate(self, context):
        if not os.path.isfile(self.filename):
            raise ValidationError('file {} does not exist'.format(self.filename), self)
    def info(self):
        yield lreplace(str(self), literal(sym.SOURCE), symbolic(sym.SOURCE))
    def execute(self, context):
        try:
            execute_from_file(self.filename, context, echo=True)
        except Exception as e:
            raise ExecutionError('error while executing from {}:\n{}'\
                                 .format(self.filename, e)) from e

class CommandSqlexec(Command):
    def __init__(self, sql):
        assert isinstance(sql, str)
        self.sql = sql
    def __str__(self):
        return literal(sym.SQLEXEC) +\
            literal(sym.ARG_L) + self.sql + literal(sym.ARG_R)
    def validate(self, context):
        pass
    def info(self):
        yield symbolic(sym.SQLEXEC) + ': ' + self.sql
    def execute(self, context):
        logger.debug(self.sql)
        try:
            context.db.execute_and_print_result(self.sql)
        except Exception as e:
            raise ExecutionError('SQL error in:\n{}\n{}'.format(self.sql, e)) from e
