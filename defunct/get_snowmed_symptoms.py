import requests
import json
import os


# === CONFIGURATION ===
API_KEY = "d95c2fe3-9b8c-4425-a9b0-3fe7b389f57d"  # Replace with your actual key
ONTOLOGY = "SNOMEDCT"  # You can also use 'UMLS' or 'HPO'
SYMP_CATEGORY = "finding"  # Also consider "symptom", "clinical finding"
MAX_RESULTS = 600  # adjust as needed

# === GET SCRIPT DIRECTORY ===
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "snomed_symptom_list.txt")

# === FUNCTION TO QUERY BIOPORTAL SEARCH ===
def get_symptom_terms(api_key, ontology, query, max_results=100):
    url = "https://data.bioontology.org/search"
    params = {
        "q": query,
        "ontologies": ontology,
        "apikey": api_key,
        "require_exact_match": "false",
        "pagesize": max_results
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")
    
    results = response.json()["collection"]
    terms = []
    for result in results:
        name = result.get("prefLabel")
        if name and name.lower() != query.lower():
            terms.append(name.lower())
    
    return list(set(terms))  # remove duplicates

# === FETCH TERMS ===
keywords = ["symptom", "complaint"]
all_terms = []

for keyword in keywords:
    terms = get_symptom_terms(API_KEY, ONTOLOGY, keyword, max_results=MAX_RESULTS)
    all_terms.extend(terms)

# Deduplicate and sort
symptom_list = sorted(set(all_terms))

# Save to file
with open(output_path, "w") as f:
    for term in symptom_list:
        f.write(term + "\n")

print(f"✅ Saved {len(symptom_list)} symptom terms to: {output_path}")