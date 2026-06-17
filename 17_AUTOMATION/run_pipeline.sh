#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

make ecuador

echo "Ecuador pipeline completed. Render reports separately with make report if needed."
