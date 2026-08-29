# Digital Crown License Control Plane

Private control plane for Digital Crown production license signing.

## Security

- Private signing keys must never be committed to this repository.
- Production secrets must never appear in logs or artifacts.
- Only public trust keys may be exported to the Digital Crown client.
- Production signing operations must be explicitly authorized.

## Generate the production Ed25519 keypair locally

Run this on the trusted Windows control-plane machine, not in GitHub Actions.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\generate_ed25519.py --private-output "$env:USERPROFILE\DigitalCrownSecrets\license-signing.private.env"
```

The command prints only:

- `DIGITALCROWN_LICENSE_SIGNING_KEY_ID`
- `DIGITALCROWN_LICENSE_SIGNING_PUBLIC_KEY_B64URL`

The private signing key is written only to the requested path outside this repository and is never printed.

## GitHub Actions provisioning

In **Settings > Secrets and variables > Actions** configure:

Repository secrets:

- `DIGITALCROWN_LICENSE_SIGNING_PRIVATE_KEY_B64URL`
- `DIGITALCROWN_LICENSE_SIGNING_KEY_ID`

Repository variable:

- `DIGITALCROWN_LICENSE_SIGNING_PUBLIC_KEY_B64URL`

Then manually run **Validate production license signing** once. The workflow verifies the private/public Ed25519 match and performs an in-memory sign/verify test without exporting private material.
