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
```
for file in *.png; do convert "$file" -depth 16 -type Grayscale -compress none "../teapod_tif/${file%.png}.tif"; done
```