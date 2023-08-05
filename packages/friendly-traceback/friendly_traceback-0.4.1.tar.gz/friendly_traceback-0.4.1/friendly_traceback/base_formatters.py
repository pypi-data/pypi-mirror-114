"""
base_formatters.py
===================

Default formatters showing all or only part of the available information.

A formatter is a function that takes two arguments:

1. a dict (named ``info`` everywhere in friendly files) containing
   all the information that can be shown to the user, as well as some
   entries that are meant to be used only internally as the full
   friendly information is obtained.

2. A second argument which is meant to convey what information should be shown.
   This second argument used to be a single integer ("verbosity level").
   It is currently recently being replaced by a single string. However,
   this might change as we experiment with various options prior to
   version 1.0

A formatter returns a single string. By default, this string will be
written to stderr; however this can be changed by the calling program.

This module currently contains 2 formatters:

* ``repl()``: This is used to print the information in a traditional console.
  The indentation of the traceback itself is chosen
  so as to reproduce that of a normal Python traceback.

* ``docs()``: this produces output with leading spaces so that it can be
  embedded as a code-block in a file (such as .rst). It can also be used
  to print the information in a traditional console.
"""
import sys
from typing import Dict, List, Set

from .ft_gettext import current_lang
from . import debug_helper


if sys.version_info >= (3, 8):
    from typing import Literal, Protocol, TypedDict

    InclusionChoice = Literal[
        "message",
        "hint",
        "what",
        "why",
        "where",
        "friendly_tb",
        "python_tb",
        "debug_tb",
        "explain",
        "no_tb",
    ]

    class Info(TypedDict, total=False):
        message: str
        original_python_traceback: str
        simulated_python_traceback: str
        shortened_traceback: str
        suggest: str
        generic: str
        parsing_error: str
        parsing_error_source: str
        cause: str
        last_call_header: str
        last_call_source: str
        last_call_variables: str
        exception_raised_header: str
        exception_raised_source: str
        exception_raised_variables: str

    class Formatter(Protocol):
        def __call__(self, info: Info, include: InclusionChoice = ...) -> str:
            ...


else:
    from typing import Callable

    InclusionChoice = str
    Info = Dict[str, str]
    Formatter = Callable[[Info, InclusionChoice], str]


# The following is the order in which the various items, if they exist
# and have been selected to be printed, would be printed.
# If you are writing a custom formatter, this should be taken as the
# authoritative list of items to consider.

items_in_order = [
    "header",  # Currently unused by this project; used by HackInScience
    "message",  # The last line of a Python traceback
    "original_python_traceback",  # <-- Friendly._debug_tb()
    "simulated_python_traceback",  # <-- python_tb()
    "shortened_traceback",  # <-- friendly_tb()
    "suggest",  # <-- hint()
    "generic",  # <-- what()
    "parsing_error",
    "parsing_error_source",
    "cause",  # <-- why()
    "last_call_header",
    "last_call_source",
    "last_call_variables",
    "exception_raised_header",
    "exception_raised_source",
    "exception_raised_variables",
]


repl_indentation = {
    "header": "single",  # no longer shown; keep for reference
    "message": "single",
    "simulated_python_traceback": "none",
    "original_python_traceback": "none",
    "shortened_traceback": "none",
    "suggest": "double",
    "generic": "single",
    "parsing_error": "single",
    "parsing_error_source": "none",
    "cause": "single",
    "last_call_header": "single",
    "last_call_source": "none",
    "last_call_variables": "double",
    "exception_raised_header": "single",
    "exception_raised_source": "none",
    "exception_raised_variables": "double",
}


def repl(info: Info, include: InclusionChoice = "friendly_tb") -> str:
    """Default formatter, primarily for console usage.

    The only change made to the content of "info" is
    some added indentation.
    """
    if include == "message":
        return info["message"]
    items_to_show = select_items(include)
    spacing = {"single": " " * 4, "double": " " * 8, "none": ""}
    result = [""]
    for item in items_to_show:
        if item in info:
            indentation = spacing[repl_indentation[item]]
            for line in info[item].split("\n"):
                result.append(indentation + line)

    if result == [""] or not result:
        return no_result(info, include)

    return "\n".join(result)


def docs(
    info: Info, include: InclusionChoice = "friendly_tb"
) -> str:  # pragma: no cover
    """Formatter that produces an output that is suitable for
    insertion in a RestructuredText (.rst) code block,
    with pre-formatted indentation.

    The only change made to the content of "info" is
    some added indentation.
    """
    # We first define the indentation to appear before each item
    pre_items = dict(**repl_indentation)

    pre_items.update(
        **{
            "simulated_python_traceback": "single",
            "original_python_traceback": "single",
            "shortened_traceback": "single",
        }
    )

    items_to_show = select_items(include)
    spacing = {"single": " " * 4, "double": " " * 8, "none": ""}
    result = [""]
    for item in items_to_show:
        if item in info and info[item].strip():
            indentation = spacing[pre_items[item]]
            for line in info[item].split("\n"):
                result.append(indentation + line)

    if result == [""]:
        return no_result(info, include)

    return "\n".join(result)


def no_result(info: Info, include: InclusionChoice) -> str:
    """Should normally only be called if no result is available
    from either hint() or why().
    """
    _ = current_lang.translate
    if include == "why":
        return _("I have no suggestion to offer.")

    if include == "hint":
        if "cause" in info:
            return _("I have no suggestion to offer; try `why()`.")

        return _("I have no suggestion to offer.")

    debug_helper.log(
        f"Internal error: include = {include} in base_formatters.no_result()"
    )  # pragma: no cover


items_groups: Dict[InclusionChoice, Set[str]] = {
    "message": {"message"},  # Also included as last line of traceback
    "hint": {"suggest"},
    "what": {"generic"},
    "why": {"cause"},
    "where": {
        "parsing_error",
        "parsing_error_source",
        "last_call_header",
        "last_call_source",
        "last_call_variables",
        "exception_raised_header",
        "exception_raised_source",
        "exception_raised_variables",
    },
    "friendly_tb": {"shortened_traceback", "suggest"},
    "python_tb": {"simulated_python_traceback"},
    "debug_tb": {"original_python_traceback"},
}
items_groups["explain"] = (
    items_groups["friendly_tb"]
    .union(items_groups["what"])
    .union(items_groups["why"])
    .union(items_groups["where"])
)

items_groups["no_tb"] = set(items_groups["explain"])  # used in check_syntax()
for item_ in items_groups["friendly_tb"]:
    items_groups["no_tb"].discard(item_)


def select_items(group_name: InclusionChoice) -> List[str]:
    items = items_groups[group_name]
    return [item for item in items_in_order if item in items]
