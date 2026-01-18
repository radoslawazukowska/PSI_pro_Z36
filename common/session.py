from dataclasses import dataclass
from typing import Optional, ClassVar
import hashlib
from random import randbytes
import secrets


@dataclass
class Session:
    KEY_SIZE: ClassVar[int] = 4
    # Default values - can be overridden during key exchange
    DEFAULT_DH_P: ClassVar[int] = 4294967311
    DEFAULT_DH_G: ClassVar[int] = 5

    dh_p: Optional[int] = None
    dh_g: Optional[int] = None
    private_key: Optional[int] = None
    public_key: Optional[int] = None
    peer_public_key: Optional[int] = None

    shared_key: Optional[bytes] = None
    mac_key: Optional[bytes] = None

    @property
    def tls_established(self) -> bool:
        return self.shared_key is not None

    def set_dh_params(self, p: int, g: int):
        """Set Diffie-Hellman parameters (P and G)"""
        self.dh_p = p
        self.dh_g = g

    def generate_keys(self):
        self.private_key = secrets.randbelow(self.dh_p - 2) + 2
        self.public_key = pow(self.dh_g, self.private_key, self.dh_p)

    def public_key_bytes(self) -> bytes:
        return self.public_key.to_bytes(self.KEY_SIZE, "big")

    def dh_params_bytes(self) -> bytes:
        if self.dh_p is None:
            self.dh_p = self.DEFAULT_DH_P
        if self.dh_g is None:
            self.dh_g = self.DEFAULT_DH_G
        return self.dh_p.to_bytes(self.KEY_SIZE, "big") + self.dh_g.to_bytes(self.KEY_SIZE, "big")

    def set_dh_params_from_bytes(self, data: bytes):
        if len(data) < 2 * self.KEY_SIZE:
            raise ValueError("Data too short for DH parameters")
        self.dh_p = int.from_bytes(data[:self.KEY_SIZE], "big")
        self.dh_g = int.from_bytes(data[self.KEY_SIZE:2*self.KEY_SIZE], "big")

    def set_peer_key(self, peer_bytes: bytes):
        self.peer_public_key = int.from_bytes(peer_bytes, "big")

    def calculate_shared_key(self):
        key = pow(self.peer_public_key, self.private_key, self.dh_p)
        self.shared_key = key.to_bytes(self.KEY_SIZE, "big")
        self.mac_key = hashlib.sha256(self.shared_key).digest()[: self.KEY_SIZE]
    
    def save_shared_key_to_file(self, id):
        if self.shared_key:
            with open(f"shared_key_{id}.bin", "wb") as f:
                f.write(self.shared_key)
            with open(f"hash_{id}.bin", "wb") as f:
                f.write(self.mac_key)
            print("Shared key saved to shared_keys.txt")
        else:
            raise ValueError("Shared key is not established")

    def encrypt_message(self, plaintext: bytes) -> bytes:
        if self.shared_key is None:
            raise ValueError("Shared key not established")

        key = self.shared_key
        key_len = len(key)
        ciphertext = bytes([b ^ key[i % key_len] for i, b in enumerate(plaintext)])
        return ciphertext

    def decrypt_message(self, ciphertext: bytes) -> bytes:
        return self.encrypt_message(ciphertext)

    def encrypt_and_mac(self, plaintext: bytes) -> bytes:
        ciphertext = self.encrypt_message(plaintext)
        mac = hashlib.sha256(self.mac_key + ciphertext).digest()[: self.KEY_SIZE]
        return ciphertext + mac

    def verify_and_decrypt(self, data: bytes) -> bytes:
        if len(data) < self.KEY_SIZE:
            raise ValueError("Data too short to contain MAC")
        ciphertext = data[: -self.KEY_SIZE]
        recv_mac = data[-self.KEY_SIZE :]

        # verification
        expected_mac = hashlib.sha256(self.mac_key + ciphertext).digest()[
            : self.KEY_SIZE
        ]
        if recv_mac != expected_mac:
            raise ValueError("MAC verification failed")

        # decryption
        return self.decrypt_message(ciphertext)
