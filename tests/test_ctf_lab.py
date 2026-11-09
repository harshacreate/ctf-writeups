import json
import subprocess
import sys
from pathlib import Path

import pytest

from challenges.web_access.app import create_app as create_vulnerable_app
from challenges.web_access.secure_app import create_app as create_secure_app
from ctf_lab.crypto import DEFAULT_CIPHERTEXT, recover_repeating_xor
from ctf_lab.forensics import DEFAULT_LOG, read_events, summarize


ROOT = Path(__file__).resolve().parents[1]


def test_vulnerable_app_exposes_other_users_invoice_and_secure_app_denies_it():
    vulnerable = create_vulnerable_app().test_client()
    secure = create_secure_app().test_client()
    headers = {"X-User-ID": "1001"}

    exposed = vulnerable.get("/api/invoices/8802", headers=headers)
    denied = secure.get("/api/invoices/8802", headers=headers)
    legitimate = secure.get("/api/invoices/3101", headers=headers)

    assert exposed.status_code == 200
    assert exposed.json["memo"] == "flag{object_ids_are_not_authorization}"
    assert denied.status_code == 404
    assert legitimate.status_code == 200


def test_web_app_requires_known_user_header():
    response = create_vulnerable_app().test_client().get("/api/invoices/3101")
    assert response.status_code == 401


def test_repeating_xor_fixture_recovers_key_and_plaintext():
    ciphertext = bytes.fromhex(DEFAULT_CIPHERTEXT.read_text(encoding="utf-8"))
    key, plaintext = recover_repeating_xor(ciphertext)
    assert key == b"KEY!"
    assert plaintext == b"flag{reused_xor_keys_need_known_plaintext}"


def test_repeating_xor_rejects_inconsistent_prefix():
    with pytest.raises(ValueError, match="inconsistent"):
        recover_repeating_xor(bytes.fromhex("0000000000"), b"flag{", 4)


def test_log_fixture_orders_events_and_decodes_note():
    summary = summarize(read_events(DEFAULT_LOG))
    assert summary["event_ids"] == ["log-01", "log-02", "log-03", "log-04"]
    assert summary["decoded_notes"] == ["flag{follow_the_process_chain}"]


def test_log_parser_rejects_malformed_json(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text("{broken}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        read_events(path)


def test_log_parser_rejects_missing_fields(tmp_path):
    path = tmp_path / "missing.jsonl"
    path.write_text(json.dumps({"event_id": "x"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required fields"):
        read_events(path)


@pytest.mark.parametrize(
    ("module", "expected"),
    [
        ("ctf_lab.crypto", "flag{reused_xor_keys_need_known_plaintext}"),
        ("ctf_lab.forensics", "flag{follow_the_process_chain}"),
    ],
)
def test_cli_modules_print_reference_solution(module, expected):
    result = subprocess.run(
        [sys.executable, "-m", module], cwd=ROOT, text=True, capture_output=True, check=True
    )
    assert expected in result.stdout
