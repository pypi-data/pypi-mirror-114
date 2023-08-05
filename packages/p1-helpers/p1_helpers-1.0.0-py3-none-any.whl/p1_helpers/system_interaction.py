"""
Import as:

import p1_helpers.system_interaction as p1_si

Contain all the code needed to interact with the outside world, e.g., through
system commands, env vars, ...
"""
import logging
import os
import signal
import subprocess
import sys
import time
from typing import Any, Callable, List, Optional, Tuple, Union

import p1_helpers.dbg as p1_dbg
import p1_helpers.printing as hprint

_LOG = logging.getLogger(__name__)


# #############################################################################

def get_env_var(env_var_name: str) -> str:
    if env_var_name not in os.environ:
        msg = "Can't find '%s': re-run dev_scripts/setenv.sh?" % env_var_name
        _LOG.error(msg)
        raise RuntimeError(msg)
    return os.environ[env_var_name]


# #############################################################################

# pylint: disable=too-many-branches,too-many-statements,too-many-arguments,too-many-locals
def _system(
        cmd: str,
        abort_on_error: bool,
        suppress_error: Optional[Any],
        suppress_output: bool,
        blocking: bool,
        wrapper: Optional[Any],
        output_file: Optional[Any],
        num_error_lines: Optional[int],
        tee: bool,
        dry_run: bool,
        log_level: Union[int, str],
) -> Tuple[int, str]:
    """
    Execute a shell command.

    :param cmd: string with command to execute
    :param abort_on_error: whether we should assert in case of error or not
    :param suppress_error: set of error codes to suppress
    :param suppress_output: whether to print the output or not
        - If "on_debug_level" then print the output if the log level is DEBUG
    :param blocking: blocking system call or not
    :param wrapper: another command to prepend the execution of cmd
    :param output_file: redirect stdout and stderr to this file
    :param num_error_lines: number of lines of the output to display when
        raising `RuntimeError`
    :param tee: if True, tee stdout and stderr to output_file
    :param dry_run: just print the final command but not execute it
    :param log_level: print the command to execute at level "log_level".
        - If "echo" then print the command line to screen as print and not
          logging
    :return: return code (int), output of the command (str)
    """
    orig_cmd = cmd[:]
    # Prepare the command line.
    cmd = "(%s)" % cmd
    p1_dbg.dassert_imply(tee, output_file is not None)
    if output_file is not None:
        dir_name = os.path.dirname(output_file)
        if not os.path.exists(dir_name):
            _LOG.debug("Dir '%s' doesn't exist: creating", dir_name)
            p1_dbg.dassert(bool(dir_name), "dir_name='%s'", dir_name)
            os.makedirs(dir_name)
        if tee:
            cmd += " 2>&1 | tee %s" % output_file
        else:
            cmd += " 2>&1 >%s" % output_file
    else:
        cmd += " 2>&1"
    if wrapper:
        cmd = wrapper + " && " + cmd
    #
    # TODO(gp): Add a check for the valid values.
    # TODO(gp): Make it "ECHO".
    if isinstance(log_level, str):
        p1_dbg.dassert_eq(log_level, "echo")
        print("> %s" % orig_cmd)
        _LOG.debug("> %s", cmd)
    else:
        _LOG.log(log_level, "> %s", cmd)
    #
    p1_dbg.dassert_in(suppress_output, ("ON_DEBUG_LEVEL", True, False))
    if suppress_output == "ON_DEBUG_LEVEL":
        # print("eff_lev=%s" % eff_level)
        # print("lev=%s" % logging.DEBUG)
        _LOG.getEffectiveLevel()
        # Suppress the output if the verbosity level is higher than DEBUG,
        # otherwise print.
        suppress_output = _LOG.getEffectiveLevel() > logging.DEBUG
    #
    output = ""
    if dry_run:
        _LOG.warning("Not executing cmd\n%s\nas per user request", cmd)
        rc = 0
        return rc, output
    # Execute the command.
    try:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
        p = subprocess.Popen(
            cmd, shell=True, executable="/bin/bash", stdout=stdout, stderr=stderr
        )
        output = ""
        if blocking:
            # Blocking call: get the output.
            while True:
                line = p.stdout.readline().decode("utf-8")  # type: ignore
                if not line:
                    break
                if not suppress_output:
                    print((line.rstrip("\n")))
                output += line
            p.stdout.close()  # type: ignore
            rc = p.wait()
        else:
            # Not blocking.
            # Wait until process terminates (without using p.wait()).
            max_cnt = 20
            cnt = 0
            while p.poll() is None:
                # Process hasn't exited yet, let's wait some time.
                time.sleep(0.1)
                cnt += 1
                _LOG.debug("cnt=%s, rc=%s", cnt, p.returncode)
                if cnt > max_cnt:
                    break
            if cnt > max_cnt:
                # Timeout: we assume it worked.
                rc = 0
            else:
                rc = p.returncode
        if suppress_error is not None:
            p1_dbg.dassert_isinstance(suppress_error, set)
            if rc in suppress_error:
                rc = 0
    except OSError as e:
        rc = -1
        _LOG.error("error=%s", str(e))
    _LOG.debug("rc=%s", rc)
    if abort_on_error and rc != 0:
        msg = (
                "\n"
                + hprint.frame("cmd='%s' failed with rc='%s'" % (cmd, rc))
                + "\nOutput of the failing command is:\n%s\n%s\n%s"
                % (hprint.line(">"), output, hprint.line("<"))
        )
        _LOG.error("%s", msg)
        # Report the first `num_error_lines` of the output.
        num_error_lines = num_error_lines or 30
        output_error = "\n".join(output.split("\n")[:num_error_lines])
        raise RuntimeError(
            "cmd='%s' failed with rc='%s'\ntruncated output=\n%s"
            % (cmd, rc, output_error)
        )
    # p1_dbg.dassert_type_in(output, (str, ))
    return rc, output


# pylint: disable=too-many-arguments
def system(
        cmd: str,
        abort_on_error: bool = True,
        suppressed_error: Optional[Any] = None,
        suppress_output: bool = True,
        blocking: bool = True,
        wrapper: Optional[Any] = None,
        output_file: Optional[Any] = None,
        num_error_lines: Optional[int] = None,
        tee: bool = False,
        dry_run: bool = False,
        log_level: Union[int, str] = logging.DEBUG,
) -> int:
    """
    Execute a shell command, without capturing its output.

    See _system() for options.
    """
    rc, _ = _system(
        cmd,
        abort_on_error=abort_on_error,
        suppress_error=suppressed_error,
        suppress_output=suppress_output,
        blocking=blocking,
        wrapper=wrapper,
        output_file=output_file,
        num_error_lines=num_error_lines,
        tee=tee,
        dry_run=dry_run,
        log_level=log_level,
    )
    return rc


def system_to_string(
        cmd: str,
        abort_on_error: bool = True,
        wrapper: Optional[Any] = None,
        dry_run: bool = False,
        log_level: Union[int, str] = logging.DEBUG,
) -> Tuple[int, str]:
    """
    Execute a shell command and capture its output.

    See _system() for options.
    """
    rc, output = _system(
        cmd,
        abort_on_error=abort_on_error,
        suppress_error=None,
        suppress_output=True,
        # If we want to see the output the system call must be blocking.
        blocking=True,
        wrapper=wrapper,
        output_file=None,
        num_error_lines=None,
        tee=False,
        dry_run=dry_run,
        log_level=log_level,
    )
    output = output.rstrip("\n")
    return rc, output


def get_first_line(output: str) -> str:
    """
    Return the first (and only) line from a string.

    This is used when calling system_to_string() and expecting a single
    line output.
    """
    output = hprint.remove_empty_lines(output)
    output_as_arr: List[str] = output.split("\n")
    p1_dbg.dassert_eq(len(output_as_arr), 1, "output='%s'", output)
    output = output_as_arr[0]
    output = output.rstrip().lstrip()
    return output


def system_to_one_line(cmd: str, *args: Any, **kwargs: Any) -> Tuple[int, str]:
    """
    Execute a shell command, capturing its output (expected to be a single
    line).

    This is a thin wrapper around system_to_string().
    """
    rc, output = system_to_string(cmd, *args, **kwargs)
    output = get_first_line(output)
    return rc, output


# #############################################################################


def get_process_pids(
        keep_line: Callable[[str], bool]
) -> Tuple[List[int], List[str]]:
    """
    Find all the processes corresponding to `ps ax` filtered line by line with
    `keep_line()`.

    :return: list of pids and filtered output of `ps ax`
    """
    cmd = "ps ax"
    rc, txt = system_to_string(cmd, abort_on_error=False)
    _LOG.debug("txt=\n%s", txt)
    pids: List[int] = []
    txt_out: List[str] = []
    if rc == 0:
        for line in txt.split("\n"):
            _LOG.debug("line=%s", line)
            # PID   TT  STAT      TIME COMMAND
            if "PID" in line and "TT" in line and "STAT" in line:
                txt_out.append(line)
                continue
            keep = keep_line(line)
            _LOG.debug("  keep=%s", keep)
            if not keep:
                continue
            # > ps ax | grep 'ssh -i' | grep localhost
            # 19417   ??  Ss     0:00.39 ssh -i /Users/gp/.ssh/id_rsa -f -nNT \
            #           -L 19999:localhost:19999 gp@54.172.40.4
            fields = line.split()
            try:
                pid = int(fields[0])
            except ValueError as e:
                _LOG.error("Can't parse fields '%s' from line '%s'", fields, line)
                raise e
            _LOG.debug("pid=%s", pid)
            pids.append(pid)
            txt_out.append(line)
    return pids, txt_out


def kill_process(
        get_pids: Callable[[], Tuple[List[int], str]],
        timeout_in_secs: int = 5,
        polltime_in_secs: float = 0.1,
) -> None:
    """
    Kill all the processes returned by the function `get_pids()`.

    :param timeout_in_secs: how many seconds to wait at most before giving up
    :param polltime_in_secs: how often to check for dead processes
    """
    pids, txt = get_pids()
    _LOG.info("Killing %d pids (%s)\n%s", len(pids), pids, "\n".join(txt))
    if not pids:
        return
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError as e:
            _LOG.warning(str(e))
    #
    _LOG.info("Waiting %d processes (%s) to die", len(pids), pids)
    import tqdm

    for _ in tqdm.tqdm(range(int(timeout_in_secs / polltime_in_secs))):
        time.sleep(polltime_in_secs)
        pids, _ = get_pids()
        if not pids:
            break
    pids, txt = get_pids()
    p1_dbg.dassert_eq(len(pids), 0, "Processes are still alive:%s", "\n".join(txt))
    _LOG.info("Processes dead")


def check_exec(tool: str) -> bool:
    """
    Check if an executable can be executed.

    :return: True if the executables "tool" can be executed.
    """
    suppress_output = _LOG.getEffectiveLevel() > logging.DEBUG
    cmd = "which %s" % tool
    abort_on_error = False
    rc = system(
        cmd,
        abort_on_error=abort_on_error,
        suppress_output=suppress_output,
        log_level=logging.DEBUG,
    )
    return rc == 0


# #############################################################################


def query_yes_no(question: str, abort_on_no: bool) -> bool:
    """
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {
        "yes": True,
        "y": True,
        #
        "no": False,
        "n": False,
    }
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in valid:
            ret = valid[choice]
            break
    _LOG.debug("ret=%s", ret)
    if abort_on_no:
        if not ret:
            print("You answer no: exiting")
            sys.exit(-1)
    return ret


def create_executable_script(file_name: str, content: str) -> None:
    # To avoid circular dependencies.
    import p1_helpers.io_ as p1_io

    p1_dbg.dassert_isinstance(content, str)
    p1_io.to_file(file_name, content)
    cmd = "chmod +x " + file_name
    system(cmd)
