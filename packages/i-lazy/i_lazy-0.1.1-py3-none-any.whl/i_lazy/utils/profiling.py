from types import FrameType
from typing import Any, Literal


def trace_calls(frame: FrameType, event: str, arg: Any) -> Any:
    # event: "call", "line", "return", "exception", "c_call", "c_return", "c_exception"
    if event != "call":
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == "write":
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    caller = frame.f_back
    if caller is not None:
        print(
            f"{caller.f_code.co_name} called {func_name} at {func_filename}:{func_line_no}")
    else:
        print(f"{func_name} at {func_filename}:{func_line_no} called")
    # caller_line_no = caller.f_lineno
    # caller_filename = caller.f_code.co_filename
    return
