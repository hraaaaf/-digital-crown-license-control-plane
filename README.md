# -digital-crown-license-control-plane

# Digital Crown License Control Plane

Private control plane for Digital Crown production license signing.

## Security

- Private signing keys must never be committed to this repository.
- Production secrets must never appear in logs or artifacts.
- Only public trust keys may be exported to the Digital Crown client.
- Production signing operations must be explicitly authorized.