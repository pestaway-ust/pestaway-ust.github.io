import pandas as pd
from readability import Readability
import nltk

# Ensure punkt and punkt_tab tokenizers are downloaded
nltk.download('punkt')
nltk.download('punkt_tab')

# Step 1: Load your CSV file
df = pd.read_csv(r'C:\Users\Carlo PC\Documents\pestaway\dpodataset.csv')
print("Columns in DataFrame:", df.columns)

# Step 2: Extract text data from specific columns
texts = pd.concat([df['prompt'], df['chosen'], df['rejected']]).dropna().tolist()

# Step 3: Calculate and print Coleman-Liau readability scores
for text in texts:
    if len(text.split()) < 10:
        print(f"Skipping text (too short): {text[:50]}...")
        continue  # Skip texts that are too short

    # Calculate statistics needed for Coleman-Liau
    num_letters = sum(c.isalpha() for c in text)  # Count letters
    num_words = len(text.split())                  # Count words
    num_sentences = text.count('.') + text.count('!') + text.count('?')  # Count sentences

    # Create a stats object (you may need to adjust this based on your implementation)
    class Stats:
        num_letters = num_letters
        num_words = num_words
        num_sentences = num_sentences

    stats = Stats()

    # Calculate Coleman-Liau readability score
    try:
        coleman_liau = ColemanLiau(stats)
        result = coleman_liau.score()
        
        print(f"Text: {text[:50]}...")  # Print first 50 characters for context
        print(f"Coleman-Liau Score: {result.score}")
        print(f"Coleman-Liau Grade Level: {result.grade_level}")
        print("-" * 40)
        
    except ReadabilityException as e:
        print(f"Error calculating readability: {e}")