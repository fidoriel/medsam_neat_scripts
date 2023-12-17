# Scripts 3D MedSAM Segmentation with NeAT

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Convert for MedSAM
```
for file in *.tif; do convert "$file" -depth 8 -colorspace Gray -format PNG -compress none "../teapod_png/${file%.tif}.png"; done
```

Convert MedSAM to NeAT
for whole image with mask
```
for file in *.png; do convert "$file" -depth 16 -type Grayscale -compress none "../teapod_tif/${file%.png}.tif"; done
```

for mask only
```
for file in *.png; do convert "$file" \( -clone 0 -colorspace gray -negate \) -compose over -composite -background white -alpha remove -flatten -depth 16 -type Grayscale -compress none  "${file%.tif}_white.tif"; done
```