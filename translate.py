import torch
import os
import re
import pandas as pd
import argparse
import weave
import warnings

from weave import Dataset
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, BitsAndBytesConfig
from wtpsplit import SaT
from tqdm import tqdm

warnings.simplefilter("ignore", DeprecationWarning)

def get_args():
    parser = argparse.ArgumentParser(description="Translate dataset using MADLAD model")
    parser.add_argument("--input", type=str, required=True, help="Input Parquet file path")
    parser.add_argument("--column1", type=str, required=True, help="First column name to translate")
    parser.add_argument("--column2", type=str, required=True, help="Second column name to translate")
    parser.add_argument("--weave_output", type=str, required=True, help="Base filename for output files to weave dataset")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for translation")
    parser.add_argument("--chunk_size", type=int, default=50, help="Chunk size for processing")
    parser.add_argument("--range_begin", type=int, required=True, help="Begin from this range the translation")
    parser.add_argument("--range_end", type=int, required=True, help="End to this range the translation")
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
df_last = df.iloc[::-1].reset_index(drop=True)


weave.init(f'{args.weave_output}')
# try:
#     df_ref = weave.ref(f'{args.weave_output}').get().to_pandas()
# except:
#     df_ref = pd.DataFrame([
#         {f'{args.column1}': '', f'{args.column2}': ''}
#     ])

# chunks = [df[i:i + args.chunk_size] for i in range(len(df_ref)+args.range_begin, len(df_ref)+args.range_end, args.chunk_size)]
chunks = [df_last[i:i + args.chunk_size] for i in range(args.range_begin, args.range_end, args.chunk_size)]
for chunk in chunks:
    result = chunk.progress_apply(
        lambda row: [translate(row[args.column1], args.batch_size), translate(row[args.column2], args.batch_size)],
        axis=1, result_type='expand'
    )
    result.columns = [args.column1, args.column2]
    # df_pub = pd.concat([df_ref, result], axis=0, ignore_index=0)
    dataset = Dataset(
        name=f'{args.weave_output}',
        rows=result.to_dict(orient='records')
        # rows=df_pub.to_dict(orient='records')
    )
    weave.publish(dataset)
    # df_ref = weave.ref(f'{args.weave_output}').get().to_pandas()
    # chunks = [df[i:i + args.chunk_size] for i in range(len(df_ref)+args.range_begin, len(df), args.chunk_size)]
    torch.cuda.empty_cache()