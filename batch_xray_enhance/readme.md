# build commands
```bash
sudo docker buildx build -t fidoriel/xray-enhance --load .
```

# run commands
```bash
sudo docker run --rm -it -v ./projections:/data -v ./results:/app/results fidoriel/xray-enhance
```
