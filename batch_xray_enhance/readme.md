# build commands
```bash
docker buildx build . -t fidoriel/xray-batch-enhance --load
```

# run commands
```bash
docker run --rm --init -v ./data:/data/ -v ./results:/app/results fidoriel/xray-batch-enhance bash /app/batch.sh
```
