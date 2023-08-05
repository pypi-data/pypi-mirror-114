"""
Import as:

import p1_helpers.printing as p1_print
"""

import logging
import re
import sys
import tempfile
from typing import Any, Dict, Iterable, List, Optional, Tuple, cast

import p1_helpers.dbg as p1_dbg

_LOG = logging.getLogger(__name__)


# #############################################################################
# Debug output
# #############################################################################

COLOR_MAP = {
    "blue": "\033[94m",
    "green": "\033[92m",
    "none": "\033[0m",
    "purple": "\033[95m",
    "red": "\033[91m",
    "yellow": "\033[93m",
}


def color_highlight(text: str, color: str) -> str:
    return COLOR_MAP[color] + text + COLOR_MAP["none"]


def clear_screen() -> None:
    print((chr(27) + "[2J"))


def line(char: Optional[str] = None, num_chars: Optional[int] = None) -> str:
    """
    Return a line with the desired character.
    """
    char = "#" if char is None else char
    num_chars = 80 if num_chars is None else num_chars
    return char * num_chars


def frame(
    message: str,
    char1: Optional[str] = None,
    num_chars: Optional[int] = None,
    char2: Optional[str] = None,
    thickness: int = 1,
) -> str:
    """
    Print a frame around a message.
    """
    # Fill in the default values.
    if char1 is None:
        # User didn't specify any char.
        char1 = char2 = "#"
    elif char1 is not None and char2 is None:
        # User specified only one char.
        char2 = char1
    elif char1 is None and char2 is not None:
        # User specified the second char, but not the first.
        p1_dbg.dfatal("Invalid char1='%s' char2='%s'" % (char1, char2))
    else:
        # User specified both chars. Nothing to do.
        pass
    num_chars = 80 if num_chars is None else num_chars
    # Sanity check.
    p1_dbg.dassert_lte(1, thickness)
    p1_dbg.dassert_eq(len(char1), 1)
    p1_dbg.dassert_eq(len(char2), 1)
    p1_dbg.dassert_lte(1, num_chars)
    # Build the return value.
    ret = (
        (line(char1, num_chars) + "\n") * thickness
        + message
        + "\n"
        + (line(char2, num_chars) + "\n") * thickness
    ).rstrip("\n")
    return ret


def indent(str_: str, num_spaces: int = 2) -> str:
    """
    Add `num_spaces` spaces before each line of the string `str_`.
    """
    return prepend(str_, " " * num_spaces)


def dedent(txt: str) -> str:
    """
    Remove all extra leadning / trailing spaces and empty lines.
    """
    txt_out = []
    for curr_line in txt.split("\n"):
        curr_line = curr_line.rstrip(" ").lstrip(" ")
        if curr_line:
            txt_out.append(curr_line)
    return "\n".join(txt_out)


def prepend(str_: str, prefix: str) -> str:
    """
    Add `prefix` before each line of the string `str_`.
    """
    # lines = ["<" + prefix + curr_line + ">" for curr_line in str_.split("\n")]
    lines = [prefix + curr_line for curr_line in str_.split("\n")]
    return "\n".join(lines)


def remove_empty_lines_from_string_list(arr: List[str]) -> List[str]:
    """
    Remove empty lines from a list of strings.
    """
    arr = [line for line in arr if line.rstrip().lstrip()]
    return arr


# TODO(gp): It would be nice to have a decorator to go from / to array of
#  strings.
def remove_empty_lines(txt: str) -> str:
    """
    Remove empty lines from a multi-line string.
    """
    arr = txt.split("\n")
    arr = remove_empty_lines_from_string_list(arr)
    txt = "\n".join(arr)
    return txt


def vars_to_debug_string(vars_as_str: List[str], locals_: Dict[str, Any]) -> str:
    """
    Create a string with var name -> var value.

    E.g., ["var1", "var2"] is converted into: ``` var1=... var2=... ```
    """
    txt = []
    for var in vars_as_str:
        txt.append(var + "=")
        txt.append(indent(str(locals_[var])))
    return "\n".join(txt)


# #############################################################################
# Pretty print data structures.
# #############################################################################


def thousand_separator(v: float) -> str:
    v = "{0:,}".format(v)
    return v


def perc(
    a: float,
    b: float,
    only_perc: bool = False,
    invert: bool = False,
    num_digits: int = 2,
    use_thousands_separator: bool = False,
) -> str:
    """
    Calculate percentage a / b as a string.

    Asserts 0 <= a <= b. If true, returns a/b to `num_digits` decimal places.

    :param a: numerator
    :param b: denominator
    :param only_perc: return only the percentage, without the original numbers
    :param invert: assume the fraction is (b - a) / b
        This is useful when we want to compute the complement of a count.
    :param use_thousands_separator: report the numbers using thousands separator
    :return: string with a/b
    """
    p1_dbg.dassert_lte(0, a)
    p1_dbg.dassert_lte(a, b)
    if use_thousands_separator:
        a_str = str("{0:,}".format(a))
        b_str = str("{0:,}".format(b))
    else:
        a_str = str(a)
        b_str = str(b)
    if invert:
        a = b - a
    p1_dbg.dassert_lte(0, num_digits)
    if only_perc:
        fmt = "%." + str(num_digits) + "f%%"
        ret = fmt % (float(a) / b * 100.0)
    else:
        fmt = "%s / %s = %." + str(num_digits) + "f%%"
        ret = fmt % (a_str, b_str, float(a) / b * 100.0)
    return ret


def round_digits(
    v: float, num_digits: int = 2, use_thousands_separator: bool = False
) -> str:
    """
    Round digit returning a string representing the formatted number.

    :param v: value to convert
    :param num_digits: number of digits to represent v on
            None is (Default value = 2)
    :param use_thousands_separator: use "," to separate thousands (Default value = False)
    :returns: str with formatted value
    """
    if (num_digits is not None) and isinstance(v, float):
        fmt = "%0." + str(num_digits) + "f"
        res = float(fmt % v)
    else:
        res = v
    if use_thousands_separator:
        res = "{0:,}".format(res)  # type: ignore
    res_as_str = str(res)
    return res_as_str


# #############################################################################


def to_str(expression: str, frame_lev: int = 1) -> str:
    """
    Return a string representing the value of an expression like `exp=value`.

    # This is similar to Python 3.8 f-string syntax `f"{foo=} {bar=}"`.
    # We don't want to force to use Python 3.8 just for this feature.

    # If expression is a space-separated compound expression, convert it into
    # `exp1=val1, exp2=val2, ...`.

    >>> x = 1
    >>> to_str("x+1")
    x+1=2
    """
    p1_dbg.dassert_isinstance(expression, str)
    if " " in expression:
        # If expression is a list of space-separated expression, convert each in a
        # string.
        exprs = [v.lstrip().rstrip() for v in expression.split(" ")]
        _to_str = lambda x: to_str(x, frame_lev=frame_lev + 2)
        return ", ".join(list(map(_to_str, exprs)))

    frame = sys._getframe(frame_lev)
    ret = (
        expression + "=" + repr(eval(expression, frame.f_globals, frame.f_locals))
    )
    return ret


def log(logger, verbosity, *vals: Any) -> Tuple[str, List[str]]:
    """
    _LOG.debug(to_log("ticker", "exchange"))

    is equivalent to statements like:

    _LOG.debug("%s, %s", to_str("ticker"), to_str("exchange"))
    _LOG.debug("ticker=%s, exchange=%s", ticker, exchange)
    """
    logger_verbosity = p1_dbg.get_logger_verbosity()
    # print("verbosity=%s logger_verbosity=%s" % (verbosity, logger_verbosity))
    # We want to avoid the overhead of converting strings, so we evaluate the
    # expressions only if we are going to print.
    if verbosity >= logger_verbosity:
        # We need to increment frame_lev since we are 2 levels deeper in the stack.
        _to_str = lambda x: to_str(x, frame_lev=3)
        num_vals = len(vals)
        if num_vals == 1:
            fstring = "%s"
            vals = _to_str(vals[0])
        else:
            fstring = ", ".join(["%s"] * num_vals)
            vals = list(map(_to_str, vals))
        logger.log(verbosity, fstring, vals)


# #############################################################################


def type_to_string(type_as_str: str) -> str:
    """
    Return a short string representing the type of an object, e.g.,
    "core.dataflow.Node" (instead of "class <'core.dataflow.Node'>")
    """
    if isinstance(type_as_str, type):
        type_as_str = str(type_as_str)
    p1_dbg.dassert_isinstance(type_as_str, str)
    # Remove the extra string from:
    #   <class 'core.dataflow.Zscore'>
    prefix = "<class '"
    p1_dbg.dassert(type_as_str.startswith(prefix), type_as_str)
    suffix = "'>"
    p1_dbg.dassert(type_as_str.endswith(suffix), type_as_str)
    type_as_str = type_as_str[len(prefix) : -len(suffix)]
    return type_as_str


def format_list(
    list_: List[Any],
    sep: str = " ",
    max_n: Optional[int] = None,
    tag: Optional[str] = None,
) -> str:
    sep = " "
    # sep = ", "
    if max_n is None:
        max_n = 10
    max_n = cast(int, max_n)
    p1_dbg.dassert_lte(1, max_n)
    n = len(list_)
    txt = ""
    if tag is not None:
        txt += "%s: " % tag
    txt += "(%s) " % n
    if n < max_n:
        txt += sep.join(map(str, list_))
    else:
        num_elems = int(max_n / 2)
        p1_dbg.dassert_lte(1, num_elems)
        txt += sep.join(map(str, list_[:num_elems]))
        txt += " ... "
        # pylint: disable=invalid-unary-operand-type
        txt += sep.join(map(str, list_[-num_elems:]))
    return txt


# TODO(gp): Use format_list().
def list_to_str(
    list_: List,
    tag: str = "",
    sort: bool = False,
    axis: int = 0,
    to_string: bool = False,
) -> str:
    """
    Print list / index horizontally or vertically.
    """
    # TODO(gp): Fix this.
    _ = to_string
    txt = ""
    if axis == 0:
        if list_ is None:
            txt += "%s: (%s) %s" % (tag, 0, "None") + "\n"
        else:
            # p1_dbg.dassert_in(type(l), (list, pd.Index, pd.Int64Index))
            vals = list(map(str, list_))
            if sort:
                vals = sorted(vals)
            txt += "%s: (%s) %s" % (tag, len(list_), " ".join(vals)) + "\n"
    elif axis == 1:
        txt += "%s (%s):" % (tag, len(list_)) + "\n"
        vals = list(map(str, list_))
        if sort:
            vals = sorted(vals)
        txt += "\n".join(vals) + "\n"
    else:
        raise ValueError("Invalid axis='%s'" % axis)
    return txt


# TODO(gp): -> set_diff_to_str
def print_set_diff(
    obj1: Iterable,
    obj2: Iterable,
    obj1_name: str = "obj1",
    obj2_name: str = "obj2",
    add_space: bool = False,
) -> None:
    def _to_string(obj: Iterable) -> str:
        return " ".join(map(str, obj))

    print("# %s vs %s" % (obj1_name, obj2_name))
    obj1 = set(obj1)
    p1_dbg.dassert_lte(1, len(obj1))
    print("* %s: (%s) %s" % (obj1_name, len(obj1), _to_string(obj1)))
    if add_space:
        print()
    #
    obj2 = set(obj2)
    p1_dbg.dassert_lte(1, len(obj2))
    print("* %s: (%s) %s" % (obj2_name, len(obj2), _to_string(obj2)))
    if add_space:
        print()
    #
    intersection = obj1.intersection(obj2)
    print("* intersect=(%s) %s" % (len(intersection), _to_string(intersection)))
    if add_space:
        print()
    #
    diff = obj1 - obj2
    print("* %s-%s=(%s) %s" % (obj1_name, obj2_name, len(diff), _to_string(diff)))
    if add_space:
        print()
    #
    diff = obj2 - obj1
    print("* %s-%s=(%s) %s" % (obj2_name, obj1_name, len(diff), _to_string(diff)))
    if add_space:
        print()


def diff_strings(
    txt1: str,
    txt2: str,
    txt1_descr: Optional[str] = None,
    txt2_descr: Optional[str] = None,
    width: int = 130,
) -> str:
    # To avoid circular dependencies.
    import p1_helpers.io_ as p1_io

    # Write file.
    def _to_file(txt: str, txt_descr: Optional[str]) -> str:
        file_name = tempfile.NamedTemporaryFile().name
        if txt_descr is not None:
            txt = "# " + txt_descr + "\n" + txt
        p1_io.to_file(file_name, txt)
        return file_name

    #
    file_name1 = _to_file(txt1, txt1_descr)
    file_name2 = _to_file(txt2, txt2_descr)
    #
    cmd = f"sdiff --width={width} {file_name1} {file_name2}"
    # To avoid circular dependencies.
    import p1_helpers.system_interaction as p1_si

    _, txt = p1_si.system_to_string(
        cmd,
        # We don't care if they are different.
        abort_on_error=False,
    )
    # For some reason, mypy doesn't understand that system_to_string returns a
    # string.
    txt = cast(str, txt)
    return txt


def obj_to_str(
    obj: Any,
    attr_mode: str = "__dict__",
    print_type: bool = False,
    callable_mode: str = "skip",
    private_mode: str = "skip_dunder",
) -> str:
    """
    Print attributes of an object.

    :param using_dict: use `__dict__` instead of `dir`
    :param print_type: print the type of the attribute
    :param callable_mode: how to handle attributes that are callable (i.e.,
        methods)
        - skip: skip the methods
        - only: print only the methods
        - all: print variables and callable
    """

    def _to_skip_callable(attr: Any, callable_mode: str) -> bool:
        p1_dbg.dassert_in(callable_mode, ("skip", "only", "all"))
        is_callable = callable(attr)
        skip = False
        if callable_mode == "skip" and is_callable:
            skip = True
        if callable_mode == "only" and not is_callable:
            skip = True
        return skip

    def _to_skip_private(name: str, private_mode: str) -> bool:
        p1_dbg.dassert_in(
            private_mode,
            ("skip_dunder", "only_dunder", "skip_private", "only_private", "all"),
        )
        is_dunder = name.startswith("__") and name.endswith("__")
        is_private = not is_dunder and name.startswith("_")
        skip = False
        if private_mode == "skip_dunder" and is_dunder:
            skip = True
        if private_mode == "only_dunder" and not is_dunder:
            skip = True
        if private_mode == "skip_private" and is_private:
            skip = True
        if private_mode == "only_private" and not is_private:
            skip = True
        return skip

    def _to_str(attr: Any, print_type: bool) -> str:
        if print_type:
            _out = "%s= (%s) %s" % (v, type(attr), str(attr))
        else:
            _out = "%s= %s" % (v, str(attr))
        return _out

    ret = []
    if attr_mode == "__dict__":
        for v in sorted(obj.__dict__):
            attr = obj.__dict__[v]
            # Handle dunder / private methods.
            skip = _to_skip_private(v, private_mode)
            if skip:
                continue
            # Handle callable methods.
            skip = _to_skip_callable(attr, callable_mode)
            if skip:
                continue
            #
            out = _to_str(attr, print_type)
            ret.append(out)
    elif attr_mode == "dir":
        for v in dir(obj):
            attr = getattr(obj, v)
            # Handle dunder / private methods.
            skip = _to_skip_private(v, private_mode)
            if skip:
                continue
            # Handle callable methods.
            skip = _to_skip_callable(attr, callable_mode)
            if skip:
                continue
            #
            out = _to_str(attr, print_type)
            ret.append(out)
    else:
        p1_dbg.dassert("Invalid attr_mode='%s'" % attr_mode)
    return "\n".join(ret)


def type_obj_to_str(obj: Any) -> str:
    ret = "(%s) %s" % (type(obj), obj)
    return ret


def dataframe_to_str(
    df: Any,
    max_columns: int = 10000,
    max_colwidth: int = 2000,
    max_rows: int = 500,
    display_width: int = 10000,
) -> str:
    import pandas as pd

    with pd.option_context(
        "display.max_colwidth",
        max_colwidth,
        #'display.height', 1000,
        "display.max_rows",
        max_rows,
        "display.max_columns",
        max_columns,
        "display.width",
        display_width,
    ):
        res = str(df)
    return res


def remove_non_printable_chars(txt: str) -> str:
    # From https://stackoverflow.com/questions/14693701
    # 7-bit and 8-bit C1 ANSI sequences
    ansi_escape = re.compile(
        r"""
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    """,
        re.VERBOSE,
    )
    txt = ansi_escape.sub("", txt)
    return txt


# #############################################################################
# Notebook output
# #############################################################################

# TODO: Move to explore.py


def config_notebook(sns_set: bool = True) -> None:
    import matplotlib.pyplot as plt
    import seaborn as sns

    if sns_set:
        sns.set()
    import pandas as pd

    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.width", 1000)
    # plt.rcParams
    plt.rcParams["figure.figsize"] = (20, 5)
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["font.size"] = 14
    plt.rcParams["image.cmap"] = "rainbow"
