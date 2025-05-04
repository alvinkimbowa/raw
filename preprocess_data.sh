#!/bin/bash
# This script unzips all zip files in the current directory into their respective folders.

cwd=$(pwd)
root_dir='/home/alvin/UltrAi/Datasets/raw_datasets/cartilage/raw_ultrasound_data/alvin/2025_05_04_all_imaging_modes/Vascular_carotid'
cd "$root_dir"
for rf_file in *.tar; do
    folder="${rf_file%.tar}"
    echo "Processing folder: $folder"
    mkdir -p "$folder"
    tar -xf "$rf_file" -C "$folder"
    video="${folder#*_}".mp4
    echo video "$video"
    mv $root_dir/$video "$folder"
    lzop -d -o "$folder"/*.lzo
done

cd "$cwd"
