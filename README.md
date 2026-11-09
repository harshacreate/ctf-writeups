# CTF Practice Lab

Three small, reproducible CTF-style exercises for practicing web authorization review, log triage, and a known-plaintext XOR puzzle. Each has a local fixture and a reference walkthrough.

[![CI](https://github.com/harshacreate/ctf-writeups/actions/workflows/ci.yml/badge.svg)](https://github.com/harshacreate/ctf-writeups/actions/workflows/ci.yml)

## Scope and provenance

The exercises and artifacts in this repository are synthetic and self-contained. The walkthroughs are reference solutions for these included labs; they are not writeups from the Vel Tech CTF or claims about a placement, a third-party challenge, or an event solve. The web exercise is intentionally vulnerable and should only be run on localhost or in the provided container.

## Challenges

| Exercise | Focus | Start here |
|---|---|---|
| Invoice access | Object-level authorization and a local request trace | [Challenge](challenges/web_access/README.md) · [Walkthrough](writeups/01-object-ownership.md) |
| Process trail | Timeline reconstruction from synthetic JSONL audit events | [Challenge](challenges/log_triage/README.md) · [Walkthrough](writeups/02-log-triage.md) |
| Reused XOR key | Recovering a repeating XOR key from a known prefix | [Challenge](challenges/repeating_xor/README.md) · [Walkthrough](writeups/03-reused-xor.md) |

## Run it

Requires Python 3.9 or later. The log and crypto exercises work offline. The web lab can run directly with Flask or in Docker, bound to localhost.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m ctf_lab.forensics
python -m ctf_lab.crypto
```

For the vulnerable web exercise:

```bash
python -m challenges.web_access.app
# In another terminal, use the documented request in the challenge walkthrough.
```

Or run `docker compose up --build`; the published port is bound to `127.0.0.1:5000`. To compare the patched implementation, start it with `python -m challenges.web_access.secure_app`.

## Design notes

- The web lab checks that a caller is known but omits invoice ownership validation. A paired secure app adds the missing object check so the behavior can be compared with tests.
- The log and crypto artifacts are checked into the repository so the walkthroughs can be repeated without an external service or dataset.
- Tests cover the expected vulnerable behavior, the authorization fix, fixture parsing, and both challenge solvers.

## Limitations

These are small teaching exercises, not a security assessment toolkit. The web app uses a plain numeric header as an intentionally simplified identity and has no real authentication. The logs do not represent a real host, and the XOR puzzle is deliberately weak. Do not reuse the toy authorization design in an application.

## License

MIT. See [LICENSE](LICENSE).
