#!/bin/bash
python -m pip install -r requirements.txt

wandb login 2570172483ba90dcd524a971e6a6efe6aa0f6581

python translate_ms_marco.py \
  --input "https://drive.google.com/uc?id=12FmGAOSalPy4MRnKtrdbsATlwfvYzArc" \
  --output "queries.tsv" \
  --column1 "qid" \
  --column2 "query" \
  --weave_output "ms-marco-queries" \
  --batch_size 8 \
  --chunk_size 50 \
  --range_begin 0 \
  --range_end 10000
