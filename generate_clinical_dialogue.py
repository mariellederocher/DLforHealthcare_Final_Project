import json 
import random
import pandas as pd
from MedicalKnowledgeBase import MedicalKnowledgeBase

kb = MedicalKnowledgeBase('output/mimic_4_kb_w_freq.json')
with open("revised_input/symptom_questions.json") as f:
    questions = json.load(f)
with open("revised_input/emote_rules.json") as f:
    emote_phrases = json.load(f)
output_file = "output/generated_cases.csv"

df = pd.DataFrame({
    "encounter_id": [],
    "doctor_q": [],
    "emote": [],
    "finding": [],
    "patient_a": [],
    "affirmative": [],
    "prev_doctor_q": [],
    "prev_patient_a": [],
    "prev_finding": [],
    "prev_affirmative": []

})

# simulate cases (just a list of symptoms)
encounter_id = 0
cases_to_generate = 1000
cases = []

for i in range(cases_to_generate):
    cases.append({
        "encounter_id" : encounter_id,
        "findings" : kb.get_random_findings(10)
    })
    encounter_id += 1


def generate_question(finding):
    try: 
        return random.choice(questions[finding])
    except: 
        return None

# create question answer turns 
max_turns=10

for case in cases:
    entry = {"encounter_id": case["encounter_id"]}

    current_findings = []
    neg_findings = []
    next_finding = kb.get_random_finding(current_findings, neg_findings)

    prev_doctor_q = "none"
    prev_patient_a = "none"
    prev_finding = "none"
    prev_affirmative = "none"

    while len(current_findings) + len(neg_findings) < max_turns:
        # generate question
        question = generate_question(next_finding)
        if not question:
            next_finding = kb.get_random_finding(current_findings, neg_findings)
            continue

        emote = "Neutral"
        if prev_patient_a == "Yes.":
            r = random.random()
            if r > .6:
                question = random.choice(emote_phrases["affirmative"]) + " " + question
                emote = "Affirmative"  
            elif .6 >= r > .45 :
                question = random.choice(emote_phrases["empathetic"]) + " " + question
                emote = "Empathetic"  
            elif .45 >= r > .3 :
                question = random.choice(emote_phrases["apologetic"]) + " " + question.lower()
                emote = "Apologetic"  


        #update info from previous turn
        entry["prev_doctor_q"] = prev_doctor_q
        entry["prev_patient_a"]	= prev_patient_a
        entry["prev_finding"] = prev_finding
        entry["prev_affirmative"] = prev_affirmative

        prev_doctor_q = entry["doctor_q"] = question
        prev_finding = entry["finding"] = next_finding
        entry["emote"] = emote  

        if next_finding in case["findings"]:
            prev_patient_a = entry["patient_a"]	= "Yes."
            prev_affirmative = entry["affirmative"] = "True"
            current_findings.append(next_finding)
        else:
            prev_patient_a = entry["patient_a"]	= "No."
            prev_affirmative = entry["affirmative"] = "False"
            neg_findings.append(next_finding)

        df.loc[len(df)] = entry
        
        next_finding = kb.suggest_next_finding(current_findings, neg_findings)

df.to_csv(output_file, index=False)



    
    