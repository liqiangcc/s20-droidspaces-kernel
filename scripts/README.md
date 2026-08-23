# Verification Scripts

- `verify-stock-config.sh [config]` prints the observed namespace/network options from a captured stock config.
- `verify-droidspaces-config.sh [config]` enforces the mandatory namespace options and warns on the extended `USER_NS`/`VETH` target.

These scripts validate configuration only. They do not build or flash the phone.
