import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

# Load SpaCy language model
nlp = spacy.load("en_core_web_sm")

# Download required NLTK packages
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Load the dataset
file_path = r"datasets/sft_final.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Ensure the dataset has "question" and "answer" columns
if "question" not in data.columns or "answer" not in data.columns:
    raise ValueError("Dataset must contain 'question' and 'answer' columns.")

# Function to calculate lexical diversity
def lexical_diversity(text):
    words = text.split()
    unique_words = set(words)
    return len(unique_words) / len(words) if words else 0

# Function to calculate semantic similarity
def semantic_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)

# Function to calculate average sentence length
def avg_sentence_length(text):
    sentences = sent_tokenize(text)
    total_words = sum(len(word_tokenize(sent)) for sent in sentences)
    return total_words / len(sentences) if sentences else 0

# Function to calculate syntactic simplicity (using POS tagging)
def syntactic_simplicity(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    noun_count = sum(1 for word, tag in pos_tags if tag in ['NN', 'NNS', 'NNP', 'NNPS'])
    verb_count = sum(1 for word, tag in pos_tags if tag.startswith('VB'))
    return noun_count / (verb_count + 1)  # Adding 1 to avoid division by zero

# Function to calculate cosine similarity for documents
def cosine_sim(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

# Analyze the dataset
print("Starting metrics calculation...")
metrics = []
for index, row in data.iterrows():
    question = row["question"]
    answer = row["answer"]
    
    # Calculate metrics
    q_word_count = len(question.split())
    a_word_count = len(answer.split())
    q_lexical_div = lexical_diversity(question)
    a_lexical_div = lexical_diversity(answer)
    avg_sent_len_q = avg_sentence_length(question)
    avg_sent_len_a = avg_sentence_length(answer)
    semantic_sim = semantic_similarity(question, answer)
    syntactic_sim_q = syntactic_simplicity(question)
    syntactic_sim_a = syntactic_simplicity(answer)
    cosine_sim_q_a = cosine_sim(question, answer)
    
    # Append results
    metrics.append({
        "question Word Count": q_word_count,
        "answer Word Count": a_word_count,
        "question Lexical Diversity": q_lexical_div,
        "answer Lexical Diversity": a_lexical_div,
        "Average Sentence Length (Q)": avg_sent_len_q,
        "Average Sentence Length (A)": avg_sent_len_a,
        "Semantic Similarity": semantic_sim,
        "Syntactic Simplicity (Q)": syntactic_sim_q,
        "Syntactic Simplicity (A)": syntactic_sim_a,
        "Cosine Similarity (Q-A)": cosine_sim_q_a
    })

# Create a DataFrame with metrics
metrics_df = pd.DataFrame(metrics)

# Save results to a new CSV
output_path = "output_coh_metrix_results.csv"
metrics_df.to_csv(output_path, index=False)
print(f"Coh-Metrix analysis saved to {output_path}")
