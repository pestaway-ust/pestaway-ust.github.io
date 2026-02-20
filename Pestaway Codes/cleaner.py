import json

# Load the dataset
with open(r"D:\Downloads\additional_rice_sugarc.json", encoding='utf-8') as file:
    data = json.load(file)

# Function to clean and format text, and fix encoding errors
def clean_text(text):
    text = text.strip()  # Remove leading/trailing spaces
    text = text.replace("â€™", "'")  # Replace corrupted apostrophes
    text = text.replace("â€", '"').replace("â€œ", '"')  # Fix corrupted quotes
    text = '. '.join([sentence.strip().capitalize() for sentence in text.split('.')])  # Capitalize sentences
    return text

# Clean up the dataset
for entry in data:
    entry["prompt"] = clean_text(entry["prompt"])
    entry["chosen"] = clean_text(entry["chosen"])
    entry["rejected"] = clean_text(entry["rejected"])

# Save the cleaned dataset
with open(r"D:\Downloads\additional_rice_sugarc.json", 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Dataset has been cleaned and saved to 'cleaned_train.json'.")
