import pandas as pd
import re
from collections import defaultdict
from fuzzywuzzy import fuzz

# Load MTS-Dialog
df = pd.read_csv("MTS-Dialog-TrainingSet.csv") 
print(df.columns)

# Load rules
emote_df = pd.read_json("emote_rules.json")

# Initialize phrase buckets
emote_phrases = defaultdict(list)

# Rule-based emotion annotation (simplified version from MEDCOD)
def classify_emotion(text):
    # Load rules
    emote_df = pd.read_json("emote_rules.json")

    text = text.lower()
    if any(x in text for x in emote_df[0]["phrase"]):
        return "apology"
    elif any(x in text for x in emote_df[1]["phrase"]):
        return "empathy"
    elif any(x in text for x in emote_df[2]["phrase"]):
        return "affirmative"
    return "none"

# Heuristic: find prefix statements before questions
def extract_emote_phrase(text):
    # Split on question punctuation or transition
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(parts) > 1:
        # Return first sentence if it looks like a preface
        if len(parts[0].split()) <= 12:
            return parts[0]
    return None

# Process each dialogue
for _, row in df.iterrows():
    if "dialogue" not in row or not isinstance(row['dialogue'], str):
        continue
    dialogue = row['dialogue']
    turns = re.findall(r"(Doctor|Patient): ([^:]+?)(?=(?:Doctor|Patient):|$)", dialogue)

    for i, (speaker, text) in enumerate(turns):
        if speaker != "Doctor":
            continue
        emote = classify_emotion(text)
        phrase = extract_emote_phrase(text)
        if phrase:
            emote_phrases[emote].append(phrase.strip())

# Deduplicate with fuzzy match
def deduplicate_phrases(phrases, threshold=90):
    unique = []
    for p in phrases:
        if not any(fuzz.ratio(p, u) > threshold for u in unique):
            unique.append(p)
    return unique

# Deduplicated phrases per emote class
deduped_emote_phrases = {
    k: deduplicate_phrases(v) for k, v in emote_phrases.items()
}

import csv

# Save deduplicated emote phrases to a CSV
with open("emote_phrases.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["emote_class", "phrase"])  # header

    for emote, phrases in deduped_emote_phrases.items():
        for phrase in phrases:
            writer.writerow([emote, phrase])
            if emote != "none":
                print(emote, phrase)