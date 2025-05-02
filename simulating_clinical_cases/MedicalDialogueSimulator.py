class MedicalDialogueSimulator:
    '''
    Input: Medical knowledge base with entries in format (diagnoses, symptom, evoking_strength, frequency)
        Example Entry: ("Flu", "fever", evoking_strength=0.9, frequency=0.8)
    '''
    def __init__(self, kb: MedicalKnowledgeBase):
        self.kb = kb
    
    def simulate_conversation(self, patient_findings, max_turns=10):
        conversation = []
        current_findings = []

        for turn in range(max_turns):
            # Suggest next finding
            next_finding = self.kb.suggest_next_finding(current_findings)
            if not next_finding:
                print("No more findings to ask about.")
                break
            
            # Ask the question
            question = self.generate_question(next_finding)
            
            # Simulate patient response
            answer = "Yes" if next_finding in patient_findings else "No"

            # Save conversation turn
            conversation.append({
                "system_question": question,
                "patient_answer": answer,
                "finding_queried": next_finding,
                "response_positive": (answer == "Yes")
            })

            # Update what findings have been asked
            if answer == "Yes":
                current_findings.append(next_finding)
        
        return conversation

    def generate_question(self, finding):
        # In MEDCOD, this part is NLG model + control codes (empathy etc.)
        # Here: a simple template
        return f"Do you have {finding}?"