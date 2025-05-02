import json
import pandas as pd
import os

class MedicalKnowledgeBase:

    def __init__(self, kb_json_file=None):
        self.df = pd.DataFrame({
            "diagnosis" : [],
            "finding" : [],
            "evoking_strength" : [], 
            "frequency" : []
        })
        self.diagnosis_list = []

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

    
    def get_diagnoses_for_findings(self, findings):
        df = self.df
        valid_diagnoses = []
        for diagnosis in self.diagnosis_list:
            valid = True
            for finding in findings:
                if finding not in df.where(df["diagnosis"] == diagnosis)['finding'].tolist():
                    valid = False
                    break
            if valid:
                valid_diagnoses.append(diagnosis)
        
        return valid_diagnoses

    
    def suggest_next_finding(self, current_findings):
        # very simple strategy: find common findings not yet observed
        candidate_scores = {}
        valid_diagnoses = self.get_diagnoses_for_findings(current_findings)
        for _, row in self.df.iterrows():
            if row['diagnosis'] in valid_diagnoses and row['finding'] not in current_findings:
                score = row["evoking_strength"] * row["frequency"]
                candidate_scores[row['finding']] = candidate_scores.get(row['finding'], 0) + score
        # return the best finding
        if not candidate_scores:
            return None
        return max(candidate_scores, key=candidate_scores.get)
    
    def save_kb_as_csv(self, filename="medical_kb.csv"):
        self.df.to_csv(filename, index=False)


    def load_kb(self, filename="medical_kb.csv"):
        self.df = pd.read_csv(filename)

