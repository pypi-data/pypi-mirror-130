"""NanamiLang BuiltinMacros and BuiltinFunctions classes"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import functools
import time
from functools import reduce
from typing import List

from nanamilang import fn, datatypes
from nanamilang.shortcuts import (
    ASSERT_COLL_LENGTH_IS_EVEN, ASSERT_EVERY_COLLECTION_ITEM_EQUALS_TO,
    ASSERT_DICT_CONTAINS_KEY, ASSERT_IS_INSTANCE_OF, ASSERT_NO_DUPLICATES
)
from nanamilang.shortcuts import randstr, plain2partitioned
from nanamilang.spec import Spec


def meta(data: dict):
    """
    NanamiLang, apply meta data to a function
    'name': fn or macro LISP name
    'type': 'macro' or 'function'
    'forms': possible fn or macro possible forms
    'docstring': what fn or macro actually does?
    May contain 'hidden' (do not show in completions)
    May contain 'spec' attribute, but its not required

    :param data: a function meta data Python dictionary
    """

    def wrapped(_fn):
        @functools.wraps(_fn)
        def function(*args, **kwargs):
            spec = data.get('spec')
            if spec:
                if data.get('type') == 'macro':
                    Spec.validate(data.get('name'), args[1], spec)
                else:
                    Spec.validate(data.get('name'), args[0], spec)

            return _fn(*args, **kwargs)

        # TODO: maybe also implement spec linting

        ASSERT_DICT_CONTAINS_KEY('name', data, 'function meta data must contain a name')
        ASSERT_DICT_CONTAINS_KEY('type', data, 'function meta data must contain a type')
        ASSERT_DICT_CONTAINS_KEY('forms', data, 'function meta data must contain a forms')
        ASSERT_DICT_CONTAINS_KEY('docstring', data, 'function meta data must contain a docstring')

        function.meta = data

        return function

    return wrapped


class LetUnableAssignToError(Exception):
    """
    NanamiLang Let Error
    Unable assign to error
    """

    _target = None

    def __init__(self, to, *args):
        """NanamiLang LetUnableAssignToError"""

        self._target = to

        super(LetUnableAssignToError).__init__(*args)

    def __str__(self):
        """NanamiLang LetUnableAssignToError"""

        return f'let: unable to assign to {self._target}'


class LetDestructuringError(Exception):
    """
    NanamiLang Let Error

    """

    _reason: str = None
    Reason_LeftSideIsNotAVector: str = 'left side needs to be a Vector'
    Reason_RightSideIsNotAVector: str = 'right side needs to be a Vector'
    Reason_LeftAndRightLensUnequal: str = 'left and right sides lengths are unequal'

    def __init__(self, reason, *args):
        """NanamiLang LetDestructuringError"""

        self._reason = reason

        super(LetDestructuringError).__init__(*args)

    def __str__(self):
        """NanamiLang LetUnableAssignToError"""

        return f'let: an error has been occurred while destructuring: {self._reason}'


class BuiltinMacros:
    """NanamiLang Builtin Macros"""

    cached = {}

    ########################################################################################################

    @staticmethod
    def resolve(mc_name: str) -> dict:
        """Resolve macro by its name"""

        if fun := BuiltinMacros.cached.get(mc_name, {}):
            return fun
        for macro in BuiltinMacros.functions():
            if macro.meta.get('name') == mc_name:
                resolved: dict = {'macro_name': mc_name,
                                  'macro_reference': macro}
                BuiltinMacros.cached.update({mc_name: resolved})
                return resolved
        return {}

    @staticmethod
    def names() -> list:
        """Return LISP names"""

        return [_.meta.get('name') for _ in BuiltinMacros.functions()]

    @staticmethod
    def functions() -> list:
        """Return all _macro functions"""

        attrib_names = filter(lambda _: '_macro' in _, BuiltinMacros().__dir__())

        return list(map(lambda n: getattr(BuiltinMacros, n, None), attrib_names))

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'cond',
           'type': 'macro',
           'forms': ['(cond cond1 expr1 ... condN exprN)'],
           'docstring': 'Allows you to describe condition-expr pairs'})
    def cond_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'cond' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        for [condition, expr] in plain2partitioned(tree_slice):
            if ev_func(env,
                       (condition
                        if isinstance(condition, list)
                        else [token_cls(token_cls.Identifier, 'identity'),
                              condition])).reference() is True:
                return expr \
                    if isinstance(expr, list) \
                    else [token_cls(token_cls.Identifier, 'identity'), expr]
        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->',
           'type': 'macro',
           'forms': ['(-> form1 form2 ... formN)'],
           'docstring': 'Allows you to write your code as a pipeline of functions and macros calls'})
    def first_threading_macro(token_cls, tree_slice: list, *args) -> list:
        """
        Builtin '->' macro implementation

        :param tree_slice: slice of encountered tree
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        if len(tree_slice) > 1:

            for idx, tof in enumerate(tree_slice):
                if len(tree_slice) - 1 != idx:
                    if not isinstance(tof, list):
                        tof = [token_cls(token_cls.Identifier, 'identity'),
                               tof]
                    next_tof = tree_slice[idx + 1]
                    if not isinstance(next_tof, list):
                        tree_slice[idx + 1] = [next_tof, tof]
                    else:
                        tree_slice[idx + 1].insert(1, tof)

            return tree_slice[-1]

        return [token_cls(token_cls.Identifier, 'identity'), tree_slice[-1]]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': '->>',
           'type': 'macro',
           'forms': ['(->> form1 form2 ... formN)'],
           'docstring': 'Allows you to write your code as a pipeline of functions and macros calls'})
    def last_threading_macro(token_cls, tree_slice: list, *args) -> list:
        """
        Builtin '->>' macro implementation

        :param tree_slice: slice of encountered tree
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        if len(tree_slice) > 1:

            for idx, tof in enumerate(tree_slice):
                if len(tree_slice) - 1 != idx:
                    if not isinstance(tof, list):
                        tof = [token_cls(token_cls.Identifier, 'identity'),
                               tof]
                    next_tof = tree_slice[idx + 1]
                    if not isinstance(next_tof, list):
                        tree_slice[idx + 1] = [next_tof, tof]
                    else:
                        tree_slice[idx + 1].append(tof)

            return tree_slice[-1]

        return [token_cls(token_cls.Identifier, 'identity'), tree_slice[-1]]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'measure',
           'type': 'macro',
           'forms': ['(measure ...)'],
           'docstring': 'Allows you to measure how long it takes for your code to evaluate'})
    def measure_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'measure' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        started = time.perf_counter()

        ev_func(env, tree_slice)

        finished = time.perf_counter()

        return [token_cls(token_cls.Identifier, 'identity'),
                token_cls(token_cls.String, f'Took {round(finished - started, 2)} s')]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 3]],
           'name': 'if',
           'type': 'macro',
           'forms': ['(if condition true-branch else-branch)'],
           'docstring': 'Returns true- or else-branch depending on condition'})
    def if_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'if' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        condition, true_branch, else_branch = tree_slice

        if not isinstance(condition, list):
            condition = [token_cls(token_cls.Identifier, 'identity'), condition]
        if not isinstance(true_branch, list):
            true_branch = [token_cls(token_cls.Identifier, 'identity'), true_branch]
        if not isinstance(else_branch, list):
            else_branch = [token_cls(token_cls.Identifier, 'identity'), else_branch]

        return true_branch if ev_func(env, condition).reference() is True else else_branch

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'comment',
           'type': 'macro',
           'forms': ['(comment ...)'],
           'docstring': 'Allows you to replace entire form with just Nil'})
    def comment_macro(token_cls, *args) -> list:
        """
        Builtin 'comment' macro implementation

        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne]],
           'name': 'and',
           'type': 'macro',
           'forms': ['(and cond1 cond2 ... condN)'],
           'docstring': 'Returns false if the next cond evaluates to false, otherwise true'})
    def and_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'and' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        for condition in tree_slice:
            if not isinstance(condition, list):
                condition = [token_cls(token_cls.Identifier, 'identity'), condition]
            if ev_func(env, condition).reference() is False:
                return [token_cls(token_cls.Identifier, 'identity'),
                        token_cls(token_cls.Boolean, False)]
        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Boolean, True)]

    ########################################################################################################

    @staticmethod
    @meta({'spec': ((Spec.ArityAtLeastOne,),),
           'name': 'or',
           'type': 'macro',
           'forms': ['(or cond1 cond2 ... condN)'],
           'docstring': 'Returns true if the next cond evaluates to true, otherwise false'})
    def or_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'or' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        for condition in tree_slice:
            if not isinstance(condition, list):
                condition = [token_cls(token_cls.Identifier, 'identity'), condition]
            if ev_func(env, condition).reference() is True:
                return [token_cls(token_cls.Identifier, 'identity'),
                        token_cls(token_cls.Boolean, True)]
        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Boolean, False)]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityVariants, [2, 3]]],
           'name': 'fn',
           'type': 'macro',
           'forms': ['(fn [n ...] f)',
                     '(fn name [n ...] f)'],
           'docstring': 'Allows you to declare your anonymous NanamiLang function, maybe named'})
    def fn_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'fn' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        name_token, parameters_form, body_token_or_form = [None] * 3

        if len(tree_slice) == 2:
            parameters_form, body_token_or_form = tree_slice
        elif len(tree_slice) == 3:
            name_token, parameters_form, body_token_or_form = tree_slice
            assert not isinstance(name_token, list), 'fn: name needs to be a token, not a form'
            assert name_token.type() == token_cls.Identifier, 'fn: name needs to be an Identifier'

        ASSERT_IS_INSTANCE_OF(parameters_form, list, 'fn: parameters form needs to be a Vector')

        # TODO: destructuring support
        assert len(list(filter(lambda x: isinstance(x, list), parameters_form))) == 0, (
            'fn: every element of parameters form needs to be a Token, not a form, no destruction.'
        )

        but_first = parameters_form[1:]

        ASSERT_EVERY_COLLECTION_ITEM_EQUALS_TO(
            [x.type() for x in but_first], token_cls.Identifier,
            'fn: each element of parameters form needs to be an Identifier')

        parameters_form = [t.dt().origin() for t in but_first]

        ASSERT_NO_DUPLICATES(parameters_form, 'fn: parameters form could not contain duplicates')

        name = name_token.dt().origin() if name_token else randstr()

        handler = fn.Fn(env, name, ev_func, token_cls, parameters_form, body_token_or_form)
        # Pylint will not be happy, but we can use lambda here and don't have any problems with it
        function_reference = lambda args: handler.handle(tuple(args))

        function_reference.meta = {
            'name': name, 'docstring': '',
            'type': 'function', 'forms': handler.generate_meta__forms()
        }

        _env = {name: datatypes.Function({'function_name': name,
                                          'function_reference': function_reference})}
        # Update local env, so ev_func() will later know about function that has been 'defined'
        env.update(_env)
        handler.env().update(_env)

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Identifier, name)]

    ########################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': 'let',
           'type': 'macro',
           'forms': ['(let [b1 v1 ...] b1)'],
           'docstring': 'Allows you to declare local bindings and then access them in a pretty easy way'})
    def let_macro(token_cls, tree_slice: list, env: dict, ev_func) -> list:
        """
        Builtin 'let' macro implementation

        :param tree_slice: slice of encountered tree
        :param env: current environment during evaluation
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        bindings_form, body_form = tree_slice

        but_first = bindings_form[1:]

        ASSERT_COLL_LENGTH_IS_EVEN(but_first,
                                   'let: bindings form must be even')

        for [key_token_or_form, value_token_or_form] in plain2partitioned(but_first):
            evaluated_value = ev_func(
                env,
                value_token_or_form
                if isinstance(value_token_or_form, list)
                else [token_cls(token_cls.Identifier, 'identity'), value_token_or_form])
            if isinstance(key_token_or_form, token_cls) and key_token_or_form.type() == token_cls.Identifier:
                env[key_token_or_form.dt().origin()] = evaluated_value
            elif isinstance(key_token_or_form, list):
                if not key_token_or_form[0].dt().origin() == 'make-vector':
                    raise LetDestructuringError(LetDestructuringError.Reason_LeftSideIsNotAVector)
                if not isinstance(evaluated_value, datatypes.Vector):
                    raise LetDestructuringError(LetDestructuringError.Reason_RightSideIsNotAVector)
                if not len(key_token_or_form[1:]) == len(evaluated_value.reference()):
                    raise LetDestructuringError(LetDestructuringError.Reason_LeftAndRightLensUnequal)
                for from_left, from_right in zip(key_token_or_form[1:], evaluated_value.reference()):
                    if isinstance(from_left, token_cls) and from_left.type() == token_cls.Identifier:
                        env[from_left.dt().origin()] = from_right
                    else:
                        raise LetUnableAssignToError(from_right)
            else:
                raise LetUnableAssignToError(key_token_or_form)

        return body_form if isinstance(body_form, list) else [token_cls(token_cls.Identifier, 'identity'), body_form]


class BuiltinFunctions:
    """NanamiLang Builtin Functions"""

    #################################################################################################################

    @staticmethod
    def install(fn_meta: dict, fn_callback) -> bool:
        """
        Allow others to install own functions.
        For example: let the REPL install (exit) function

        :param fn_meta: required function meta information
        :param fn_callback: installed function callback reference
        """

        reference_key = f'{fn_meta.get("name")}_func'
        maybe_existing = getattr(BuiltinFunctions, reference_key, None)
        if maybe_existing:
            delattr(BuiltinFunctions, reference_key)

        setattr(BuiltinFunctions, reference_key, fn_callback)
        getattr(BuiltinFunctions, reference_key, None).meta = fn_meta
        return bool(getattr(BuiltinFunctions, reference_key, None).meta == fn_meta)

    #################################################################################################################

    cached = {}

    @staticmethod
    def resolve(fn_name: str) -> dict:
        """Resolve function by its name"""

        if fun := BuiltinMacros.cached.get(fn_name, {}):
            return fun
        for func in BuiltinFunctions.functions():
            if func.meta.get('name') == fn_name:
                resolved: dict = {'function_name': fn_name,
                                  'function_reference': func}
                BuiltinFunctions.cached.update({fn_name: resolved})
                return resolved
        return {}

    @staticmethod
    def names() -> list:
        """Return LISP names"""

        return [_.meta.get('name') for _ in BuiltinFunctions.functions()]

    @staticmethod
    def functions() -> list:
        """Return all _func functions"""

        attrib_names = filter(lambda _: '_func' in _, BuiltinFunctions().__dir__())

        return list(map(lambda n: getattr(BuiltinFunctions, n, None), attrib_names))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'identity',
           'type': 'function',
           'forms': ['(identity something)'],
           'docstring': 'Returns something as it is'})
    def identity_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'identity' function implementation

        :param args: incoming 'identity' function arguments
        :return: datatypes.Base
        """

        something: datatypes.Base = args[0]

        return something

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [(datatypes.Set, datatypes.Base),
                                                       (datatypes.Vector, datatypes.IntegerNumber),
                                                       (datatypes.HashMap, datatypes.Base),
                                                       (datatypes.NException, datatypes.Keyword)]]],
           'name': 'get',
           'type': 'function',
           'forms': ['(get collection by)'],
           'docstring': 'Returns collection element by key (HashMap), index (Vector), element (Set)'})
    def get_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'get' function implementation

        :param args: incoming 'get' function arguments
        :return: datatypes.Base
        """

        collection: datatypes.Collection
        by: datatypes.Base

        collection, by = args

        return collection.get(by)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Collection]],
           'name': 'count',
           'type': 'function',
           'forms': ['(count collection)'],
           'docstring': 'Returns elements count of passed collection'})
    def count_func(args: List[datatypes.Collection]) -> datatypes.IntegerNumber:
        """
        Builtin 'count' function implementation

        :param args: incoming 'count' function arguments
        :return: datatypes.IntegerNumber
        """

        collection: datatypes.Collection = args[0]

        return collection.count()

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.Collection]],
           'name': 'empty?',
           'type': 'function',
           'forms': ['(empty? collection)'],
           'docstring': 'Whether passed collection is empty or not'})
    def is_empty_func(args: List[datatypes.Collection]) -> datatypes.Boolean:
        """
        Builtin 'empty?' function implementation

        :param args: incoming 'empty?' function arguments
        :return: datatypes.Boolean
        """

        collection: datatypes.Collection = args[0]

        return collection.is_empty()

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-set',
           'type': 'function',
           'forms': ['(make-set e1 e2 ... eX)'],
           'docstring': 'Creates a Set data structure'})
    def make_set_func(args: List[datatypes.Base]) -> datatypes.Set:
        """
        Builtin 'make-set' function implementation

        :param args: incoming 'make-set' function arguments
        :return: datatypes.Set
        """

        return datatypes.Set(tuple(args))

    #################################################################################################################

    @staticmethod
    @meta({'spec': None,
           'name': 'make-vector',
           'type': 'function',
           'forms': ['(make-vector e1 e2 ... eX)'],
           'docstring': 'Creates a Vector data structure'})
    def make_vector_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'make-vector' function implementation

        :param args: incoming 'make-vector' function arguments
        :return: datatypes.Vector
        """

        return datatypes.Vector(tuple(args))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityEven]],
           'name': 'make-hashmap',
           'type': 'function',
           'forms': ['(make-hashmap k1 v2 ... kX vX)'],
           'docstring': 'Creates a HashMap data structure'})
    def make_hashmap_func(args: List[datatypes.Base]) -> datatypes.HashMap:
        """
        Builtin 'make-hashmap' function implementation

        :param args: incoming 'make-hashmap' function arguments
        :return: datatypes.HashMap
        """

        return datatypes.HashMap(tuple(args))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1]],
           'name': 'type',
           'type': 'function',
           'forms': ['(type something)'],
           'docstring': 'Returns something type name as String'})
    def type_func(args: List[datatypes.Base]) -> datatypes.String:
        """
        Builtin 'type' function implementation

        :param args: incoming 'type' function arguments
        :return: datatypes.String
        """

        something: datatypes.Base = args[0]

        return datatypes.String(something.name)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2]],
           'name': '=',
           'type': 'function',
           'forms': ['(= first second)'],
           'docstring': 'Whether first equals to second or not'})
    def eq_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin '=' function implementation

        :param args: incoming '=' function arguments
        :return: datatypes.Boolean
        """

        # TODO: refactor: more than two arguments support

        first: datatypes.Base
        second: datatypes.Base
        first, second = args

        return datatypes.Boolean(first.hashed() == second.hashed())

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '<',
           'type': 'function',
           'forms': ['(< first second)'],
           'docstring': 'Whether first less than second or not'})
    def less_than_func(
            args: (List[datatypes.IntegerNumber] or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '<' function implementation

        :param args: incoming '<' function arguments
        :return: datatypes.Boolean
        """

        # TODO: refactor: more than two arguments support

        first: datatypes.IntegerNumber or datatypes.FloatNumber
        second: datatypes.IntegerNumber or datatypes.FloatNumber
        first, second = args

        return datatypes.Boolean(first.reference() < second.reference())

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '>',
           'type': 'function',
           'forms': ['(> first second)'],
           'docstring': 'Whether first greater than second or not'})
    def greater_than_func(
            args: (List[datatypes.IntegerNumber] or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '>' function implementation

        :param args: incoming '>' function arguments
        :return: datatypes.Boolean
        """

        # TODO: refactor: more than two arguments support

        first: datatypes.IntegerNumber or datatypes.FloatNumber
        second: datatypes.IntegerNumber or datatypes.FloatNumber
        first, second = args

        return datatypes.Boolean(first.reference() > second.reference())

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '<=',
           'type': 'function',
           'forms': ['(<= first second)'],
           'docstring': 'Whether first less than or equals to second or not'})
    def less_than_eq_func(
            args: (List[datatypes.IntegerNumber] or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '<=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        # TODO: refactor: more than two arguments support

        first: datatypes.IntegerNumber or datatypes.FloatNumber
        second: datatypes.IntegerNumber or datatypes.FloatNumber
        first, second = args

        return datatypes.Boolean(first.reference() <= second.reference())

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '>=',
           'type': 'function',
           'forms': ['(>= first second)'],
           'docstring': 'Whether first greater than or equals to second or not'})
    def greater_than_eq_func(
            args: (List[datatypes.IntegerNumber] or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '>=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        # TODO: refactor: more than two arguments support

        first: datatypes.IntegerNumber or datatypes.FloatNumber
        second: datatypes.IntegerNumber or datatypes.FloatNumber
        first, second = args

        return datatypes.Boolean(first.reference() >= second.reference())

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.String]],
           'name': 'find-mc',
           'type': 'function',
           'forms': ['(find-mc mc-name)'],
           'docstring': 'Returns a Macro by its own LISP name'})
    def find_mc_func(args: List[datatypes.String]
                     ) -> datatypes.Macro or datatypes.Nil:
        """
        Builtin 'find-mc' function implementation

        :param args: incoming 'find-mc' function arguments
        :return: datatypes.Macro or datatypes.Nil
        """

        mc_name: datatypes.String = args[0]

        resolved = BuiltinMacros.resolve(mc_name.reference())

        return datatypes.Macro(resolved) if resolved else datatypes.Nil('nil')

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeIs, datatypes.String]],
           'name': 'find-fn',
           'type': 'function',
           'forms': ['(find-fn fn-name)'],
           'docstring': 'Returns a Function by its own LISP name'})
    def find_fn_func(args: List[datatypes.String]
                     ) -> datatypes.Function or datatypes.Nil:
        """
        Builtin 'find-fn' function implementation

        :param args: incoming 'find-fn' function arguments
        :return: datatypes.Function or datatypes.Nil
        """

        fn_name: datatypes.String = args[0]

        resolved = BuiltinFunctions.resolve(fn_name.reference())

        return datatypes.Function(resolved) if resolved else datatypes.Nil('nil')

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants,
                     [[datatypes.IntegerNumber, datatypes.Base]]]],
           'name': 'repeat',
           'type': 'function',
           'forms': ['(repeat times something)'],
           'docstring': 'Vector of something repeated as many times as specified'})
    def repeat_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'repeat' function implementation

        :param args: incoming 'repeat' function arguments
        :return: datatypes.Base
        """

        times: datatypes.IntegerNumber
        something: datatypes.Base

        times, something = args

        return datatypes.Vector(tuple(something for _ in range(times.reference())))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': 'inc',
           'type': 'function',
           'forms': ['(inc number)'],
           'docstring': 'Returns incremented number'})
    def inc_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin 'inc' function implementation

        :param args: incoming 'inc' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        number: (datatypes.IntegerNumber or datatypes.FloatNumber) = args[0]

        return datatypes.IntegerNumber(number.reference() + 1) if \
            isinstance(number, datatypes.IntegerNumber) else datatypes.FloatNumber(number.reference() + 1)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': 'dec',
           'type': 'function',
           'forms': ['(dec number)'],
           'docstring': 'Returns decremented number'})
    def dec_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin 'dec' function implementation

        :param args: incoming 'dec' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        number: (datatypes.IntegerNumber or datatypes.FloatNumber) = args[0]

        return datatypes.IntegerNumber(number.reference() - 1) if \
            isinstance(number, datatypes.IntegerNumber) else datatypes.FloatNumber(number.reference() - 1)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '+',
           'type': 'function',
           'forms': ['(+ n1 n2 ... nX)'],
           'docstring': 'Applies "+" operation to all passed numbers'})
    def add_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin '+' function implementation

        :param args: incoming '+' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ + x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '-',
           'type': 'function',
           'forms': ['(- n1 n2 ... nX)'],
           'docstring': 'Applies "-" operation to all passed numbers'})
    def sub_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin '-' function implementation

        :param args: incoming '-' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ - x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '*',
           'type': 'function',
           'forms': ['(* n1 n2 ... nX)'],
           'docstring': 'Applies "*" operation to all passed numbers'})
    def mul_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin '*' function implementation

        :param args: incoming '*' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ * x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': '/',
           'type': 'function',
           'forms': ['(/ n1 n2 ... nX)'],
           'docstring': 'Applies "/" operation to all passed numbers'})
    def divide_func(args: (List[datatypes.IntegerNumber]
                           or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                or datatypes.FloatNumber):
        """
        Builtin '/' function implementation

        :param args: incoming '/' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ / x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityAtLeastOne],
                    [Spec.EachArgumentTypeVariants, (datatypes.IntegerNumber, datatypes.FloatNumber)]],
           'name': 'mod',
           'type': 'function',
           'forms': ['(mod n1 n2 ... nX)'],
           'docstring': 'Applies "mod" operation to all passed numbers'})
    def modulo_func(args: (List[datatypes.IntegerNumber]
                           or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                or datatypes.FloatNumber):
        """
        Builtin 'mod' function implementation

        :param args: incoming 'mod' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        result = reduce(lambda _, x: _ % x, map(lambda n: n.reference(), args))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'map',
           'type': 'function',
           'forms': ['(map function collection)'],
           'docstring': 'Allows to map collection elements with the passed function which returns a Base'})
    def map_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'map' function implementation

        :param args: incoming 'map' function arguments
        :return: datatypes.Vector
        """

        function: datatypes.Function or datatypes.Keyword
        collection: datatypes.Collection

        function, collection = args

        if isinstance(function, datatypes.Keyword):
            k = function
            function = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        return datatypes.Vector(tuple(map(lambda element: function.reference()([element]), collection.elements())))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 2],
                    [Spec.ArgumentsTypeChainVariants, [[datatypes.Function, datatypes.Collection],
                                                       [datatypes.Keyword, datatypes.Collection]]]],
           'name': 'filter',
           'type': 'function',
           'forms': ['(filter function collection)'],
           'docstring': 'Allows to filter collection elements with the passed function which returns a Boolean'})
    def filter_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'filter' function implementation

        :param args: incoming 'filter' function arguments
        :return: datatypes.Vector
        """

        fun: datatypes.Function or datatypes.Keyword
        coll: datatypes.Collection

        fun, coll = args

        if isinstance(fun, datatypes.Keyword):
            k = fun
            fun = datatypes.Function(
                {'function_name': randstr(),
                 'function_reference': lambda _a_: BuiltinFunctions.get_func(_a_ + [k])})

        return datatypes.Vector(tuple(filter(lambda e: fun.reference()([e]).reference() is True, coll.elements())))

    #################################################################################################################

    @staticmethod
    @meta({'spec': [[Spec.ArityIs, 1],
                    [Spec.EachArgumentTypeVariants, (datatypes.Macro, datatypes.Function)]],
           'name': 'doc',
           'type': 'function',
           'forms': ['(doc function-or-macro)'],
           'docstring': 'Allows you to lookup for a Function or a Macro documentation, represented as a HashMap'})
    def doc_func(args: List[datatypes.Macro or datatypes.Function]) -> datatypes.HashMap:
        """
        Builtin 'doc' function implementation

        :param args: incoming 'doc' function arguments
        :return: datatypes.HashMap
        """

        function_or_macro: datatypes.Macro or datatypes.Function = args[0]

        t = function_or_macro.reference().meta.get('type')

        return datatypes.HashMap(
            (datatypes.Keyword('forms'),
             datatypes.Vector(
                 tuple(datatypes.String(_) for _ in function_or_macro.reference().meta.get('forms'))),
             datatypes.Keyword('macro?'), datatypes.Boolean(t == 'macro'),
             datatypes.Keyword('function?'), datatypes.Boolean(t == 'function'),
             datatypes.Keyword('docstring'), datatypes.String(function_or_macro.reference().meta.get('docstring'))))

    #################################################################################################################
