#!/bin/bash


MODEL_PATH=pytorch_bert_zh_model
VOCAB_PATH=data/output_vocabulary/
BASE_PATH=ctc2021_baseline/best.th
INPUT_FILE=qualification_input.txt
OUTPUT_FILE=${INPUT_FILE}.output

python segment.py < $INPUT_FILE > ${INPUT_FILE}.tok


CUDA_VISIBLE_DEVICES=0 python predict.py \
    --transformer_model $MODEL_PATH \
    --special_tokens_fix 0 \
    --iteration_count 3 \
    --model_path $MODEL_PATH/pytorch_model.bin \
    --vocab_path $VOCAB_PATH \
    --input_file ${INPUT_FILE}.tok \
    --output_file $OUTPUT_FILE \
    --additional_confidence 0. \
    --min_error_probability 0.

python convert_from_sentpair_to_edits.py ${INPUT_FILE}.tok $OUTPUT_FILE $INPUT_FILE > ${INPUT_FILE}.result
