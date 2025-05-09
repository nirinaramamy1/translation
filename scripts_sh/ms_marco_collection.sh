#!/bin/bash
python -m pip install -r requirements.txt

wandb login 2570172483ba90dcd524a971e6a6efe6aa0f6581

python translate_ms_marco.py \
  --input "Maminirina1/collection" \
  --column1 "pid" \
  --column2 "passage" \
  --weave_output "ms-marco-collection-mg" \
  --batch_size 8 \
  --chunk_size 50 \
  --range_begin 0 \
  --range_end 10000
