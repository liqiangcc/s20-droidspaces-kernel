#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${1:-out/.config}"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "missing config: $CONFIG_FILE" >&2
  exit 2
fi

required=(
  CONFIG_NAMESPACES
  CONFIG_PID_NS
  CONFIG_IPC_NS
  CONFIG_UTS_NS
  CONFIG_NET_NS
)

recommended=(
  CONFIG_USER_NS
  CONFIG_VETH
)

failed=0

for key in "${required[@]}"; do
  if grep -qx "${key}=y" "$CONFIG_FILE"; then
    echo "PASS required ${key}=y"
  else
    echo "FAIL required ${key}=y" >&2
    failed=1
  fi
done

for key in "${recommended[@]}"; do
  if grep -qx "${key}=y" "$CONFIG_FILE"; then
    echo "PASS recommended ${key}=y"
  else
    echo "WARN recommended ${key} is not y" >&2
  fi
done

exit "$failed"
