# Invoice access

This local Flask exercise shows why checking a caller identity is not enough to authorize access to a specific record. The vulnerable API accepts a valid user ID but does not verify invoice ownership; `secure_app.py` adds that check.

## Run locally

From the repository root, install the requirements and start the vulnerable version:

```bash
python -m pip install -r requirements.txt
python -m challenges.web_access.app
```

In another terminal, request the other user’s synthetic invoice:

```bash
curl -i -H 'X-User-ID: 1001' http://127.0.0.1:5000/api/invoices/8802
```

The patched comparison listens on the same local port, so stop the first process before running `python -m challenges.web_access.secure_app`. The same request is denied there. Run `python -m pytest -q` to compare both behaviors without starting a server.

## Scope

The `X-User-ID` header is a deliberately simplified lab identity, not real authentication. The records and flag are synthetic. Run only on localhost or in the provided container, and do not reuse this toy design in an application. See [the reference walkthrough](../../writeups/01-object-ownership.md).
