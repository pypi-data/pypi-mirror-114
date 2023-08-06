from camphr.doc import T_Doc
from typing_extensions import Protocol


class Pipe(Protocol):
    def __call__(self, doc: T_Doc) -> T_Doc:
        ...
