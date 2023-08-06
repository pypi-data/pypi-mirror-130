import enum
import os.path
import re
import traceback

__version__ = "0.1.0"

_EXCEPTION_LOCATION_LINE_REGEX = re.compile(
    r'\s*File "(?P<source_path>[^"]+)", line (?P<source_line_number>\d+), in (?P<function>.+)\n(?P<source_code>.+)'
)


class ErrorReferenceSource(enum.Enum):
    ALWAYS = 1
    DEVELOPER = 2
    NEVER = 3


def error_text(error: Exception, reference_source: ErrorReferenceSource = ErrorReferenceSource.DEVELOPER) -> str:
    base_error_message = str(error)
    is_developer_error = isinstance(error, (AssertionError, AttributeError, NotImplementedError, TypeError))
    result = type(error).__name__ if not base_error_message or is_developer_error else ""
    if base_error_message != "":
        if is_developer_error:
            result += ": "
        result += base_error_message
    if reference_source == ErrorReferenceSource.ALWAYS or (
        reference_source == ErrorReferenceSource.DEVELOPER and is_developer_error
    ):
        stack_lines = error_trace(error)
        stack_match = None
        for stack_line in stack_lines:
            stack_match = _EXCEPTION_LOCATION_LINE_REGEX.match(stack_line)
            if stack_match is not None:
                break
        if stack_match is not None:
            source_path = stack_match.group("source_path")
            relative_source_path = os.path.relpath(source_path, os.getcwd())
            source_line_number = stack_match.group("source_line_number")
            function = stack_match.group("function")
            if not result.endswith(" "):
                result += " "
            result += f"(from {function}@{relative_source_path}:{source_line_number})"
    return result


def error_trace(error: Exception) -> str:
    return (
        "".join(traceback.format_exception(type(error), error, error.__traceback__))
        if isinstance(error, Exception)
        else ""
    )
