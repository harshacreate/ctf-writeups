# Reused XOR key: known-prefix recovery

**Type:** local practice challenge  
**Status:** reference walkthrough for the included synthetic ciphertext

## Challenge and scope

Decrypt `challenges/repeating_xor/ciphertext.hex`. The plaintext begins with `flag{`; the same four-byte key repeats across the message.

## Approach

For XOR, ciphertext byte `c[i]` equals plaintext byte `p[i]` XOR key byte `k[i mod 4]`. XORing the first five ciphertext bytes with the known prefix reveals all four key positions; the fifth byte also checks that position zero repeats consistently. The derived key bytes are `4b455921` in hex, which decode to `KEY!`.

Run `python -m ctf_lab.crypto` to repeat the calculation. It prints `flag{reused_xor_keys_need_known_plaintext}`. The code rejects a prefix that conflicts with a previously derived key byte.

## Tools and validation

The helper uses only Python's standard library. Tests verify the exact recovered key and plaintext and ensure an inconsistent known prefix is rejected.

## What I learned

Reusing a short XOR key leaks structure, especially when part of the plaintext is predictable. This deliberately weak construction is a puzzle, not a recommendation for encryption; real cryptographic protocols should use established libraries and authenticated encryption.
