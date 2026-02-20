import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from langdetect import detect
from textstat import textstat
import numpy as np

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define function to detect language (English/Tagalog)
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Define function to compute lexical diversity
def lexical_diversity(text):
    words = word_tokenize(text)
    unique_words = set(words)
    return len(unique_words) / len(words) if len(words) > 0 else 0

# Define function to calculate sentence complexity
def sentence_complexity(text):
    sentences = sent_tokenize(text)
    avg_sentence_length = np.mean([len(word_tokenize(sentence)) for sentence in sentences])
    return avg_sentence_length

# Define function to compute Coh-Metrix-like metrics
def analyze_text(text):
    # Ensure text is a string and not empty
    if not isinstance(text, str) or not text.strip():
        return {  # Return empty metrics if text is invalid
            'num_sentences': 0,
            'num_words': 0,
            'lexical_diversity': 0,
            'readability': 0,
            'sentence_complexity': 0,
            'language': 'unknown'
        }
    
    metrics = {}
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    metrics['num_sentences'] = len(sentences)
    metrics['num_words'] = len(words)
    metrics['lexical_diversity'] = lexical_diversity(text)
    metrics['readability'] = textstat.flesch_reading_ease(text)
    metrics['sentence_complexity'] = sentence_complexity(text)
    metrics['language'] = detect_language(text)
    return metrics

# Load dataset
file_path = r"datasets\all datasets\dpo_final.csv"   # Update this with your CSV file path
df = pd.read_csv(file_path)

# Initialize lists to store metrics
prompts_metrics = []
chosen_metrics = []
rejected_metrics = []

# Analyze each row
for _, row in df.iterrows():
    prompt = row['prompt']
    chosen = row['chosen']
    rejected = row['rejected']
    
    # Analyze each of the text columns
    prompts_metrics.append(analyze_text(prompt))
    chosen_metrics.append(analyze_text(chosen))
    rejected_metrics.append(analyze_text(rejected))

# Convert metrics into dataframes
prompts_df = pd.DataFrame(prompts_metrics)
chosen_df = pd.DataFrame(chosen_metrics)
rejected_df = pd.DataFrame(rejected_metrics)

# Merge metrics back with the original dataframe
prompts_df = prompts_df.add_prefix('Prompt_')
chosen_df = chosen_df.add_prefix('Chosen_')
rejected_df = rejected_df.add_prefix('Rejected_')
result = pd.concat([df, prompts_df, chosen_df, rejected_df], axis=1)

# Calculate overall Coh-Metrix metrics for English and Tagalog text
def calculate_overall_metrics(df):
    # Select only the numeric columns (exclude the language columns)
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    # Separate English and Tagalog texts based on language
    english_data = df[df['Prompt_language'] == 'en'][numeric_columns]
    tagalog_data = df[df['Prompt_language'] == 'tl'][numeric_columns]

    # Calculate averages for each group (English and Tagalog)
    if not english_data.empty:
        english_metrics = english_data.mean(axis=0)
    else:
        english_metrics = "No numeric data available for English"

    if not tagalog_data.empty:
        tagalog_metrics = tagalog_data.mean(axis=0)
    else:
        tagalog_metrics = "No numeric data available for Tagalog"

    return english_metrics, tagalog_metrics

# Add language column to the dataframe for easy grouping
result['Prompt_language'] = result['prompt'].apply(lambda x: 'en' if detect_language(x) == 'en' else 'tl')
result['Chosen_language'] = result['chosen'].apply(lambda x: 'en' if detect_language(x) == 'en' else 'tl')
result['Rejected_language'] = result['rejected'].apply(lambda x: 'en' if detect_language(x) == 'en' else 'tl')

# Calculate overall Coh-Metrix for both languages
english_metrics, tagalog_metrics = calculate_overall_metrics(result)

# Print overall Coh-Metrix results for both languages
print("Overall Coh-Metrix for English Text:")
print(english_metrics)
print("\nOverall Coh-Metrix for Tagalog Text:")
print(tagalog_metrics)
