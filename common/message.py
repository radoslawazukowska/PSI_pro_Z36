from enum import IntEnum
from dataclasses import dataclass
import struct


class MessageType(IntEnum):
    CLH = 1
    SVH = 2
    END = 3
    MSG = 4


@dataclass
class Message:
    msg_type: MessageType
    body: bytes

    HEADER_FORMAT = "!BI"  # type (1B), length (4B)

    def encode(self) -> bytes:
        header = struct.pack(self.HEADER_FORMAT, self.msg_type, len(self.body))
        return header + self.body

    @classmethod
    def decode(cls, data: bytes) -> "Message":
        header_size = struct.calcsize(cls.HEADER_FORMAT)

        msg_type, length = struct.unpack(cls.HEADER_FORMAT, data[:header_size])

        body = data[header_size : header_size + length]

        return cls(MessageType(msg_type), body)
