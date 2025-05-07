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


    def get_random_finding(self, current_findings=[], neg_findings=[]):
        finding = self.df.sample(n=1)['finding'].values[0]
        while finding in current_findings or finding in neg_findings:
            finding = self.df.sample(n=1)['finding'].values[0]
        return finding
    
    def get_random_findings(self, num_findings):
        return random.sample(sorted(self.df['finding'].unique()), num_findings)
    

    def save_kb_as_csv(self, filename="outputs/medical_kb.csv"):
        filename = os.path.join(self.script_dir, filename)
        self.df.to_csv(filename, index=False)

    def load_kb(self, filename="outputs/medical_kb.csv"):
        filename = os.path.join(self.script_dir, filename)
        self.df = pd.read_csv(filename)
        self.diagnosis_list = self.df['diagnosis'].unique()

