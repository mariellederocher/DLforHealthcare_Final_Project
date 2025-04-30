import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# === STEP 1: Get symptom page links from A–Z index ===
BASE_URL = "https://www.mayoclinic.org/"
INDEX_URL = "https://www.mayoclinic.org/symptoms/index?letter="

def get_symptom_links():
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    symptom_urls = []

    for letter in ascii_uppercase:

        res = requests.get(INDEX_URL + letter)
        soup = BeautifulSoup(res.text, "html.parser")
        
        links = soup.select("a")
        symptom_urls = symptom_urls + [BASE_URL + link['href'] for link in links if link.has_attr('href') and link['href'].startswith("/symptoms") and "/definition" in link['href']]

    return symptom_urls

def get_symptoms(symptom_urls):
    symptoms = []
    for url in symptom_urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        
        symptoms.append(soup.title.get_text())

    return symptoms

# === STEP 2: Clean and extract unique names ===
def normalize_symptom_name(name):
    name = name.lower().strip()
    name = name.replace("- mayo clinic", "").strip()
    return name

# === STEP 3: Save as TXT and CSV ===
def save_symptoms(symptom_list, output_dir):
    txt_path = os.path.join(output_dir, "mayoclinic_symptom_list.txt")
    
    with open(txt_path, "w") as f:
        for symptom in symptom_list:
            f.write(symptom + "\n")
    
    print(f"✅ Saved {len(symptom_list)} symptoms to:")
    print(f" - {txt_path}")

# === MAIN SCRIPT ===
if __name__ == "__main__":
    # Get current script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🔍 Scraping MayoClinic for symptom names...")
    raw_symptoms = get_symptoms(get_symptom_links())
    names_only = sorted(set(normalize_symptom_name(name) for name in raw_symptoms if not name == "403 forbidden"))
    
    save_symptoms(names_only, script_dir)