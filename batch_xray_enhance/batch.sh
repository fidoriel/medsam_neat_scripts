!# /bin/bash
mkdir -p /data/enhanced
for i in /data/*; do
    echo "python /app/x-ray-images-enhancement/app.py -a clahe -i $i < /app/quality.in"
done # | parallel -j$(nproc) task