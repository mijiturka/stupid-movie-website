#!/bin/bash

SCRIPT_DIR="."
REVIEWS_DIR=${SCRIPT_DIR}"/../reviews"

FILE_TO_WRITE_TO="${SCRIPT_DIR}/generate_film_list/seen-in-2021.md"

pushd ${REVIEWS_DIR}
LIST=$(grep -rl "2021" | sed "s/.html//")
popd

echo "$LIST" > ${FILE_TO_WRITE_TO}
echo "Results written to ${FILE_TO_WRITE_TO}"
