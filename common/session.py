from dataclasses import dataclass
from typing import Optional, ClassVar
import hashlib
from random import randbytes
import secrets


@dataclass
class Session:
    KEY_SIZE: ClassVar[int] = 4
    DH_P: ClassVar[int] = 4294967311  # 32-bitowa liczba pierwsza
    DH_G: ClassVar[int] = 5  # mała podstawa

    private_key: Optional[int] = None
    public_key: Optional[int] = None
    peer_public_key: Optional[int] = None

    shared_key: Optional[bytes] = None
    mac_key: Optional[bytes] = None

    @property
    def tls_established(self) -> bool:
        return self.shared_key is not None

    def generate_keys(self):
        self.private_key = secrets.randbelow(self.DH_P - 2) + 2
        self.public_key = pow(self.DH_G, self.private_key, self.DH_P)

    def public_key_bytes(self) -> bytes:
        return self.public_key.to_bytes(self.KEY_SIZE, "big")

    def set_peer_key(self, peer_bytes: bytes):
        self.peer_public_key = int.from_bytes(peer_bytes, "big")

    def calculate_shared_key(self):
        self.shared_key = pow(self.peer_public_key, self.private_key, self.DH_P)
        self.shared_key = self.shared_key.to_bytes(self.KEY_SIZE, "big")
        print("Shared key calculated.", self.shared_key)
        print("Shared key:", self.shared_key.hex())

    def encrypt_message(self, plaintext: bytes) -> bytes:
        if self.shared_key is None:
            raise ValueError("Shared key not established")

        key = self.shared_key
        key_len = len(key)
        ciphertext = bytes([b ^ key[i % key_len] for i, b in enumerate(plaintext)])
        return ciphertext

    def decrypt_message(self, ciphertext: bytes) -> bytes:
        return self.encrypt_message(ciphertext)

    def encrypt_and_mac(plaintext):
        pass

    def verify_and_decrypt(ciphertext):
        pass
