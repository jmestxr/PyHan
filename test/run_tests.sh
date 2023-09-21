#!/bin/bash

# Console output text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR=$(dirname "$0")
PYHAN_COMPILER="${SCRIPT_DIR}/../src/compiler.py"
TEST_FILES_DIR="${SCRIPT_DIR}/test-files"
TEST_OUTDIR="${SCRIPT_DIR}/__test-outdir__"
EXPECTED_DIR="${SCRIPT_DIR}/expected"

# Create outdir if does not exist
mkdir -p "${TEST_OUTDIR}"

num_tests_failed=0

echo "--------------------------------------------------------"

# Iterate over test files
for test_file_path in "${TEST_FILES_DIR}"/*.pyhan; do
    test_file=$(basename "$test_file_path")
    actual_output_file="${TEST_OUTDIR}/${test_file%.*}.py"
    expected_output_file="${EXPECTED_DIR}/${test_file%.*}.py"
    
    echo "Running test: ${test_file}"
    python "${PYHAN_COMPILER}" "${test_file_path}" "${actual_output_file}"
    if cmp -s "${expected_output_file}" "${actual_output_file}"
    then
        echo -e "${GREEN}Test passed${NC}"
    else
        echo -e "${RED}Test failed${NC}"
        num_tests_failed=$((num_tests_failed + 1))
    fi
    echo "--------------------------------------------------------"
done

if [ "${num_tests_failed}" -eq 0 ]
then 
    echo -e "${GREEN}All tests passed! 🥳${NC}"
else
    echo -e "${RED}${num_tests_failed} tests failed 😞${NC}"
fi
