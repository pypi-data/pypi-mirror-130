from typing import IO, Tuple

class TextFile:
    def __init__(
        self,
        filename: str | None = ...,
        file: IO[str] | None = ...,
        *,
        strip_comments: bool = ...,
        lstrip_ws: bool = ...,
        rstrip_ws: bool = ...,
        skip_blanks: bool = ...,
        join_lines: bool = ...,
        collapse_join: bool = ...,
    ) -> None: ...
    def open(self, filename: str) -> None: ...
    def close(self) -> None: ...
    def warn(self, msg: str, line: list[int] | Tuple[int, int] | int | None = ...) -> None: ...
    def readline(self) -> str | None: ...
    def readlines(self) -> list[str]: ...
    def unreadline(self, line: str) -> str: ...
