# Tiktok logo remover
Simple discord bot that is capable of bluring tiktok logo of the videos. It is using AI to detect logo


## How to run

You need to install ffmpeg on your system.
Put your shady tiktoks in sample_tiktok folder

Prepare dataset
```bash
python setup_dataset.py
```

Prepare train on dataset
```bash
python train.py
```

When you are done create file config.txt
```bash
YoUr.DiScoRd.Token
!prefix
```

Then run the bot
```bash
python train.py
```
