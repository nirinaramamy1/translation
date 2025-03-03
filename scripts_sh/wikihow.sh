#!/bin/bash
python -m pip install -r requirements.txt

wandb login d005488f55ff93ac572938433632aa0c2e651420

python translate.py \
  --input "hf://datasets/sentence-transformers/wikihow/pair/train-00000-of-00001.parquet" \
  --column1 "text" \
  --column2 "summary" \
  --weave_output "wikihow" \
  --batch_size 8 \
  --chunk_size 50