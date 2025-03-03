#!/bin/bash
python -m pip install -r requirements.txt

mkdir Datasets
mkdir Datasets/Wikihow

python translate.py \
  --input "hf://datasets/sentence-transformers/wikihow/pair/train-00000-of-00001.parquet" \
  --column1 "text" \
  --column2 "summary" \
  --output_dir "Datasets/Wikihow" \
  --output_filename "wikihow-part" \
  --batch_size 8 \
  --chunk_size 50