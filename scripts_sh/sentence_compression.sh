#!/bin/bash
python -m pip install -r requirements.txt

mkdir Datasets
mkdir Datasets/SentenceCompression

python translate.py \
  --input "hf://datasets/sentence-transformers/sentence-compression/pair/train-00000-of-00001.parquet" \
  --column1 "text" \
  --column2 "simplified" \
  --output_dir "Datasets/SentenceCompression" \
  --output_filename "sentence-compression-part" \
  --batch_size 8 \
  --chunk_size 50