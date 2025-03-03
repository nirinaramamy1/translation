import torch
import os
import re
import pandas as pd
import argparse

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig
from wtpsplit import SaT
from tqdm import tqdm

def get_args():
    parser = argparse.ArgumentParser(description="Translate dataset using MADLAD model")
    parser.add_argument("--input", type=str, required=True, help="Input Parquet file path")
    parser.add_argument("--column1", type=str, required=True, help="First column name to translate")
    parser.add_argument("--column2", type=str, required=True, help="Second column name to translate")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save translated files")
    parser.add_argument("--output_filename", type=str, default="natural-questions-part", help="Base filename for output files")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for translation")
    parser.add_argument("--chunk_size", type=int, default=1, help="Chunk size for processing")
    return parser.parse_args()

args = get_args()

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype='float16',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type='nf4',
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/madlad400-7b-mt",
    quantization_config=bnb_config,
    device_map="auto"
).to('cuda')

model.config.max_position_embeddings = 512
tokenizer = AutoTokenizer.from_pretrained("google/madlad400-7b-mt", use_fast=True)
tokenizer.model_max_length = 512

model = torch.nn.DataParallel(model)

def translate_batch(texts):
    actual_model = model.module if isinstance(model, torch.nn.DataParallel) else model
    inputs = tokenizer(
        [f"<2mg> {text}" for text in texts],
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding="max_length"
    ).to(next(actual_model.parameters()).device)
    with torch.no_grad():
        outputs = actual_model.generate(
            **inputs,
            max_new_tokens=512,
        )
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)

sat = SaT("sat-3l")
sat.half().to("cuda")

def translate(text, batch_size=8):
    split_phrases = sat.split(text)
    translated_phrases = []
    for i in range(0, len(split_phrases), batch_size):
        batch = split_phrases[i:i + batch_size]
        translated_batch = translate_batch(batch)
        translated_phrases.extend(translated_batch)
    return ''.join(translated_phrases)

tqdm.pandas(desc="Translating")

df = pd.read_parquet(args.input)

if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
    filename = sorted(os.listdir(args.output_dir))[-1]
    match = re.search(r"(?<=part)\d+(?=\.csv)", filename)
    if match:
        part_number = int(match.group(0))
        checkpoint_range = part_number * args.chunk_size
    else:
        part_number = 0
        checkpoint_range = 0
else:
    os.makedirs(args.output_dir, exist_ok=True)
    part_number = 0
    checkpoint_range = 0

chunks = [df[i:i + args.chunk_size] for i in range(checkpoint_range, len(df), args.chunk_size)]
for i, chunk in enumerate(chunks, part_number + 1):
    result = chunk.progress_apply(
        lambda row: [translate(row[args.column1], args.batch_size), translate(row[args.column2], args.batch_size)],
        axis=1, result_type='expand'
    )
    result.columns = [args.column1, args.column2]
    output_file = os.path.join(args.output_dir, f'{args.output_filename}{i}.csv')
    result.to_csv(output_file, index=False)
    torch.cuda.empty_cache()