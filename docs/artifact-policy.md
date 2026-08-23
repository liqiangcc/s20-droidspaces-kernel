# Artifact Policy

Binary kernel/boot/firmware artifacts are not committed by default.

Commit source/configuration/scripts/checksums and human-readable metadata. Keep large or redistribution-sensitive binaries outside git and reference them by exact filename and SHA256.

A release artifact may be published later only after model/firmware compatibility, license/redistribution terms, test status, and rollback instructions are explicit.
