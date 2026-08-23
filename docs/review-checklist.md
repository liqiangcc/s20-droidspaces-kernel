# Review Checklist

Before merging adaptation/build changes, confirm:

- [ ] Exact SM-G9810 firmware properties were captured from the real phone.
- [ ] Samsung source release matches the captured firmware rather than a nearby `x1q` build.
- [ ] Exact device defconfig is identified.
- [ ] Toolchain comes from Samsung build instructions or is otherwise justified with evidence.
- [ ] Stock-baseline build exists before DroidSpaces config changes.
- [ ] Full generated config diff is reviewed.
- [ ] No unrelated KernelSU/SUSFS/performance/security modifications were bundled.
- [ ] Original boot image and SHA256 exist outside the phone.
- [ ] Candidate boot metadata diff is reviewed.
- [ ] Recovery procedure is documented and understood.
- [ ] Flash remains a manual owner action.
