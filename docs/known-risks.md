# Known Risks

- Source mismatch: another `x1q` region/build can compile yet be unsafe to flash.
- Toolchain mismatch: Android 4.19 vendor trees can depend on specific Clang/GCC revisions and vendor build flags.
- Config dependencies: enabling a visible Kconfig option may pull dependencies or change generated config beyond the intended fragment.
- Vendor security integration: Samsung kernel/security features must not be disabled casually to make a third-party build script work.
- Boot packaging: Samsung boot image/DTB/DTBO layout must be inspected rather than assumed.
- FBE/data access: a bad kernel may leave userdata intact but temporarily unmountable or undecryptable.
- Bootloop: every candidate requires a known-good stock boot rollback path.
- Container scope creep: Docker/NAT should not be used as the first success criterion; first prove Android boot and DroidSpaces basic container support.
