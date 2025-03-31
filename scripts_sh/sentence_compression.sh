#!/bin/bash
python -m pip install -r requirements.txt

wandb login 2570172483ba90dcd524a971e6a6efe6aa0f6581

python translate.py \
  --input "hf://datasets/sentence-transformers/sentence-compression/pair/train-00000-of-00001.parquet" \
  --column1 "text" \
  --column2 "simplified" \
  --weave_output "sentence-compression" \
  --batch_size 8 \
  --chunk_size 50 \
  --range_begin 0 \
  --range_end 10000