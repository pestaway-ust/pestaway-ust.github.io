import pandas as pd
import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import evaluate
import os
from torch.utils.data import DataLoader
from time import time

# ---------------------- Initialization ----------------------
start_time = time()
model_name = r"D:\Downloads\LATEST\out_finetuned1_Epoch_5\checkpoint-125"  # Replace with your model path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

# Fix tokenizer padding settings
tokenizer.padding_side = "left"
tokenizer.pad_token = tokenizer.eos_token  # Assign pad token explicitly

# Load the ground truth dataset
ground_truth_file = r"C:\Users\Nickolas\OneDrive\Documents\pestaway\ngroundtruth.parquet"
ground_truth_df = pd.read_parquet(ground_truth_file)

# Extract questions and reference answers
questions = ground_truth_df['question'].tolist()
references = ground_truth_df['answer'].tolist()

# Separate English and Tagalog (if already tagged in your dataset)
english_indices = [i for i, q in enumerate(questions) if q.isascii()]
tagalog_indices = [i for i in range(len(questions)) if i not in english_indices]

# ---------------------- Generate Predictions ----------------------
print("Generating predictions...")
generation_start = time()
batch_size = 8
data_loader = DataLoader(questions, batch_size=batch_size)

predictions = []
for batch in data_loader:
    inputs = tokenizer(list(batch), return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs['input_ids'].to(model.device)
    attention_mask = inputs['attention_mask'].to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=512,
            num_beams=5,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

    batch_predictions = [
        tokenizer.decode(output, skip_special_tokens=True) for output in outputs
    ]
    predictions.extend(batch_predictions)

print(f"Generation Time: {time() - generation_start:.2f} seconds")

# ---------------------- Save Predictions ----------------------
predictions_data = [
    {"question": q, "reference": r, "prediction": p}
    for q, r, p in zip(questions, references, predictions)
]

predictions_json_path = r"C:\Users\Nickolas\OneDrive\Documents\pestaway\ORPO EVAL\seallm.json"
os.makedirs(os.path.dirname(predictions_json_path), exist_ok=True)
with open(predictions_json_path, 'w', encoding='utf-8') as f:
    json.dump(predictions_data, f, ensure_ascii=False, indent=4)

# ---------------------- Load Evaluation Metrics ----------------------
print("Loading evaluation metrics...")
evaluation_start = time()
bleu = evaluate.load("bleu")
meteor = evaluate.load("meteor")
rouge = evaluate.load("rouge")
bertscore = evaluate.load("bertscore")

# ---------------------- Evaluate English and Tagalog Separately ----------------------
print("Evaluating English and Tagalog...")

def evaluate_metrics(predictions, references, language):
    bleu_results = bleu.compute(predictions=predictions, references=references)
    meteor_results = meteor.compute(predictions=predictions, references=references)
    rouge_results = rouge.compute(predictions=predictions, references=references)
    bertscore_results = bertscore.compute(predictions=predictions, references=references, model_type='bert-base-multilingual-cased')
    avg_bertscore = sum(bertscore_results['f1']) / len(bertscore_results['f1'])
    
    return {
        'BLEU': bleu_results['bleu'],
        'METEOR': meteor_results['meteor'],
        'ROUGE': rouge_results,
        'BERTScore': avg_bertscore
    }

# Separate predictions and references
eng_predictions = [predictions[i] for i in english_indices]
eng_references = [references[i] for i in english_indices]

tag_predictions = [predictions[i] for i in tagalog_indices]
tag_references = [references[i] for i in tagalog_indices]

english_scores = evaluate_metrics(eng_predictions, eng_references, "English")
tagalog_scores = evaluate_metrics(tag_predictions, tag_references, "Tagalog")

# ---------------------- Evaluate Perplexity ----------------------
def calculate_perplexity(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs['input_ids'])
        loss = outputs.loss
    return torch.exp(loss).item()

perplexities = [calculate_perplexity(model, tokenizer, pred) for pred in predictions]
average_perplexity = sum(perplexities) / len(perplexities)

print(f"Evaluation Time: {time() - evaluation_start:.2f} seconds")

# ---------------------- Save Evaluation Results ----------------------
evaluation_results_excel_path = r"C:\Users\Nickolas\OneDrive\Documents\pestaway\ORPO EVAL\seallm.xlsx"
results_df = pd.DataFrame([
    {'Metric': 'BLEU', 'English': english_scores['BLEU'], 'Tagalog': tagalog_scores['BLEU']},
    {'Metric': 'METEOR', 'English': english_scores['METEOR'], 'Tagalog': tagalog_scores['METEOR']},
    {'Metric': 'ROUGE', 'English': english_scores['ROUGE'], 'Tagalog': tagalog_scores['ROUGE']},
    {'Metric': 'BERTScore', 'English': english_scores['BERTScore'], 'Tagalog': tagalog_scores['BERTScore']},
    {'Metric': 'Average Perplexity', 'English': average_perplexity, 'Tagalog': average_perplexity}
])
results_df.to_excel(evaluation_results_excel_path, index=False)

print(f"Total Time Elapsed: {time() - start_time:.2f} seconds")
print("Evaluation completed and results saved.")
