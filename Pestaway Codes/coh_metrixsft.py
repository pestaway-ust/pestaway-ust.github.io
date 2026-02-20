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
file_path = r"C:\Users\rache.LAPTOP-II4GEFFH\pestaway\datasets\all datasets\sft_complete.json"   # Update this with your CSV file path
df = pd.read_json(file_path, encoding='utf-8')  # Use 'cp1252' for csv, utf-8 for json

# Initialize lists to store metrics
questions_metrics = []
answers_metrics = []

# Analyze each row
for _, row in df.iterrows():
    question = row['Question']
    answer = row['Answer']
    questions_metrics.append(analyze_text(question))
    answers_metrics.append(analyze_text(answer))

# Convert metrics into dataframes
questions_df = pd.DataFrame(questions_metrics)
answers_df = pd.DataFrame(answers_metrics)

# Merge metrics back with the original dataframe
questions_df = questions_df.add_prefix('Question_')
answers_df = answers_df.add_prefix('Answer_')
result = pd.concat([df, questions_df, answers_df], axis=1)

# Calculate overall Coh-Metrix metrics for English and Tagalog text
def calculate_overall_metrics(df):
    # Select only the numeric columns (exclude the language columns)
    numeric_columns = df.select_dtypes(include=[np.number]).columns

    # Separate English and Tagalog texts
    english_data = df[df['Question_language'] == 'en'][numeric_columns]
    tagalog_data = df[df['Question_language'] == 'tl'][numeric_columns]

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
result['Question_language'] = result['Question_language'].apply(lambda x: 'en' if x == 'en' else 'tl')
result['Answer_language'] = result['Answer_language'].apply(lambda x: 'en' if x == 'en' else 'tl')

# Calculate overall Coh-Metrix for both languages
english_metrics, tagalog_metrics = calculate_overall_metrics(result)

# Print overall Coh-Metrix results for both languages
print("Overall Coh-Metrix for English Text:")
print(english_metrics)
print("\nOverall Coh-Metrix for Tagalog Text:")
print(tagalog_metrics)
