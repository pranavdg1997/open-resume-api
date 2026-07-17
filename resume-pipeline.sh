#!/bin/bash
# Resume Pipeline Runner
# Generates PDFs from JSON resume files in .resumes/ directory

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="$SCRIPT_DIR/.venv"
PYTHON_SCRIPT="$SCRIPT_DIR/.claude/run_pipeline.py"

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "[ERROR] Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Determine Python executable based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    PYTHON="$VENV_PATH/Scripts/python"
else
    PYTHON="$VENV_PATH/bin/python"
fi

# Run the pipeline
echo "[*] Running Resume Pipeline..."
"$PYTHON" "$PYTHON_SCRIPT" "$@"
