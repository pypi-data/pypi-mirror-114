import logging
import re
import tempfile
import unittest

import p1_helpers.dbg as dbg
import p1_helpers.system_interaction as p1_si

_LOG = logging.getLogger(__name__)

# #############################################################################


class TestSystemInteraction(unittest.TestCase):
    def test1(self) -> None:
        p1_si.system("ls")

    def test2(self) -> None:
        p1_si.system("ls /dev/null", suppress_output=False)

    def test3(self) -> None:
        """
        Output to a file.
        """
        with tempfile.NamedTemporaryFile() as fp:
            temp_file_name = fp.name
            _LOG.debug("temp_file_name=%s", temp_file_name)
            p1_si.system("ls", output_file=temp_file_name)
            dbg.dassert_exists(temp_file_name)

    def test4(self) -> None:
        """
        Tee to a file.
        """
        with tempfile.NamedTemporaryFile() as fp:
            temp_file_name = fp.name
            _LOG.debug("temp_file_name=%s", temp_file_name)
            p1_si.system("ls", output_file=temp_file_name, tee=True)
            dbg.dassert_exists(temp_file_name)

    def test5(self) -> None:
        """
        Test dry_run.
        """
        temp_file_name = tempfile._get_default_tempdir()  # type: ignore
        candidate_name = tempfile._get_candidate_names()  # type: ignore
        temp_file_name += "/" + next(candidate_name)
        _LOG.debug("temp_file_name=%s", temp_file_name)
        p1_si.system("ls", output_file=temp_file_name, dry_run=True)
        dbg.dassert_not_exists(temp_file_name)

    def test6(self) -> None:
        """
        Test abort_on_error=True.
        """
        p1_si.system("ls this_file_doesnt_exist", abort_on_error=False)

    def test7(self) -> None:
        """
        Test abort_on_error=False. Default behaviour.
        """
        fixture = """cmd='(ls this_file_doesnt_exist) 2>&1' failed with rc=''
truncated output=
ls: cannot access 'this_file_doesnt_exist': No such file or directory
"""
        with self.assertRaises(RuntimeError) as cm:
            p1_si.system("ls this_file_doesnt_exist")
        act = str(cm.exception)
        # Different systems return different rc.
        # cmd='(ls this_file_doesnt_exist) 2>&1' failed with rc='2'
        act = re.sub(r"rc='(\d+)'", "rc=''", act)
        self.assertEqual(fixture, act)

