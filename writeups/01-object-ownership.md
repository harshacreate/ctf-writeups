# Invoice access: object ownership check

**Type:** local practice challenge  
**Status:** reference walkthrough for the included synthetic lab

## Challenge and scope

The toy API accepts a user ID header and returns invoice records. The goal is to request invoice `8802` while identified as user `1001`. The only authorized target is the Flask app in this repository, bound to localhost.

## Approach

Start the app with `python -m challenges.web_access.app`, then send:

```bash
curl -i -H 'X-User-ID: 1001' http://127.0.0.1:5000/api/invoices/8802
```

The response is HTTP 200 and includes the synthetic flag. The header establishes only which toy user the request claims to be. The handler checks that the ID is in a small set, retrieves the invoice by the caller-controlled path ID, and never compares `owner_id` with the caller.

## Tools and validation

`curl` shows the request and status; the Flask test client reproduces the same behavior without a server. `python -m challenges.web_access.secure_app` starts the comparison app. Repeating the request there returns HTTP 404 because the owner check fails. The tests assert both the vulnerable response and patched denial, plus a legitimate owner's access.

## What I learned

Authentication and object authorization are separate checks. A request can identify a valid user and still cross a tenant boundary if the server trusts a resource ID without verifying ownership. The numeric header is a deliberate simplification; it is not a model for real authentication.
