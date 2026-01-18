import hashlib


if __name__ == "__main__":
    with open("shared_key_4.bin", "rb") as f:
        shared_key = f.read()
    with open("hash_4.bin", "rb") as f:
        mac_key = f.read()
    with open("4_message.bin", "rb") as f:
        data = f.read()
    ciphertext = data[:-4]
    recv_mac = data[-4:]
    expected_mac = hashlib.sha256(mac_key + ciphertext).digest()[:4]

    if recv_mac != expected_mac:
        raise ValueError("MAC verification failed")

    key_len = len(shared_key)
    plaintext = bytes([b ^ shared_key[i % key_len] for i, b in enumerate(ciphertext)])

    print("Zaszyfrowana wiadomość z MAC:")
    print(" ".join(str(b) for b in data))

    print("Zaszyfrowana wiadomość bez MAC:")
    print(" ".join(str(b) for b in ciphertext))

    print("Odszyfrowana wiadomość:")
    print(plaintext)