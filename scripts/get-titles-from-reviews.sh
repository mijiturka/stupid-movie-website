#!/bin/bash

SCRIPT_DIR="."
REVIEWS_DIR=${SCRIPT_DIR}"/../reviews"

for review in `ls ${REVIEWS_DIR}`; do
  cat ${REVIEWS_DIR}/${review} | head -1;
done;
