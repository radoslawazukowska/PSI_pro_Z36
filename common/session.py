from dataclasses import dataclass
from typing import Optional, ClassVar
import hashlib
from random import randbytes


@dataclass
class Session:
    KEY_SIZE: ClassVar[int] = 32
    DH_P: ClassVar[int] = 17
    DH_P: ClassVar[int] = 19

    private_key: Optional[bytes] = None
    public_key: Optional[bytes] = None
    peer_public_key: Optional[bytes] = None

    shared_key: Optional[bytes] = None
    mac_key: Optional[bytes] = None

    @property
    def tls_established(self) -> bool:
        return self.shared_key is not None

    def generate_public_key(self):
        self.public_key = randbytes(self.key_size)

    def set_peer_key(self, peer_key: bytes):
        self.peer_public_key = peer_key

    def calculate_shared_key(self):
        pass

    def encrypt_and_mac(plaintext):
        pass

    def verify_and_decrypt(ciphertext):
        pass
