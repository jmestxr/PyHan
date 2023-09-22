#!/bin/bash

# Console output text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NO_COLOR='\033[0m' # No Color

# Directories
SCRIPT_DIR=$(dirname "$0")
PYHAN_COMPILER="${SCRIPT_DIR}/../src/compiler.py"
NEGATIVE_TEST_FILES_DIR="${SCRIPT_DIR}/test-files/negative-tests"
POSITIVE_TEST_FILES_DIR="${SCRIPT_DIR}/test-files/positive-tests"
TEST_OUTDIR="${SCRIPT_DIR}/__test-outdir__"
EXPECTED_DIR="${SCRIPT_DIR}/expected"

# Create outdir if does not exist
mkdir -p "${TEST_OUTDIR}"

# Clear all files in __test-outdir__
echo "Clearing all previous test output files..."
if [ "$(ls -A "$TEST_OUTDIR")" ]
then
    rm ${TEST_OUTDIR}/*
fi

num_tests_failed=0

echo "--------------------------------------------------------"

# Iterate over positive test files
for test_file_path in "${POSITIVE_TEST_FILES_DIR}"/*.pyhan; do
    test_file=$(basename "$test_file_path")
    actual_output_file="${TEST_OUTDIR}/${test_file%.*}.py"
    expected_output_file="${EXPECTED_DIR}/${test_file%.*}.py"
    
    echo "Running positive test: ${test_file}"
    python "${PYHAN_COMPILER}" "${test_file_path}" "${actual_output_file}"
    if cmp -s "${expected_output_file}" "${actual_output_file}"
    then
        echo -e "${GREEN}Test passed${NO_COLOR}"
    else
        echo -e "${RED}Test failed${NO_COLOR}"
        num_tests_failed=$((num_tests_failed + 1))
    fi
    echo "--------------------------------------------------------"
done

# Iterate over negative test files
for test_file_path in "${NEGATIVE_TEST_FILES_DIR}"/*.pyhan; do
    test_file=$(basename "$test_file_path")

    echo "Running negative test: ${test_file}"
    if python "${PYHAN_COMPILER}" "${test_file_path}" "${actual_output_file}"
    then
        echo -e "${RED}Test failed${NO_COLOR}"
        num_tests_failed=$((num_tests_failed + 1))
    else
        echo -e "${GREEN}Test passed${NO_COLOR}"
    fi
    echo "--------------------------------------------------------"
done

if [ "${num_tests_failed}" -eq 0 ]
then 
    echo -e "${GREEN}All tests passed! 🥳${NO_COLOR}"
else
    echo -e "${RED}${num_tests_failed} tests failed 😞${NO_COLOR}"
fi
