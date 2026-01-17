from __future__ import annotations
from enum import IntEnum
from dataclasses import dataclass
from typing import ClassVar
import struct


class MessageType(IntEnum):
    CLH = 1
    SVH = 2
    END = 3
    MSG = 4


@dataclass
class Message:
    HEADER_FORMAT: ClassVar[str] = "!B"  # network order, 1 Byte
    HEADER_SIZE: ClassVar[int] = struct.calcsize(HEADER_FORMAT)

    type: MessageType
    body: bytes

    def to_bytes(self) -> bytes:
        header = struct.pack(self.HEADER_FORMAT, self.type)
        return header + self.body

    @classmethod
    def from_bytes(cls, data: bytes) -> Message:
        print(len(data))
        type = struct.unpack(cls.HEADER_FORMAT, data[: cls.HEADER_SIZE])[0]
        body = data[cls.HEADER_SIZE :]

        return cls(MessageType(type), body)
