#!/usr/bin/env bash
# Cadence Pre-Commit Verification Hook
# Enforces deterministic Oracle certification and Archival CAS integrity before commit.
#
# To install:
#   ln -s ../../scripts/pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
PYTHON_CMD="python3"

if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# 1. Oracle Certification Gate (if contracts or accelerated compute code is touched)
if [ -d "$REPO_ROOT/.experiments/certificates" ]; then
    echo "🔬 [Cadence] Verifying Layered Oracle Certification & Canonical Tree SHA..."
    $PYTHON_CMD "$REPO_ROOT/scripts/verify_oracle.py" --verify-staged
fi

# 2. Scientific Failure Archival CAS Gate (if .experiments records exist)
if [ -d "$REPO_ROOT/.experiments" ]; then
    echo "🗄️ [Cadence] Verifying Scientific Archival & CAS SHA-256 integrity..."
    $PYTHON_CMD "$REPO_ROOT/scripts/verify_archival.py" --verify-all
fi

echo "✅ [Cadence] Pre-commit verification passed."
exit 0
