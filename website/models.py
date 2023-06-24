from dataclasses import dataclass

@dataclass
class Thought:
    tid: str
    text: str
    createDate: str
    createTimeEpochMs: int
    lastModifiedDate: str
    lastModifiedEpochMs: int
