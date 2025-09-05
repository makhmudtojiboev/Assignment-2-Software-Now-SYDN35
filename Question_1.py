# Mohammed Abir Chowdhury - s397008
# Makhmud Tojiboev - s395965

import os, json
from pathlib import Path

# ================== Utilities ==================
def _shift_alpha(ch: str, k: int) -> str:
    """Shift alphabetic character by k, wrap around (mod 26). Non-letters unchanged."""
    if ch.islower():
        return chr((ord(ch) - 97 + k) % 26 + 97)
    if ch.isupper():
        return chr((ord(ch) - 65 + k) % 26 + 65)
    return ch

def _class_code(ch: str) -> str:
    """Return a classification code for each character."""
    if ch.islower():
        return 'l1' if ch <= 'm' else 'l2'
    if ch.isupper():
        return 'u1' if ch <= 'M' else 'u2'
    return '.'

# ================== Core Encryption / Decryption ==================
def encrypt_text_with_meta(text: str, shift1: int, shift2: int):
    s1, s2 = shift1 % 26, shift2 % 26
    encrypted, meta = [], []

    for ch in text:
        code = _class_code(ch)
        meta.append(code)

        match code:
            case 'l1': encrypted.append(_shift_alpha(ch, (s1 * s2) % 26))
            case 'l2': encrypted.append(_shift_alpha(ch, -(s1 + s2) % 26))
            case 'u1': encrypted.append(_shift_alpha(ch, -s1))
            case 'u2': encrypted.append(_shift_alpha(ch, (s2 * s2) % 26))
            case _:    encrypted.append(ch)

    return ''.join(encrypted), meta

def decrypt_text_with_meta(enc_text: str, shift1: int, shift2: int, meta):
    s1, s2 = shift1 % 26, shift2 % 26
    decrypted = []

    for ch, code in zip(enc_text, meta):
        match code:
            case 'l1': decrypted.append(_shift_alpha(ch, -(s1 * s2) % 26))
            case 'l2': decrypted.append(_shift_alpha(ch, +(s1 + s2) % 26))
            case 'u1': decrypted.append(_shift_alpha(ch, +s1))
            case 'u2': decrypted.append(_shift_alpha(ch, -(s2 * s2) % 26))
            case _:    decrypted.append(ch)

    return ''.join(decrypted)

# ================== File Operations ==================
def encrypt_file(shift1: int, shift2: int,
                 src="raw_text.txt",
                 enc_dst="encrypted_text.txt",
                 meta_dst="encrypted_text.meta"):

    raw = Path(src)
    if not raw.exists():
        raise FileNotFoundError(f"Missing input: {raw.resolve()}")

    text = raw.read_text(encoding="utf-8")
    enc, meta = encrypt_text_with_meta(text, shift1, shift2)

    Path(enc_dst).write_text(enc, encoding="utf-8")
    Path(meta_dst).write_text(json.dumps(meta), encoding="utf-8")

def decrypt_file(shift1: int, shift2: int,
                 enc_src="encrypted_text.txt",
                 dec_dst="decrypted_text.txt",
                 meta_src="encrypted_text.meta"):

    enc, meta_p = Path(enc_src), Path(meta_src)
    if not enc.exists():  raise FileNotFoundError(f"No encrypted file: {enc.resolve()}")
    if not meta_p.exists():
        raise FileNotFoundError(f"Missing meta file: {meta_p.resolve()} "
                                "(required for accurate decryption).")

    enc_text = enc.read_text(encoding="utf-8")
    meta = json.loads(meta_p.read_text(encoding="utf-8"))
    if len(meta) != len(enc_text):
        raise ValueError("Encrypted text and metadata length mismatch.")

    dec = decrypt_text_with_meta(enc_text, shift1, shift2, meta)
    Path(dec_dst).write_text(dec, encoding="utf-8")

    try: os.remove(meta_src)
    except FileNotFoundError: pass

def verify_decryption(raw="raw_text.txt", dec="decrypted_text.txt") -> bool:
    raw_t, dec_t = Path(raw).read_text(encoding="utf-8"), Path(dec).read_text(encoding="utf-8")
    ok = (raw_t == dec_t)
    print("✔ Decryption successful!" if ok else "❌ Decryption failed.")
    return ok

# ================== Main ==================
if __name__ == "__main__":
    s1, s2 = int(input("Enter shift1: ")), int(input("Enter shift2: "))
    if min(s1, s2) < 0:
        print("Invalid shift values.")
    else:
        encrypt_file(s1, s2)
        decrypt_file(s1, s2)
        verify_decryption()
