#!/bin/bash
python -m pip install -r requirements.txt

wandb login d005488f55ff93ac572938433632aa0c2e651420

python translate.py \
  --input "hf://datasets/sentence-transformers/squad/pair/train-00000-of-00001.parquet" \
  --column1 "question" \
  --column2 "answer" \
  --weave_output "squad" \
  --batch_size 8 \
  --chunk_size 50