"""
This module provides conditional dispatch support.
"""
import inspect
from itertools import chain, repeat

__all__ = ['run_cls', 'matches_types', 'arginize', 'correct_argspec',
           'matches_signature', 'ConditionalDispatch', 'fmt_argspec_types']


def run_cls(name):
    """
    run_cls("foo")(cls, *args, **kwargs) -> cls.foo(*args, **kwargs)
    """
    fun = lambda cls, *args, **kwargs: getattr(cls, name)(*args, **kwargs)
    fun.__name__ = str(name)
    fun.run_cls = True
    return fun


def matches_types(fun, types, args, kwargs):
    """
    See if args and kwargs match are instances of types.

    types are given in the order they are defined in the function. kwargs are automatically
    converted into that order.
    """
    return all(
        isinstance(obj, cls) for obj, cls in zip(
            arginize(fun, args, kwargs), types
        )
    )


def arginize(fun, a, kw):
    """
    Turn args and kwargs into args by considering the function signature.
    """
    args, varargs, keywords, defaults = correct_argspec(fun)
    if varargs is not None:
        raise ValueError
    names = args[len(a):]
    if defaults:
        defs = dict(zip(args[-len(defaults):], defaults))
    else:
        defs = {}
    return list(a) + [kw.get(name, defs.get(name, None)) for name in names]


def correct_argspec(fun):
    """
    Remove first argument if method is bound.
    """
    args, varargs, keywords, defaults = inspect.getargspec(fun)
    if inspect.ismethod(fun):
        args = args[1:]
    return args, varargs, keywords, defaults


def matches_signature(fun, a, kw):
    """
    Check whether function can be called with a as args and kw as kwargs.
    """
    args, varargs, keywords, defaults = correct_argspec(fun)
    if varargs is None and len(a) > len(args):
        return False
    skw = set(kw)
    sargs = set(args[len(a):])

    # There mayn't be unexpected parameters unless there is a **kwargs
    # in fun's signature.
    if keywords is None and skw - sargs != set():
        return False
    rest = set(args[len(a):])  - set(kw)

    # If there are any arguments that weren't passed but do not have
    # defaults, the signature does not match.
    defs = set() if defaults is None else set(defaults)
    if keywords is None and rest > defs:
        return False
    return True


class ConditionalDispatch(object):
    def __init__(self):
        self.funcs = []
        self.nones = []

    @classmethod
    def from_existing(cls, cond_dispatch):
        new = cls()
        new.funcs = cond_dispatch.funcs[:]
        new.nones = cond_dispatch.nones[:]
        return new

    def add_dec(self, condition):
        def _dec(fun):
            self.add(fun, condition)
            return fun
        return _dec

    def add(self, fun, condition=None, types=None, check=True):
        """
        Add fun to ConditionalDispatch under the condition that the arguments must match.

        If condition is left out, the function is executed for every input that matches the
        signature. Functions are considered in the order they are added, but ones with
        condition=None are considered as the last: that means, a function with condition None serves
        as an else branch for that signature. conditions must be mutually exclusive because
        otherwise which will be executed depends on the order they are added in. Function signatures
        of fun and condition must match (if fun is bound, the bound parameter needs to be left out
        in condition).
        """
        if condition is None:
            self.nones.append((fun, types))
        elif check and correct_argspec(fun) != correct_argspec(condition):
            raise ValueError(
                "Signature of condition must match signature of fun."
            )
        else:
            self.funcs.append((fun, condition, types))

    def __call__(self, *args, **kwargs):
        matched = False
        for fun, condition, types in self.funcs:
            if (matches_signature(condition, args, kwargs) and
               (types is None or matches_types(condition, types, args, kwargs))):
                matched = True
                if condition(*args, **kwargs):
                    return fun(*args, **kwargs)
        for fun, types in self.nones:
            if (matches_signature(fun, args, kwargs) and
               (types is None or matches_types(fun, types, args, kwargs))):
                return fun(*args, **kwargs)

        if matched:
            raise TypeError(
                "Your input did not fulfill the condition for any function."
            )
        else:
            raise TypeError(
                "There are no functions matching your input parameter "
                "signature."
            )

    def wrapper(self):
        return lambda *args, **kwargs: self(*args, **kwargs)

    def get_signatures(self, prefix="", start=0):
        """
        Return an iterator containing all possible function signatures. If prefix is given, use it
        as function name in signatures, else leave it out. If start is given, leave out first n
        elements.

        If start is -1, leave out first element if the function was created by run_cls.
        """
        for fun, condition, types in self.funcs:
            if start == -1:
                st = getattr(fun, 'run_cls', 0)
            else:
                st = start

            if types is not None:
                yield prefix + fmt_argspec_types(condition, types, st)
            else:
                args, varargs, keywords, defaults = correct_argspec(condition)
                args = args[st:]
                yield prefix + inspect.formatargspec(
                    args, varargs, keywords, defaults
                )

        for fun, types in self.nones:
            if types is not None:
                yield prefix + fmt_argspec_types(fun, types, st)
            else:
                args, varargs, keywords, defaults = correct_argspec(condition)
                args = args[st:]
                yield prefix + inspect.formatargspec(
                    args, varargs, keywords, defaults
                )

    def generate_docs(self):
        fns = (item[0] for item in chain(self.funcs, self.nones))
        return '\n\n'.join("{0} -> :py:meth:`{1}`".format(sig, fun.__name__)
            for sig, fun in
            # The 1 prevents the cls from incorrectly being shown in the
            # documentation.
            zip(self.get_signatures("create", -1), fns)
        )


def fmt_argspec_types(fun, types, start=0):
    args, varargs, keywords, defaults = correct_argspec(fun)

    args = args[start:]
    types = types[start:]

    NULL = object()
    if defaults is None:
        defaults = []
    defs = chain(repeat(NULL, len(args) - len(defaults)), defaults)

    spec = []
    for key, value, type_ in zip(args, defs, types):
        # This is a work around for a bug introduced during Python 3 porting.
        # for some reason the type was being passed in as a length 1 tuple.
        # This extracts the type under that condition. SM 6/10/15
        if isinstance(type_, tuple) and len(type_) == 1:
            type_ = type_[0]
        if value is NULL:
            spec.append("{0}: {1}".format(key, type_.__name__))
        else:
            spec.append("{0}: {1} = {2}".format(key, type_.__name__, value))
    if varargs is not None:
        spec.append('*{!s}'.format(varargs))
    if keywords is not None:
        spec.append('**{!s}'.format(keywords))
    return '(' + ', '.join(spec) + ')'
