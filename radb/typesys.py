from typing import List, Dict, Union, Optional
import copy
import re

from radb.utils import AutoNameEnum, CustomJSONSerializable

import logging
logger = logging.getLogger('ra')

class TypeSysError(Exception):
    pass

ValType = AutoNameEnum('ValType', (
    'BOOLEAN',
    'NUMBER',
    'STRING',
    'DATE',
    'DATETIME',
    'UNKNOWN',
    'ANY',
))

class FuncSpec:
    """Specification (i.e., signature) of a built-in function.  See
    :ref:`Operators and Functions` and :ref:`Type Checking` for an
    overview.

    """
    def __init__(self,
                 name: str, is_aggr: bool, outtype: ValType,
                 required_argtypes: List[ValType],
                 optional_argtypes: List[ValType],
                 no_max_argc: bool=False):
        """Create a function specification.  The function is an aggregate
        function if is_aggr is True.  If no_max_argc is True, the
        function can take an arbitrary number of additional arguments;
        in that case, optional_argtypes must not be empty, and its
        last element will be used as the type for additional
        arguments.
        """
        self.name = name
        self.is_aggr = is_aggr
        self.outtype = outtype
        self.required_argtypes = required_argtypes
        self.optional_argtypes = optional_argtypes
        self.no_max_argc = no_max_argc
    def __str__(self):
        s_argtypes = list()
        for argtype in self.required_argtypes:
            s_argtypes.append(argtype.value)
        for i, argtype in enumerate(self.optional_argtypes):
            s_argtypes.append(argtype.value\
                              + ('*' if (i == len(self.optional_argtypes)-1 and self.no_max_argc)\
                                 else '?'))
        return '{}{}({}) -> {}'.format('aggregate: ' if self.is_aggr else '',
                                       self.name, ', '.join(s_argtypes), self.outtype.value)
    @staticmethod
    def from_config_line(line: str):
        """Construct a :class:`FuncSpec` object from a line.  See
        :ref:`Specification of Built-in Functions` for the
        specification format.

        """
        r_argtype = r'\w+[\?\*]?'
        r_argtypes = r'\s*(?:{r_argtype}(?:\s*,\s*{r_argtype})*)?\s*'.format(r_argtype=r_argtype)
        r_decl =\
            r'(?P<s_aggregate>\s*aggregate\s*:)?' +\
            r'\s*(?P<s_name>[^\s\(]*)\s*' +\
            r'\((?P<s_argtypes>{r_argtypes})\)'.format(r_argtypes=r_argtypes) +\
            r'\s*->\s*(?P<s_outtype>\w+)\s*(\#.*)?$'
        m = re.match(r_decl, line)
        if m is None:
            raise TypeSysError('cannot parse function declaration: {}'.format(line.strip()))
        name, s_argtypes, s_outtype = m.group('s_name', 's_argtypes', 's_outtype')
        is_aggr = (m.group('s_aggregate') is not None)
        outtype = ValType(s_outtype)
        required_argtypes = list()
        optional_argtypes = list()
        no_max_argc = False
        for s_argtype in re.findall(r_argtype, s_argtypes):
            argtype = ValType(s_argtype.rstrip('?*'))
            if s_argtype[-1] in ('?', '*'):
                if no_max_argc:
                    raise TypeSysError('only the very last argument can have *')
                if s_argtype[-1] == '*':
                    no_max_argc = True
                optional_argtypes.append(argtype)
            else:
                if len(optional_argtypes) > 0:
                    raise TypeSysError('required argument cannot follow an optional one')
                required_argtypes.append(argtype)
        return FuncSpec(name, is_aggr,
                        outtype, required_argtypes, optional_argtypes, no_max_argc)

class ValTypeChecker:
    def __init__(self, default_decl_lines: str, decl_lines: str=None):
        default_decls = ValTypeChecker.decls_from_config_lines(default_decl_lines)
        if decl_lines is None:
            self.decls = default_decls
        else:
            self.decls = ValTypeChecker.decls_from_config_lines(decl_lines)
            for f in default_decls:
                if f in self.decls:
                    logger.info('default signature of "{}" overridden by configuration'.format(f))
                else:
                    self.decls[f] = default_decls[f]
    @staticmethod
    def decls_from_config_lines(lines):
        decls = dict()
        for i, line in enumerate(lines.split('\n')):
            line = line.rsplit('#', 1)[0].strip() # strip trailing comment
            if line == '':
                continue
            f = FuncSpec.from_config_line(line)
            if f.name not in decls:
                decls[f.name] = list()
            decls[f.name].append(f)
        return decls
    def can_be_used_as(self, this, other):
        if this == other:
            return True
        if other == ValType.ANY:
            return True
        if this == ValType.UNKNOWN:
            return True # relaxed semantics: allow UNKNOWN to be used as any type
        if this == ValType.STRING and other in (ValType.DATE, ValType.DATETIME):
            return True
        if this == ValType.DATE and other == ValType.DATETIME:
            return True
        return False
    def function_call(self, fname: str, argtypes: List[ValType], allow_aggr=False):
        if fname not in self.decls:
            logger.warning('function "{}" not recognized'.format(fname))
            return FuncSpec(fname, None, ValType.UNKNOWN, argtypes, list())
        for funcspec in self.decls[fname]:
            if len(argtypes) < len(funcspec.required_argtypes):
                continue
            if (not funcspec.no_max_argc)\
               and len(argtypes) > len(funcspec.required_argtypes)+len(funcspec.optional_argtypes):
                continue
            targets = copy.copy(funcspec.required_argtypes)
            for i in range(len(argtypes)-len(funcspec.required_argtypes)):
                targets.append(funcspec.optional_argtypes\
                               [min(i, len(funcspec.optional_argtypes)-1)])
            if all(self.can_be_used_as(argtype, target)\
                   for argtype, target in zip(argtypes, targets)):
                if not allow_aggr and funcspec.is_aggr:
                    raise TypeSysError('aggregate function "{}" cannot be used here'\
                                       .format(fname))
                else:
                    return funcspec
        raise TypeSysError('function "{}" cannot be applied to ({});'
                           ' correct signature(s):\n    {}'\
                           .format(fname, ', '.join(argtype.value for argtype in argtypes),
                                   '\n    '.join(str(funcspec) for funcspec in self.decls[fname])))

class AttrSpec(CustomJSONSerializable):
    """Specification of an attribute in a :class:`RelType`.  See
    :ref:`Relation Schema and Attribute References` for an overview.

    """
    def __init__(self, rel: Optional[str], name: Optional[str], type: ValType):
        """Construct a :class:`AttrSpec`, given the name of the relation where
        the attribute originally comes from (optional), the name of
        the attribute (optional), and the type of the attribute.

        """
        assert rel is None or isinstance(rel, str)
        assert name is None or isinstance(name, str)
        assert isinstance(type, ValType)
        self.rel = rel
        self.name = name
        self.type = type
    def __str__(self):
        return '{}.{}:{}'.format('_' if self.rel is None else self.rel,
                                 '_' if self.name is None else self.name,
                                 self.type.value)
    def str_ref_only(self):
        return '{}.{}'.format('_' if self.rel is None else self.rel,
                              '_' if self.name is None else self.name)
    def str_name_and_type_only(self):
        return '{}:{}'.format('_' if self.name is None else self.name,
                              self.type.value)
    def can_be_confused_with(self, other: 'AttrSpec'):
        """Check if this :class:`AttrSpec` can be potentially confused with
        another one, if both are presented as possibilities when
        resolving an :class:`.AttrRef`.

        """
        return (self.rel == other.rel or self.rel is None or other.rel is None) and\
            (self.name == other.name)

class RelType(CustomJSONSerializable):
    def __init__(self, tmp, attrs):
        assert isinstance(tmp, int)
        assert all(isinstance(attr, AttrSpec) for attr in attrs)
        self.tmp = tmp
        self.attrs = attrs
    def __str__(self):
        return '{}({})'.format(self.tmp, ', '.join(str(attr) for attr in self.attrs))
    def str_attr_names_and_types(self):
        return [attr.str_name_and_type_only() for attr in self.attrs]
    def sql_rel(self):
        return 'rat{}'.format(self.tmp)
    def sql_attr(self, i):
        return 'a{}'.format(i)
    def sql_attrs(self):
        return [self.sql_attr(i) for i in range(len(self.attrs))]
