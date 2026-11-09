# Process trail

**Goal:** reconstruct the order of the four synthetic audit events and recover the note embedded in the record. Explain which events form the suspicious sequence and why a single event would be weak evidence on its own.

The artifact is `auth.jsonl`. It contains no real host data. Run the included helper from the repository root with `python -m ctf_lab.forensics`; it validates the required fields, orders events by timestamp, and decodes the marked note. The solution is in [the reference walkthrough](../../writeups/02-log-triage.md).
