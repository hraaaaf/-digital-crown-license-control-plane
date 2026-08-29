#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def b64url_no_padding(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the Digital Crown production Ed25519 signing keypair locally."
    )
    parser.add_argument(
        "--private-output",
        required=True,
        help="Path OUTSIDE this repository where the private signing material will be written.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    output_path = Path(args.private_output).expanduser().resolve()

    if is_within(output_path, repo_root):
        raise SystemExit("REFUSED: private signing material must be stored outside the repository.")
    if output_path.exists():
        raise SystemExit(f"REFUSED: output already exists: {output_path}")

    private_key = Ed25519PrivateKey.generate()
    private_raw = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_raw = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    private_b64url = b64url_no_padding(private_raw)
    public_b64url = b64url_no_padding(public_raw)
    kid = "dc-prod-" + hashlib.sha256(public_raw).hexdigest()[:16]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(f"DIGITALCROWN_LICENSE_SIGNING_PRIVATE_KEY_B64URL={private_b64url}\n")
        handle.write(f"DIGITALCROWN_LICENSE_SIGNING_KEY_ID={kid}\n")

    print("Generated Digital Crown production Ed25519 keypair.")
    print(f"DIGITALCROWN_LICENSE_SIGNING_KEY_ID={kid}")
    print(f"DIGITALCROWN_LICENSE_SIGNING_PUBLIC_KEY_B64URL={public_b64url}")
    print(f"Private signing material written to: {output_path}")
    print("The private key value was intentionally not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
