#!/bin/bash
# made for https://github.com/asalmada/x-ray-images-enhancement
# you might need to remove scipy from requirements.txt scipy will be installed as dependency from scipy-image
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <image_directory>"
    exit 1
fi

echo "clear tmp dir"
rm -rf results/*

input_directory="$1"

output_directory="output_images"
mkdir -p "$output_directory"

for image_path in "$input_directory"/*.tif; do
    filename_without_extension=$(basename -- "$image_path" .tif)

    echo "processing $filename_without_extension"

    python app.py -a clahe -i "$image_path" < "test_cases/clahe/100_150_1.in"

    find results -name "*$filename_without_extension*" | xargs -i mv {} $output_directory/$filename_without_extension.jpeg
done

echo "Processing complete. Output files are in the '$output_directory'