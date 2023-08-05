from typing import NamedTuple, List


class TraceTouch(NamedTuple):
    name: str
    time: int


class Trace(NamedTuple):
    id: str
    touches: List[TraceTouch] = []
