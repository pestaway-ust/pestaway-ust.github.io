from jiwer import wer, cer, compute_measures
import os

# --- EXAMPLE INPUTS ---
# Ground truth text (your original input to the chatbot or expected transcription)
reference_texts = [
    "How do I control rice stem borers?",
    "Do ducks help to manage rice pests?",
    "Bakit mahalaga ang field sanitation sa pest management",
    "Ano ang pangunahing peste ng manga"
]

# Hypothesis text (STT result or round-trip STT from TTS audio)
predicted_texts = [
    "How do I control rice stem borers?",
    "Do ducks help to manage rice pests?",
    "Bakit mahalaga ang field sanitation sa pest management",
    "Ano ang pangunahing peste ng manga"
]

# --- COMPUTE METRICS ---
for i, (ref, hyp) in enumerate(zip(reference_texts, predicted_texts)):
    print(f"\nSample {i+1}")
    print("Reference :", ref)
    print("Hypothesis:", hyp)
    
    # Word Error Rate
    wer_score = wer(ref, hyp)
    print("WER       :", f"{wer_score:.2%}")
    
    # Character Error Rate
    cer_score = cer(ref, hyp)
    print("CER       :", f"{cer_score:.2%}")
    
    # Detailed Breakdown
    measures = compute_measures(ref, hyp)
    
    # Extracting WIL and WIP from the measures dictionary
    wil_score = measures['wil']
    wip_score = measures['wip']
    
    print("WIL       :", f"{wil_score:.2%}")
    print("WIP       :", f"{wip_score:.2%}")
    
    # Additional metrics
    print("Matches       :", measures['hits'])
    print("Insertions    :", measures['insertions'])
    print("Deletions     :", measures['deletions'])
    print("Substitutions :", measures['substitutions'])
    
