#!/bin/bash

SCRIPT_DIR="."
IMAGES_DIR=$SCRIPT_DIR"/../alignments"
for img in `ls ${IMAGES_DIR}`; do
  # Replace occurrences of '-' with '_' in files and stage
  git mv ${IMAGES_DIR}/$img ${IMAGES_DIR}/`echo $img | sed 's/-/_/'`;
done;
