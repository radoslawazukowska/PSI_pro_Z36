from dataclasses import dataclass
from typing import Optional


@dataclass
class Session:
    private_key: Optional[bytes] = None
    public_key: Optional[bytes] = None
    peer_public_key: Optional[bytes] = None

    shared_key: Optional[bytes] = None
    mac_key: Optional[bytes] = None

    established: bool = False

    def generate_keys():
        pass

    def set_peer_key(peer_key):
        pass

    def encrypt_and_mac(plaintext):
        pass

    def verify_and_decrypt(ciphertext):
        pass
