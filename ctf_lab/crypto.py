"""Solver for the included repeating-key XOR practice fixture."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CIPHERTEXT = ROOT / "challenges" / "repeating_xor" / "ciphertext.hex"


def recover_repeating_xor(
    ciphertext: bytes, known_prefix: bytes = b"flag{", key_size: int = 4
) -> tuple[bytes, bytes]:
    """Recover a repeating key from a known plaintext prefix and decrypt bytes."""
    if key_size < 1:
        raise ValueError("key_size must be positive")
    if not known_prefix or len(ciphertext) < len(known_prefix):
        raise ValueError("ciphertext must cover a non-empty known prefix")

    key: list[Optional[int]] = [None] * key_size
    for index, plain_byte in enumerate(known_prefix):
        slot = index % key_size
        candidate = ciphertext[index] ^ plain_byte
        if key[slot] is not None and key[slot] != candidate:
            raise ValueError("known prefix is inconsistent with the repeating key")
        key[slot] = candidate

    if any(byte is None for byte in key):
        raise ValueError("known prefix does not reveal every key byte")
    recovered_key = bytes(byte for byte in key if byte is not None)
    plaintext = bytes(value ^ recovered_key[index % key_size]
                      for index, value in enumerate(ciphertext))
    if not plaintext.startswith(known_prefix):
        raise ValueError("recovered plaintext does not match the known prefix")
    return recovered_key, plaintext


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ciphertext", nargs="?", type=Path, default=DEFAULT_CIPHERTEXT)
    parser.add_argument("--key-size", type=int, default=4)
    args = parser.parse_args(argv)
    raw_hex = args.ciphertext.read_text(encoding="utf-8").strip()
    try:
        ciphertext = bytes.fromhex(raw_hex)
    except ValueError as exc:
        parser.error(f"invalid hexadecimal ciphertext: {exc}")
    key, plaintext = recover_repeating_xor(ciphertext, key_size=args.key_size)
    print(f"key_hex={key.hex()}")
    print(f"plaintext={plaintext.decode('utf-8')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
