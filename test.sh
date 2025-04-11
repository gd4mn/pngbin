#!/bin/bash

# filepath: /Users/albertfreeman/Projects/pngbin/temp_script.sh

# Create temporary directories
SOURCE_DIR="source_dir"
GALLERY_DIR="gallery_dir"

# Create the source and gallery directories
mkdir -p "$SOURCE_DIR"
mkdir -p "$GALLERY_DIR"

# Create 20 custom-named .png files in the source directory
for i in {1..20}; do
  touch "$SOURCE_DIR/image_$i.png"
done

# Create 55 custom-named subfolders in the gallery directory
for i in {1..55}; do
  mkdir "$GALLERY_DIR/folder_$i"
done

# Create a hidden directory in the gallery directory
mkdir "$GALLERY_DIR/.hidden"

# Create a read-only directory in the gallery directory
READ_ONLY_DIR="$GALLERY_DIR/read_only"
mkdir "$READ_ONLY_DIR"
chmod 555 "$READ_ONLY_DIR"

# Run pngbin with the source and gallery directories
python3 ./pngbin.py "$SOURCE_DIR" "$GALLERY_DIR"

# Check for -k parameter to decide whether to keep directories
if [[ "$1" != "-k" ]]; then
  # Remove the directories
  rm -rf "$SOURCE_DIR" "$GALLERY_DIR"
else
  echo "Directories kept for manual testing:"
  echo "Source Directory: $SOURCE_DIR"
  echo "Gallery Directory: $GALLERY_DIR"
fi