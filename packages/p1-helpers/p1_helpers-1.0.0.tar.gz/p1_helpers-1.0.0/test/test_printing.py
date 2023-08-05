import logging

import p1_helpers.dbg as p1_dbg
import p1_helpers.printing as p1_print
import unittest

_LOG = logging.getLogger(__name__)


class TestPrinting(unittest.TestCase):
    def test_color_highlight1(self) -> None:
        for c in p1_print.COLOR_MAP:
            _LOG.debug(p1_print.color_highlight(c, c))


class TestToStr(unittest.TestCase):
    def test1(self) -> None:
        x = 1
        # To disable linter complaints.
        _ = x
        act = p1_print.to_str("x")
        exp = "x=1"
        self.assertEqual(act, exp)

    def test2(self) -> None:
        x = "hello world"
        # To disable linter complaints.
        _ = x
        act = p1_print.to_str("x")
        exp = "x='hello world'"
        self.assertEqual(act, exp)

    def test3(self) -> None:
        x = 2
        # To disable linter complaints.
        _ = x
        act = p1_print.to_str("x*2")
        exp = "x*2=4"
        self.assertEqual(act, exp)

    def test4(self) -> None:
        """
        Test printing multiple values separated by space.
        """
        x = 1
        y = "hello"
        # To disable linter complaints.
        _ = x, y
        act = p1_print.to_str("x y")
        exp = "x=1, y='hello'"
        self.assertEqual(act, exp)

    def test5(self) -> None:
        """
        Test printing multiple strings separated by space.
        """
        x = "1"
        y = "hello"
        # To disable linter complaints.
        _ = x, y
        act = p1_print.to_str("x y")
        exp = "x='1', y='hello'"
        self.assertEqual(act, exp)

    def test6(self) -> None:
        """
        Test printing a list.
        """
        x = [1, "hello", "world"]
        # To disable linter complaints.
        _ = x
        act = p1_print.to_str("x")
        exp = "x=[1, 'hello', 'world']"
        self.assertEqual(act, exp)


class TestLog(unittest.TestCase):
    def test1(self) -> None:
        p1_dbg.test_logger()

    def test2(self) -> None:
        x = 1
        # To disable linter complaints.
        _ = x
        for verb in [logging.DEBUG, logging.INFO]:
            p1_print.log(_LOG, verb, "x")

    def test3(self) -> None:
        x = 1
        y = "hello"
        # To disable linter complaints.
        _ = x, y
        for verb in [logging.DEBUG, logging.INFO]:
            p1_print.log(_LOG, verb, "x y")

    def test4(self) -> None:
        """
        The command:

        > pytest -k Test_log::test4  -o log_cli=true --dbg_verbosity DEBUG

        should print something like:

        DEBUG    test_printing:printing.py:315 x=1, y='hello', z=['cruel', 'world']
        INFO     test_printing:printing.py:315 x=1, y='hello', z=['cruel', 'world']
        """
        x = 1
        y = "hello"
        z = ["cruel", "world"]
        # To disable linter complaints.
        _ = x, y, z
        for verb in [logging.DEBUG, logging.INFO]:
            p1_print.log(_LOG, verb, "x y z")
