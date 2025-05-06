import json
import random
from MedicalKnowledgeBase import MedicalKnowledgeBase

kb = MedicalKnowledgeBase('output/mimic_4_kb_w_freq.json')

with open("revised_input/symptom_questions.json") as f:
    questions = json.load(f)

with open("revised_input/emote_rules.json") as f:
    emote = json.load(f)


def chatbot_loop():
    print("Chatbot: Hello, I'm going to ask you some yes or no questions about your symptoms.")
    current_findings = []
    neg_findings = []
    next_finding = kb.get_random_finding()
    prev_ans = None
    while len(current_findings) + len(neg_findings) < 10:

        question = generate_question(next_finding)
        if not question:
            next_finding = kb.get_random_finding()
            continue

        if prev_ans == "y":
            r = random.random()
            if prev_ans == "y" and r > .6:
                question = random.choice(emote["affirmative"]) + " " + question
            elif .6 >= r > .45 :
                question = random.choice(emote["empathetic"]) + " " + question
            elif .45 >= r > .3 :
                question = random.choice(emote["apologetic"]) + " " + question.lower()

        print(f"Chatbot: {question}")
        user_input = input("You: ")
        if any(word in user_input.lower() for word in ["yes", "yeah", "y", "i have", "sure"]):
            prev_ans = "y"
            current_findings.append(next_finding)
        else:
            prev_ans = "n"
            neg_findings.append(next_finding)
        
        # Suggest next finding
        next_finding = kb.suggest_next_finding(current_findings, neg_findings)

    print("Chatbot: Thank you for your time.")
    

def generate_question(finding):
    try: 
        return random.choice(questions[finding])
    except: 
        return None
    

chatbot_loop()
