# Due to its size, the mimic_subset_cleaned.csv file has been compressed into mimic_subset_cleaned.zip 
# in the \outputs folder - it needs to be unzipped before using this script. 

import pandas as pd
import re
import json
from collections import defaultdict

mimic_df = pd.read_csv("output/mimiciv_subset_cleaned.csv")
kb_output_json = "output/mimic_4_kb_w_freq.json"
with open("revised_input/mayoclinic_symptom_list.txt") as f:
    symptom_list = [line.strip().lower() for line in f if line.strip()]
symptom_pattern = re.compile(r'\b(' + '|'.join(re.escape(sym) for sym in symptom_list) + r')\b', re.IGNORECASE)

# Detect findings in the mimic4 notes
def extract_findings(text):
    return list(set(symptom_pattern.findall(text)))

mimic_df["findings"] = mimic_df["text"].apply(extract_findings)

# create and normalize kb dictionary
kb = defaultdict(lambda: defaultdict(int))

for _, row in mimic_df.iterrows():
    disease = row["long_title"]
    findings = row["findings"]
    
    for finding in list(findings):
        kb[disease][finding] += 1

normalized_kb = {}
for diagnosis, findings in kb.items():
    total = sum(findings.values())
    normalized_kb[diagnosis] = {
        symptom: count / total
        for symptom, count in findings.items()
    }

# output to json and csv
# === SAVE AS JSON ===
with open(kb_output_json, "w") as f:
    json.dump(normalized_kb, f, indent=2)

# === SAVE AS CSV (flattened) ===
kb_output_csv = "output/mimic_4_kb_w_freq.csv"
flattened = []
for disease, findings in normalized_kb.items():
    for symptom, freq in findings.items():
        flattened.append({"diagnosis": disease, "symptom": symptom, "frequency": freq})

df_kb = pd.DataFrame(flattened)
df_kb.to_csv(kb_output_csv, index=False)

print(f"✅ Knowledge base created with {len(normalized_kb)} diagnoses.")