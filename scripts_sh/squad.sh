#!/bin/bash
python -m pip install -r requirements.txt

mkdir Datasets
mkdir Datasets/Squad

python translate.py \
  --input "hf://datasets/sentence-transformers/squad/pair/train-00000-of-00001.parquet" \
  --column1 "question" \
  --column2 "answer" \
  --output_dir "Datasets/Squad" \
  --output_filename "squad-part" \
  --batch_size 8 \
  --chunk_size 50