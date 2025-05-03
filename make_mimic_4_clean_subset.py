'''
NOTICE - requires mimic IV files (along with clinical notes) to be downloaded locally
'''


import pandas as pd

# Load hospital diagnoses
diagnoses = pd.read_csv("mimic-4-diagnoses/diagnoses_icd.csv")  # columns: subject_id, hadm_id, icd_code, icd_version

# Load ICD descriptions
icd_desc = pd.read_csv("mimic-4-diagnoses/d_icd_diagnoses.csv")  # columns: icd_code, long_title

# Load notes (only discharge summaries)
notes = pd.read_csv("mimic-4-clinical-notes/note/discharge.csv")  # columns: subject_id, hadm_id, note_type, note_text


# Drop missing hadm_id
notes = notes.dropna(subset=["hadm_id", "text"])

# Merge notes with diagnoses
merged = pd.merge(notes, diagnoses, on=["subject_id", "hadm_id"], how="inner")

# Merge with ICD descriptions
merged = pd.merge(merged, icd_desc, on="icd_code", how="left")

# Keep only necessary columns
merged = merged[["subject_id", "hadm_id", "icd_code", "long_title", "text"]]

# Make subset
merged_subset = merged.sample(n=1000, random_state=42).reset_index(drop=True)

import re

def clean_note_text(text):
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

merged_subset["text"] = merged_subset["text"].apply(clean_note_text)

output_filename = "mimiciv_subset_cleaned.csv"

# Export to CSV
merged_subset.to_csv(output_filename, index=False)

print(f"✅ Subset exported to {output_filename} with {len(merged_subset)} rows.")