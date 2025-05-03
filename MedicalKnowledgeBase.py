import json
import pandas as pd
import os
import random

class MedicalKnowledgeBase:

    def __init__(self, kb_json_file=None):
        self.df = pd.DataFrame({
            "diagnosis" : [],
            "finding" : [],
            "evoking_strength" : [], 
            "frequency" : []
        })
        self.diagnosis_list = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if kb_json_file:
            with open(kb_json_file) as f: 
                data = json.load(f)
            for diagnosis in data:
                for finding in data[diagnosis]:
                    self.add_entry(diagnosis, finding, 1, data[diagnosis][finding])

    def get_kb(self):
        print(self.df.head())
    
    def add_entry(self, diagnosis, finding, evoking_strength, frequency):
        self.df.loc[len(self.df)] = [diagnosis, finding, evoking_strength, frequency]
        self.diagnosis_list = self.df['diagnosis'].unique()


    
    def get_diagnoses_for_findings(self, findings, neg_findings=[], *, match_req=0):
        
        #if no findings need to be excluded and diagnosis is not required to match findings, no need to loop
        if len(neg_findings) == 0 and match_req == 0:
            return self.diagnosis_list
        
        df = self.df
        invalid_diagnoses = df[df["finding"].isin(neg_findings)]['diagnosis'].tolist()

        if match_req == 0:
            possible_diagnoses = self.diagnosis_list
        else:
            match_df = df[df["finding"].isin(findings)]['diagnosis']
            counts = match_df.groupby("Employee_Name").size()
            possible_diagnoses = counts[counts >= match_req].index.to_list() 
              
        return set(possible_diagnoses).difference(invalid_diagnoses)
    
    def suggest_next_finding(self, current_findings, neg_findings=[], *, match_req=0):
        valid_diagnoses = self.get_diagnoses_for_findings(current_findings, neg_findings, match_req=match_req)
        df = self.df[self.df['diagnosis'].isin(valid_diagnoses)]


        # find common findings not yet observed
        candidate_scores = {}
        for _, row in df.iterrows():
            if (row['finding'] not in current_findings and row['finding'] not in neg_findings):
                score = row["evoking_strength"] * row["frequency"]
                candidate_scores[row['finding']] = candidate_scores.get(row['finding'], 0) + score

        # return the best finding
        if not candidate_scores:
            return None
        return max(candidate_scores, key=candidate_scores.get)
    
    def save_kb_as_csv(self, filename="outputs/medical_kb.csv"):
        filename = os.path.join(self.script_dir, filename)
        self.df.to_csv(filename, index=False)


    def load_kb(self, filename="outputs/medical_kb.csv"):
        filename = os.path.join(self.script_dir, filename)
        self.df = pd.read_csv(filename)
        self.diagnosis_list = self.df['diagnosis'].unique()

    def get_random_finding(self, *, seed=None):
        return self.df.sample(n=1, random_state=seed)['finding'].values[0]
    
    def get_random_findings(self, num_findings):
        return random.sample(sorted(self.df['finding'].unique()), num_findings)
    
    # def get_findings_from_random_diagnosis(self):
    #     diag = random.sample(sorted(self.diagnosis_list), 1)
    #     return self.df[self.df["diagnosis"] == diag]

    def get_random_finding_list(self, num_findings=10, *, random_state=None):
        curr_finding = self.get_random_finding(random_state=random_state)
        num_findings += -1

        finding_list = [curr_finding]
        for _ in range(num_findings):
            curr_finding = self.suggest_next_finding(finding_list)
            if not curr_finding:
                break
            finding_list.append(curr_finding)
        
        return finding_list



# def simulate_conversation(kb, case_findings, max_turns=10):
#     conversation = []
#     current_findings = []
#     neg_findings = []
#     next_finding = kb.get_random_finding()

#     for _ in range(max_turns):  
#         # Ask the question
#         question = generate_question(next_finding)
        
#         # Simulate patient response
#         answer = "Yes" if next_finding in case_findings else "No"

#         # Save conversation turn
#         conversation.append({
#             "doctor_q": question,
#             "patient_a": answer,
#             "finding_queried": next_finding,
#             "response_positive": (answer == "Yes")
#         })

#         print({
#             "doctor_q": question,
#             "patient_a": answer,
#             "finding_queried": next_finding,
#             "response_positive": (answer == "Yes")
#         })

#         # Update what findings have been asked
#         if answer == "Yes":
#             current_findings.append(next_finding)
#         else:
#             neg_findings.append(next_finding)

#         # Suggest next finding
#         next_finding = kb.suggest_next_finding(current_findings, neg_findings)


#         if not next_finding:
#             # print("No more findings to ask about.")
#             break

#     return conversation

# def generate_question(finding):
#     # In MEDCOD, this part is NLG model + control codes (empathy etc.)
#     # Here: a simple template
#     return f"Do you have {finding}?"


# script_dir = os.path.dirname(os.path.abspath(__file__))
# filename = os.path.join(script_dir, "outputs\mimic_4_kb_w_freq.json")
# # kb = MedicalKnowledgeBase(filename)

# # kb.save_kb_as_csv()

# kb = MedicalKnowledgeBase()
# kb.load_kb()

# # print(kb.get_kb())

# # print(kb.get_findings_from_random_diagnosis())

# simulate_conversation(kb, kb.get_random_findings(10))