#!/bin/bash

# Directories
SCRIPT_DIR=$(dirname "$0")
PYHAN_COMPILER="${SCRIPT_DIR}/../src/compiler.py"
TEST_FILES_DIR="${SCRIPT_DIR}/test-files"
TEST_OUTDIR="${SCRIPT_DIR}/__test-outdir__"

# Iterate over test files
for test_file_path in "${TEST_FILES_DIR}"/*.pyhan; do
    test_file=$(basename "$test_file_path")
    echo "Running test: ${test_file}"
    python "${PYHAN_COMPILER}" "${test_file_path}" "${TEST_OUTDIR}/${test_file%.*}.py"
done
