#!/bin/bash
python -m pip install -r requirements.txt

mkdir Datasets
mkdir Datasets/Eli5

python translate.py \
  --input "hf://datasets/sentence-transformers/eli5/pair/train-00000-of-00001.parquet" \
  --column1 "question" \
  --column2 "answer" \
  --output_dir "Datasets/Eli5" \
  --output_filename "eli5-part" \
  --batch_size 8 \
  --chunk_size 50