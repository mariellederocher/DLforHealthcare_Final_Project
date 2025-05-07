# requires mimic IV files (along with clinical notes) to be downloaded locally

import pandas as pd
import re

# filter for subset of icd-10 codes
ranges = [
    ('A00', 'A90'), ('B00', 'B99'), ('D50', 'D89'), ('E00', 'E89'),
    ('F01', 'F99'), ('G00', 'G99'), ('H00', 'H59'), ('H60', 'H95'),
    ('I00', 'I99'), ('J00', 'J99'), ('K00', 'K95'), ('L00', 'L99'), 
    ('M00', 'M99'), ('N00', 'N99')
]

# use broader labels
labels = [
    (("A00", "A09"), "Intestinal infectious diseases"),
    (("A15", "A19"), "Tuberculosis"),
    (("A20", "A28"), "Certain zoonotic bacterial diseases"),
    (("A30", "A49"), "Other bacterial diseases"),
    (("A50", "A64"), "Infections with a predominantly sexual mode of transmission"),
    (("A65", "A69"), "Other spirochetal diseases"),
    (("A70", "A74"), "Other diseases caused by chlamydiae"),
    (("A75", "A79"), "Rickettsioses"),
    (("A80", "A89"), "Viral and prion infections of the central nervous system"),
    (("A90", "A99"), "Arthropod-borne viral fevers and viral hemorrhagic fevers"),
    (("B00", "B09"), "Viral infections characterized by skin and mucous membrane lesions"),
    (("B10", "B10"), "Other human herpesviruses"),
    (("B15", "B19"), "Viral hepatitis"),
    (("B20", "B20"), "Human immunodeficiency virus [HIV] disease"),
    (("B25", "B34"), "Other viral diseases"),
    (("B35", "B49"), "Mycoses"),
    (("B50", "B64"), "Protozoal diseases"),
    (("B65", "B83"), "Helminthiases"),
    (("B85", "B89"), "Pediculosis, acariasis and other infestations"),
    (("B90", "B94"), "Sequelae of infectious and parasitic diseases"),
    (("B95", "B97"), "Bacterial and viral infectious agents"),
    (("B99", "B99"), "Other infectious diseases"),
    (("D50", "D53"), "Nutritional anemias"),
    (("D55", "D59"), "Hemolytic anemias"),
    (("D60", "D64"), "Aplastic and other anemias and other bone marrow failure syndromes"),
    (("D65", "D69"), "Coagulation defects, purpura and other hemorrhagic conditions"),
    (("D70", "D77"), "Other disorders of blood and blood-forming organs"),
    (("D78", "D78"), "Intraoperative and postprocedural complications of the spleen"),
    (("D80", "D89"), "Certain disorders involving the immune mechanism"),
    (("E00", "E07"), "Disorders of thyroid gland"),
    (("E08", "E13"), "Diabetes mellitus"),
    (("E15", "E16"), "Other disorders of glucose regulation and pancreatic internal secretion"),
    (("E20", "E35"), "Disorders of other endocrine glands"),
    (("E36", "E36"), "Intraoperative complications of endocrine system"),
    (("E40", "E46"), "Malnutrition"),
    (("E50", "E64"), "Other nutritional deficiencies"),
    (("E65", "E68"), "Overweight, obesity and other hyperalimentation"),
    (("E70", "E88"), "Metabolic disorders"),
    (("E89", "E89"), "Postprocedural endocrine and metabolic complications and disorders, not elsewhere classified"),
    (("F01", "F09"), "Mental disorders due to known physiological conditions"),
    (("F10", "F19"), "Mental and behavioral disorders due to psychoactive substance use"),
    (("F20", "F29"), "Schizophrenia, schizotypal, delusional, and other non-mood psychotic disorders"),
    (("F30", "F39"), "Mood [affective] disorders"),
    (("F40", "F48"), "Anxiety, dissociative, stress-related, somatoform and other nonpsychotic mental disorders"),
    (("F50", "F59"), "Behavioral syndromes associated with physiological disturbances and physical factors"),
    (("F60", "F69"), "Disorders of adult personality and behavior"),
    (("F70", "F79"), "Intellectual disabilities"),
    (("F80", "F89"), "Pervasive and specific developmental disorders"),
    (("F90", "F98"), "Behavioral and emotional disorders with onset usually occurring in childhood and adolescence"),
    (("F99", "F99"), "Unspecified mental disorder"),
    (("G00", "G09"), "Inflammatory diseases of the central nervous system"),
    (("G10", "G14"), "Systemic atrophies primarily affecting the central nervous system"),
    (("G20", "G26"), "Extrapyramidal and movement disorders"),
    (("G30", "G32"), "Other degenerative diseases of the nervous system"),
    (("G35", "G37"), "Demyelinating diseases of the central nervous system"),
    (("G40", "G47"), "Episodic and paroxysmal disorders"),
    (("G50", "G59"), "Nerve, nerve root and plexus disorders"),
    (("G60", "G65"), "Polyneuropathies and other disorders of the peripheral nervous system"),
    (("G70", "G73"), "Diseases of myoneural junction and muscle"),
    (("G80", "G83"), "Cerebral palsy and other paralytic syndromes"),
    (("G89", "G99"), "Other disorders of the nervous system"),
    (("H00", "H05"), "Disorders of eyelid, lacrimal system and orbit"),
    (("H10", "H11"), "Disorders of conjunctiva"),
    (("H15", "H22"), "Disorders of sclera, cornea, iris and ciliary body"),
    (("H25", "H28"), "Disorders of lens"),
    (("H30", "H36"), "Disorders of choroid and retina"),
    (("H40", "H42"), "Glaucoma"),
    (("H43", "H44"), "Disorders of vitreous body and globe"),
    (("H46", "H47"), "Disorders of optic nerve and visual pathways"),
    (("H49", "H52"), "Disorders of ocular muscles, binocular movement, accommodation and refraction"),
    (("H53", "H54"), "Visual disturbances and blindness"),
    (("H55", "H57"), "Other disorders of eye and adnexa"),
    (("H59", "H59"), "Intraoperative and postprocedural complications and disorders of eye and adnexa, not elsewhere classified"),
    (("I00", "I02"), "Acute rheumatic fever"),
    (("I05", "I09"), "Chronic rheumatic heart diseases"),
    (("I10", "I16"), "Hypertensive diseases"),
    (("I20", "I25"), "Ischemic heart diseases"),
    (("I26", "I28"), "Pulmonary heart disease and diseases of pulmonary circulation"),
    (("I30", "I5A"), "Other forms of heart disease"),
    (("I60", "I69"), "Cerebrovascular diseases"),
    (("I70", "I79"), "Diseases of arteries, arterioles and capillaries"),
    (("I80", "I89"), "Diseases of veins, lymphatic vessels and lymph nodes, not elsewhere classified"),
    (("I95", "I99"), "Other and unspecified disorders of the circulatory system"),
    (("J00", "J06"), "Acute upper respiratory infections"),
    (("J09", "J18"), "Influenza and pneumonia"),
    (("J20", "J22"), "Other acute lower respiratory infections"),
    (("J30", "J39"), "Other diseases of upper respiratory tract"),
    (("J40", "J47"), "Chronic lower respiratory diseases"),
    (("J60", "J70"), "Lung diseases due to external agents"),
    (("J80", "J84"), "Other respiratory diseases principally affecting the interstitium"),
    (("J85", "J86"), "Suppurative and necrotic conditions of the lower respiratory tract"),
    (("J90", "J94"), "Other diseases of the pleura"),
    (("J95", "J95"), "Intraoperative and postprocedural complications and disorders of respiratory system, not elsewhere classified"),
    (("J96", "J99"), "Other diseases of the respiratory system"),
    (("K00", "K14"), "Diseases of oral cavity and salivary glands"),
    (("K20", "K31"), "Diseases of esophagus, stomach and duodenum"),
    (("K35", "K38"), "Diseases of appendix"),
    (("K40", "K46"), "Hernia"),
    (("K50", "K52"), "Noninfective enteritis and colitis"),
    (("K55", "K64"), "Other diseases of intestines"),
    (("K65", "K68"), "Diseases of peritoneum and retroperitoneum"),
    (("K70", "K77"), "Diseases of liver"),
    (("K80", "K87"), "Disorders of gallbladder, biliary tract and pancreas"),
    (("K90", "K95"), "Other diseases of the digestive system"),
    (("L00", "L08"), "Infections of the skin and subcutaneous tissue"),
    (("L10", "L14"), "Bullous disorders"),
    (("L20", "L30"), "Dermatitis and eczema"),
    (("L40", "L45"), "Papulosquamous disorders"),
    (("L49", "L54"), "Urticaria and erythema"),
    (("L55", "L59"), "Radiation-related disorders of the skin and subcutaneous tissue"),
    (("L60", "L75"), "Disorders of skin appendages"),
    (("L76", "L76"), "Intraoperative and postprocedural complications of skin and subcutaneous tissue"),
    (("L80", "L99"), "Other disorders of the skin and subcutaneous tissue"),
    (("M00", "M02"), "Infectious arthropathies"),
    (("M04", "M04"), "Autoinflammatory syndromes"),
    (("M05", "M14"), "Inflammatory polyarthropathies"),
    (("M15", "M19"), "Osteoarthritis"),
    (("M20", "M25"), "Other joint disorders"),
    (("M26", "M27"), "Dentofacial anomalies [including malocclusion] and other disorders of jaw"),
    (("M30", "M36"), "Systemic connective tissue disorders"),
    (("M40", "M43"), "Deforming dorsopathies"),
    (("M45", "M49"), "Spondylopathies"),
    (("M50", "M54"), "Other dorsopathies"),
    (("M60", "M63"), "Disorders of muscles"),
    (("M65", "M67"), "Disorders of synovium and tendon"),
    (("M70", "M79"), "Other soft tissue disorders"),
    (("M80", "M85"), "Disorders of bone density and structure"),
    (("M86", "M90"), "Other osteopathies"),
    (("M91", "M94"), "Chondropathies"),
    (("M95", "M95"), "Other disorders of the musculoskeletal system and connective tissue"),
    (("M96", "M96"), "Intraoperative and postprocedural complications and disorders of musculoskeletal system, not elsewhere classified"),
    (("M97", "M97"), "Periprosthetic fracture around internal prosthetic joint"),
    (("M99", "M99"), "Biomechanical lesions, not elsewhere classified"),
    (("N00", "N08"), "Glomerular diseases"),
    (("N10", "N16"), "Renal tubulo-interstitial diseases"),
    (("N17", "N19"), "Acute kidney failure and chronic kidney disease"),
    (("N20", "N23"), "Urolithiasis"),
    (("N25", "N29"), "Other disorders of kidney and ureter"),
    (("N30", "N39"), "Other diseases of the urinary system"),
    (("N40", "N53"), "Diseases of male genital organs"),
    (("N60", "N65"), "Disorders of breast"),
    (("N70", "N77"), "Inflammatory diseases of female pelvic organs"),
    (("N80", "N98"), "Noninflammatory disorders of female genital tract"),
    (("N99", "N99"), "Intraoperative and postprocedural complications and disorders of genitourinary system, not elsewhere classified"),

]

# Load hospital diagnoses
diagnoses = pd.read_csv("mimic-4-diagnoses/diagnoses_icd.csv")  # columns: subject_id, hadm_id, icd_code, icd_version
# Load ICD descriptions
icd_desc = pd.read_csv("mimic-4-diagnoses/d_icd_diagnoses.csv")  # columns: icd_code, long_title
# Load notes (only discharge summaries)
notes = pd.read_csv("mimic-4-clinical-notes/note/discharge.csv")  # columns: subject_id, hadm_id, note_type, note_text

# Drop missing hadm_id
notes = notes.dropna(subset=["hadm_id", "text"])
# Merge notes with diagnoses
merged = pd.merge(notes, diagnoses, on=["subject_id", "hadm_id"], how="inner")
# Merge with ICD descriptions
merged = pd.merge(merged, icd_desc, on="icd_code", how="left")
# Keep only necessary columns
merged = merged[["icd_code", "long_title", "text"]]

# filter for codes
def code_in_ranges(code):
    match = re.match(r'^([A-Z])(\d{2})', code)
    if not match:
        return False
    letter, number = match.groups()
    num = int(number)
    for start, end in ranges:
        if start[0] == end[0] == letter:
            if int(start[1:]) <= num <= int(end[1:]):
                return True
    return False

merged = merged[merged["icd_code"].apply(code_in_ranges)]

# change name to broader labels
def label_ranges(code):
    match = re.match(r'^([A-Z])(\d{2})', code)
    if not match:
        return "Unknown"
    letter, number = match.groups()
    num = int(number)
    for r, name in labels:
        start, end = r
        if start[0] == end[0] == letter:
            try:
                if int(start[1:]) <= num <= int(end[1:]):
                    return name
            except: 
                pass
    return "Unknown"

merged["long_title"] = merged["icd_code"].apply(label_ranges)

# Make subset
merged_subset = merged.sample(n=100000).reset_index(drop=True)

# clean data
def clean_note_text(text):
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

merged_subset["text"] = merged_subset["text"].apply(clean_note_text)


# Export to CSV
output_filename = "mimiciv_subset_cleaned.csv"
merged_subset.to_csv(output_filename, index=False)

print(f"✅ Subset exported to {output_filename} with {len(merged_subset)} rows.")