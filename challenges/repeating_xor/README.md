# Reused XOR key

**Goal:** decrypt `ciphertext.hex`. The plaintext begins with the known prefix `flag{`, and the key is a repeating four-byte string. Recover the key bytes from the prefix, check the repeated position for consistency, and decrypt the whole artifact.

The included helper automates those steps after you try them manually: `python -m ctf_lab.crypto`. The fixture is synthetic. See [the reference walkthrough](../../writeups/03-reused-xor.md) for the derivation and the limitation of this toy cipher.
