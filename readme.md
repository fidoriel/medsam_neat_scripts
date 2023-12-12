# Scripts 3D MedSAM Segmentation with NeAT

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Convert to Monochrome for NeAT
```
for file in *.tif; do convert "$file" -monochrome  "$file"; done
```