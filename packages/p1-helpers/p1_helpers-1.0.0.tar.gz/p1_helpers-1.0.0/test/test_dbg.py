import logging
import unittest

import p1_helpers.dbg as dbg

_LOG = logging.getLogger(__name__)


# #############################################################################


class Test_dassert1(unittest.TestCase):
    def test1(self) -> None:
        dbg.dassert(True)

    def test2(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
cond=False
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert(False)
        self.assertEqual(fixture, str(cm.exception))

    def test3(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
cond=False
hello
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert(False, msg="hello")
        self.assertEqual(fixture, str(cm.exception))

    def test4(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
cond=False
hello world
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert(False, "hello %s", "world")
        self.assertEqual(fixture, str(cm.exception))

    def test5(self) -> None:
        """
        Too many params.
        """
        fixture = """
################################################################################
* Failed assertion *
cond=False
Caught assertion while formatting message:
'not all arguments converted during string formatting'
hello %s world too_many
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert(False, "hello %s", "world", "too_many")
        self.assertEqual(fixture, str(cm.exception))

    def test6(self) -> None:
        """
        Not enough params.
        """
        fixture = """
################################################################################
* Failed assertion *
cond=False
Caught assertion while formatting message:
'not enough arguments for format string'
hello %s 
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert(False, "hello %s")
        self.assertEqual(fixture, str(cm.exception))


# #############################################################################


class Test_dassert_eq1(unittest.TestCase):
    def test1(self) -> None:
        dbg.dassert_eq(1, 1)

    def test2(self) -> None:
        dbg.dassert_eq(1, 1, msg="hello world")

    def test3(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
'1'
==
'2'
hello world
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert_eq(1, 2, msg="hello world")
        self.assertEqual(fixture, str(cm.exception))

    def test4(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
'1'
==
'2'
hello world
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert_eq(1, 2, "hello %s", "world")
        self.assertEqual(fixture, str(cm.exception))

    def test5(self) -> None:
        """
        Raise assertion with incorrect message.
        """
        fixture = """
################################################################################
* Failed assertion *
'1'
==
'2'
Caught assertion while formatting message:
'not enough arguments for format string'
hello %s 
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert_eq(1, 2, "hello %s")
        self.assertEqual(fixture, str(cm.exception))


# #############################################################################


class Test_dassert_misc1(unittest.TestCase):
    def test1(self) -> None:
        dbg.dassert_in("a", "abc")

    def test2(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
'a' in '['xyz']'
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert_in("a", "xyz".split())
        self.assertEqual(fixture, str(cm.exception))

    # dassert_is

    def test3(self) -> None:
        a = None
        dbg.dassert_is(a, None)

    def test4(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
'a' is 'None'
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert_is("a", None)
        self.assertEqual(fixture, str(cm.exception))

    # dassert_isinstance

    def test5(self) -> None:
        dbg.dassert_isinstance("a", str)

    def test6(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
instance of 'a' is '<class 'str'>' instead of '<class 'int'>'
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            dbg.dassert_isinstance("a", int)
        self.assertEqual(fixture, str(cm.exception))

    # dassert_set_eq

    def test7(self) -> None:
        a = [1, 2, 3]
        b = [2, 3, 1]
        dbg.dassert_set_eq(a, b)

    def test8(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
val1 - val2={3}
val2 - val1=set()
val1={1, 2, 3}
set eq
val2={1, 2}
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            a = [1, 2, 3]
            b = [2, 2, 1]
            dbg.dassert_set_eq(a, b)
        self.assertEqual(fixture, str(cm.exception))

    def test9(self) -> None:
        a = [1, 2]
        b = [2, 1, 3]
        dbg.dassert_issubset(a, b)

    def test10(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
val1={1, 2, 3}
issubset
val2={1, 2, 4}
val1 - val2={3}
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            a = [1, 2, 3]
            b = [4, 2, 1]
            dbg.dassert_issubset(a, b)
        self.assertEqual(fixture, str(cm.exception))

    # dassert_not_intersection

    def test11(self) -> None:
        a = [1, 2, 3]
        b = [4, 5]
        dbg.dassert_not_intersection(a, b)

    def test12(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
val1={1, 2, 3}
has no intersection
val2={1, 2, 4}
val1 - val2={3}
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            a = [1, 2, 3]
            b = [4, 2, 1]
            dbg.dassert_not_intersection(a, b)
        self.assertEqual(fixture, str(cm.exception))

    # dassert_no_duplicates

    def test13(self) -> None:
        a = [1, 2, 3]
        dbg.dassert_no_duplicates(a)

    def test14(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
val1=[1, 3, 3]
has duplicates
3
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            a = [1, 3, 3]
            dbg.dassert_no_duplicates(a)
        self.assertEqual(fixture, str(cm.exception))

    # dassert_eq_all

    def test15(self) -> None:
        a = [1, 2, 3]
        b = [1, 2, 3]
        dbg.dassert_eq_all(a, b)

    def test16(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
val1=3
[1, 2, 3]
val2=3
[1, 2, 4]
################################################################################
"""
        with self.assertRaises(AssertionError) as cm:
            a = [1, 2, 3]
            b = [1, 2, 4]
            dbg.dassert_eq_all(a, b)
        self.assertEqual(fixture, str(cm.exception))

    def test17(self) -> None:
        dbg.dassert_has_attr(list(), "__getitem__")

    def test18(self) -> None:
        fixture = """
################################################################################
* Failed assertion *
obj has no attribute: 'some_name'
obj attributes: ['__module__', '__dict__', '__weakref__', '__doc__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__init__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']'
Dummy class has no 'some_name' attribute.
################################################################################
"""

        class Dummy:
            pass

        with self.assertRaises(AssertionError) as cm:
            attribute_name = "some_name"
            dbg.dassert_has_attr(Dummy(), attribute_name,
                                 msg=f"Dummy class has no '{attribute_name}' attribute.")
        print(str(cm.exception))
        self.assertEqual(fixture, str(cm.exception))


# #############################################################################


class Test_logging1(unittest.TestCase):
    def test_logging_levels1(self) -> None:
        dbg.test_logger()
