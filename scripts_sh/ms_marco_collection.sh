#!/bin/bash
python -m pip install -r requirements.txt

wandb login d005488f55ff93ac572938433632aa0c2e651420

python translate_ms_marco.py \
  --input "Maminirina1/collection" \
  --column1 "pid" \
  --column2 "passage" \
  --weave_output "ms-marco-collection-mg" \
  --batch_size 8 \
  --chunk_size 50 \
  --range_begin 0 \
  --range_end 10000
