#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${1:-stock.config}"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "missing config: $CONFIG_FILE" >&2
  exit 2
fi

keys=(
  CONFIG_NAMESPACES
  CONFIG_PID_NS
  CONFIG_IPC_NS
  CONFIG_UTS_NS
  CONFIG_NET_NS
  CONFIG_USER_NS
  CONFIG_VETH
)

for key in "${keys[@]}"; do
  if grep -q "^${key}=" "$CONFIG_FILE"; then
    grep "^${key}=" "$CONFIG_FILE"
  elif grep -q "^# ${key} is not set$" "$CONFIG_FILE"; then
    grep "^# ${key} is not set$" "$CONFIG_FILE"
  else
    echo "${key}: absent"
  fi
done
