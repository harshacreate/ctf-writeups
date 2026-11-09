"""Patched comparison app for the local invoice authorization exercise."""

from __future__ import annotations

import os

from flask import Flask, jsonify, request

from .app import INVOICES, KNOWN_USERS


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/api/invoices/<int:invoice_id>")
    def get_invoice(invoice_id: int):
        try:
            user_id = int(request.headers.get("X-User-ID", ""))
        except ValueError:
            return jsonify(error="a known X-User-ID is required"), 401
        if user_id not in KNOWN_USERS:
            return jsonify(error="a known X-User-ID is required"), 401
        invoice = INVOICES.get(invoice_id)
        if invoice is None or invoice["owner_id"] != user_id:
            return jsonify(error="invoice not found"), 404
        return jsonify(invoice_id=invoice_id, **invoice)

    return app


if __name__ == "__main__":
    create_app().run(
        host=os.environ.get("CTF_BIND_HOST", "127.0.0.1"),
        port=int(os.environ.get("CTF_PORT", "5000")),
        debug=False,
    )
