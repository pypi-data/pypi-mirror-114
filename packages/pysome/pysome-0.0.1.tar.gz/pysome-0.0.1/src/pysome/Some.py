import inspect
from collections import Iterable
from typing import Union, Callable, Any

from pysome.Exceptions import *


class Some:
    """
    Some() validates agains given arguments if any matches it equals
    if no argument is given Some always equals

    examples:
    >>> Some() == ...
    True
    >>> Some(int) == 1
    True
    >>> Some(str, int) == 21
    True
    >>> Some(int) == "abc"
    False
    """
    def __init__(self, *args: Union[type, Callable, "Some"]):
        self.types = []
        if args:
            for arg in args:
                if isinstance(arg, type):
                    self.types.append(arg)
                    continue
                elif isinstance(arg, Some):
                    self.types.append(arg)
                    continue
                elif callable(arg):
                    if len(inspect.signature(arg).parameters) != 1:
                        raise InvalidFunction("function must accept exactly one parameter")
                    self.types.append(arg)
                    continue
                raise InvalidArgument(f"Some accepts only objects of the types <type>, <Some> or a function but {arg} "
                                      f"is of type {type(arg)}")
        else:
            self.types = None

    def __eq__(self, other: Any):
        if self.types is None:
            return True
        # todo: what of other is also a Some is this something we want
        for t in self.types:
            if isinstance(t, type):
                if isinstance(other, t):
                    return True
            elif isinstance(t, Some):
                if t == other:
                    return True
            elif callable(t):
                eq = t(other)
                if not isinstance(eq, bool):
                    raise MustReturnBool(
                        f"validator function must return bool (True or False) but returned {eq} of type {type(eq)} "
                        "instead")
                if eq:
                    return True
        return False


class AllOf(Some):
    """
    AllOf validates against all given arguments an only equals if all match.

    examples:
    >>> AllOf(int) == 12
    True
    >>> AllOf(int, str) == 12
    False
    >>> AllOf(object, str) == "abc"
    True
    """
    def __init__(self, *args: Union[type, Callable, "Some"]):
        def validate_all(other):
            return all(Some(arg) == other for arg in args)
        super().__init__(validate_all)


class SomeIterable(Some):
    """
    SomeIterable equals all iterable objects that are equal to its given arguemnts

    example:
    >>> SomeIterable() == [1, 2, 3]
    True
    >>> SomeIterable() == 12
    False
    >>> SomeIterable(int) == (1, 2, 4)
    True
    >>> SomeIterable(str) == (1, 3, 4)
    False
    """
    # todo: first=None, last=None, nth=None,
    def __init__(self, *args: Union[type, Callable, "Some"], length=None, is_type=Iterable):
        def some_iterable_validator(others):
            if not isinstance(others, is_type):
                return False
            if length is not None and len(others) != length:
                return False
            some = Some(*args)

            return all(some == x for x in others)
        super().__init__(some_iterable_validator)


class SomeList(SomeIterable):
    """
    SomeList is just like SomeIterator but only True if other is of type 'list'

    examples
    >>> SomeList() == []
    True
    >>> SomeList() == [1, 2]
    True
    >>> SomeList() == (1, 2)
    False
    """
    # todo: test
    # todo: first=None, last=None, nth=None,
    def __init__(self, *args: Union[type, Callable, "Some"], length=None):
        super().__init__(*args, length=length, is_type=list)


class SomeDict(Some):
    # todo: test
    """
    SomeDict is equal to any dict

    examples:
    >>> SomeDict() == {}
    True
    >>> SomeDict() == {"a": {"a1": 1, "a2": 2}, "b": 3}
    True
    >>> SomeDict() == 12
    False
    """
    def __init__(self):
        super().__init__(dict)


class SomePartialDict(Some):
    # todo: test
    """
    SomePartialDict is equal to any dict that contains all keys and values that are given as a dict as argument

    examples
    >>> SomePartialDict({"a": 1}) == {"a": 1, "b": 2}
    True
    >>> SomePartialDict({"a": 2}) == {"a": 1, "b": 2}
    False
    """
    def __init__(self, arg=None):
        if arg is None:
            arg = {}

        def some_partial_dict_validator(other):
            if not isinstance(arg, dict):
                return False
            return all(item in other.items() for item in arg.items())

        super().__init__(some_partial_dict_validator)


# TODO: SOMES
# TODO: SomeStrict()
# TODO: SomeTuple(SomeIterator)
# TODO: SomeSet(SomeIterator)
# TODO: SomeCallable()
# TODO: SomeIn()
# TODO: SomeEmail()
# TODO: NotSome()
# TODO: AllOf()? other name but instead of one validator must be true all must be true
# TODO: SomeStr(regex=, pattern=Hal_o W__t, endswith=, startswith=)
# TODO: SomeNumber(min=, max=) -> Some(int, float, long...?)

class has_len(Some):
    """
    is true if other is in the given container

    examples:
    >>> has_len(2) == [1, 2]
    True
    >>> has_len(0) == []
    True
    >>> has_len(2) == (1, )
    False
    """

    def __init__(self, length=None, min_length=None, max_length=None):
        def len_validator(other):
            if not hasattr(other, '__len__'):
                return False
            if length:
                if not len(other) == length:
                    return False
            if min_length:
                if len(other) < min_length:
                    return False
            if max_length:
                if len(other) > max_length:
                    return False
            return True

        super().__init__(len_validator)


class is_in(Some):
    """
    is true if other is in the given container

    examples:
    >>> is_in({"a", "b"}) == "a"
    True
    >>> is_in(["a", "b"]) == "b"
    True
    >>> is_in({"a", "b"}) == "c"
    False
    """

    def __init__(self, container):
        if not hasattr(container, '__contains__'):
            raise InvalidArgument("is_in container doesn't implement __contains__")

        def is_in_validator(other):
            return other in container

        super().__init__(is_in_validator)


class has_attr(Some):
    """
    true if other has any of given attr(s)

    examples:
    >>> has_attr("split") == "a"
    True
    >>> has_attr("split") == 1
    False
    >>> has_attr("imag", "split") == "a"
    True
    >>> has_attr("imag", "real") == "a"
    False
    """
    def __init__(self, *args: Union[str]):
        def has_attr_validator(other):
            for attr in args:
                if hasattr(other, attr):
                    return True
            return False

        super().__init__(has_attr_validator)


class has_all_attr(Some):
    """
    true if other has all of given attr(s)

    examples:
    >>> has_all_attr("split") == "a"
    True
    >>> has_all_attr("split") == 1
    False
    >>> has_all_attr("split", "imag") == "a"
    False
    >>> has_all_attr("real", "imag") == 1
    True
    """

    def __init__(self, *args: Union[str]):
        def has_any_attr_validator(other):
            return all(hasattr(other, attr) for attr in args)

        super().__init__(has_any_attr_validator)

# TODO: is_callable()