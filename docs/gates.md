# Gate Summary

| Gate | Purpose | Flash allowed? |
|---|---|---:|
| 0 | Device/recovery baseline | No |
| 1 | Samsung source/defconfig mapping | No |
| 2 | Stock-baseline compile | No |
| 3 | Stock-baseline packaging/static verification | No |
| 4 | Manual stock-baseline device smoke test | Manual only |
| 5 | DroidSpaces config build | No |
| 6 | Manual modified-kernel device smoke test | Manual only |
| 7 | DroidSpaces requirements check | N/A |
| 8 | Minimal container | N/A |
| 9 | Full service container | N/A |
| 10 | Docker/Podman | N/A |

A gate fails closed: unresolved evidence blocks the next gate.
