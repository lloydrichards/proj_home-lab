# Keep local configuration private

Public guides use example addresses and placeholders. Public source-repository links, hardware models, generic service paths, and reusable scripts can remain. Keep actual network identifiers, deployed access policies, service endpoints, trusted SSH fingerprints, backup destinations, and recovery details under ignored `local/configuration/`.

The private service register and inventory retain the live records. Other files under that directory preserve the operational values removed from their public counterparts. These files are local operator records, not public documentation dependencies. Read the public guide for the procedure and the private record for its inputs.

## Maintain public examples

Use `<ETHERNET_MAC>` and `<SSH_FINGERPRINT>` for identifiers. Documentation uses `192.0.2.0/24` and `2001:db8::/32` for example network addresses. The Pi-hole guide uses an explicitly identified example private LAN. Substitute actual values before running commands. The public Tailscale policy is an example of policy structure, not a deployable copy of the live policy.

Keep personal documents, receipts, raw machine output, configuration exports, database dumps, and conversation archives outside tracked files. Keep passwords, tokens, and private keys in a password manager or secrets store. Do not put them in public or private Git history.

## Keep private records available

Back up `local/configuration/` through an approved private backup or transfer it to a private notebook. Git does not preserve ignored files. Check that a private backup exists before removing this checkout.

Before staging documentation, inspect `git diff --cached` for actual identifiers and secrets. Confirm that local files remain ignored with `git check-ignore local/configuration/README.md`.

This separation affects the current checkout. Previously committed values remain in Git history and may exist in published copies. Removing historical data is a separate operation. Rotate any exposed credentials before considering history cleanup.
