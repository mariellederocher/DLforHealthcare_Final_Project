import json

symptom_file = "revised_input/mayoclinic_symptom_list.txt"
with open(symptom_file, "r") as f:
    symptom_list = [line.strip().lower() for line in f if line.strip()]


# with open("revised_input/symptom_pattern_map.json") as f:
#     pattern_map = json.load(f)

# new_pattern_map = {}
# for symptom in symptom_list:
#     if symptom in pattern_map.keys():
#         new_pattern_map[symptom] = pattern_map[symptom]
#     else:
#         new_pattern_map[symptom] = [symptom]

# # print(new_pattern_map)

# with open("revised_input/symptom_pattern_map.json", "w") as f:
#     json.dump(new_pattern_map, f, indent=2)



with open("revised_input/symptom_questions.json") as f:
    symptom_questions = json.load(f)

new_questions = {}
for symptom in symptom_list:
    if symptom in symptom_questions.keys():
        new_questions[symptom] = symptom_questions[symptom]
    else:
        new_questions[symptom] = []

# print(new_pattern_map)

with open("revised_input/symptom_questions.json", "w") as f:
    json.dump(new_questions, f, indent=2)