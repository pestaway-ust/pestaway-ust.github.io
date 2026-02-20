import json
from langdetect import detect, LangDetectException

def count_languages_in_dataset(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        english_count = 0
        tagalog_count = 0
        unknown_count = 0
        
        for entry in data:
            # Ensure entry is a dictionary and handle it accordingly
            if isinstance(entry, dict):
                prompt = entry.get("prompt", "")
                chosen = entry.get("chosen", "")
                rejected = entry.get("rejected", "")
                
                # Combine text from prompt, chosen, and rejected fields
                text = prompt + " " + chosen + " " + rejected

                try:
                    # Detect language of combined text
                    lang = detect(text)
                    
                    if lang == 'en':
                        english_count += 1
                    elif lang == 'tl':  # 'tl' is the ISO code for Tagalog
                        tagalog_count += 1
                    else:
                        unknown_count += 1
                except LangDetectException:
                    # In case the language detection fails
                    unknown_count += 1

        return english_count, tagalog_count, unknown_count
    else:
        print("The data is not in the expected format (list of dictionaries).")
        return None, None, None

# Example usage:
json_file = r"D:\Downloads\handbook.json"
english_count, tagalog_count, unknown_count = count_languages_in_dataset(json_file)
print(f"English entries: {english_count}")
print(f"Tagalog entries: {tagalog_count}")
print(f"Unknown language entries: {unknown_count}")
