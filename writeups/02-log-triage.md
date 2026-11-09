# Process trail: synthetic log triage

**Type:** local practice challenge  
**Status:** reference walkthrough for the included synthetic log fixture

## Challenge and scope

Reconstruct the four events in `challenges/log_triage/auth.jsonl`, recover the encoded note, and explain why the sequence deserves review. The log is made for this exercise and does not describe a real machine.

## Approach

First inspect the JSONL structure and timestamps. The records show a successful session, an archive of a reports directory, a short encoded note, and a later outbound connection. The destination is in TEST-NET-3, reserved for documentation, so the fixture does not point at a real service.

Run `python -m ctf_lab.forensics`. The helper validates each record, orders by timestamp, and base64-decodes only the explicitly marked `encoded_note` field. The decoded text is `flag{follow_the_process_chain}`.

## Tools and validation

The reference uses Python's standard JSON, datetime, and base64 modules. `pytest` checks the event order and recovered note and verifies that malformed JSON is rejected.

## What I learned

Timeline context matters: archiving reports or connecting to a test address is not enough by itself to establish malicious activity. The event chain is a triage clue in this synthetic exercise, not an incident finding about a real user or host.
