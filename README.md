# Deep Learning for Healthcare Final Project: Reproducing the MEDCOD System

Authors: Zohreh Mahdavi, Marielle Derocher

This repository contains our reproduction of the MEDCOD dialogue system from the paper MEDCOD: A Medi-cally-Accurate, Emotive, Diverse, and Controllable Dialog System, and the development of an alternative implementation using open-source datasets and models. We reconstructed the key dataset preprocessing pipelines (symptom extraction, emotion and question labeling, and synthetic KB generation), adapted a symptom-selective dialog controller, and fine-tuned a GODEL-based question generator. Due to data access limitations, our focus shifted to scalable labeling heuristics and rule-based baselines. We used the MTS-Dialog, a set of doctor-patient dialogues, as the basis for our dataset. 

We were unable to access the datasets or proprietary modules used in the original paper. As a result, we focused on recreating the system’s structure and training pipeline using alternative resources. Our reproduction includes dataset construction, symptom-finding mapping, emotion tagging, and training a neural language generator. We implemented a simplified symptom selection logic based on co-occurrence statistics from MIMIC-IV notes, and a chatbot trained using the MTS-Dialog dialogue dataset.

Original Paper: https://arxiv.org/pdf/2111.09381 

MEDCOD Code Repository: https://github.com/curai/curai-research/tree/main/MEDCOD

MTS-Dialog Repository: https://github.com/abachaa/MTS-Dialog

## Pretrained Models From HuggingFace

* GODEL: `GODEL-v1_1-base-seq2seq`
* Zeroshot Classifier: `deberta-v3-large-zeroshot-v2.0`

## Contents

### Initial Data

* `MTS-Dialog-TrainingSet.csv` - Downloaded from https://github.com/abachaa/MTS-Dialog/blob/main/Main-Dataset/MTS-Dialog-TrainingSet.csv. Consists of 1,201 pairs of conversations and associated summaries.

### Dataset Construction

We used several notebooks and Python scripts to construct our datasets. For using this code, run the files in the given order. 

* `mayoclinic_symptom_scraper.py` - Extracts a symptom list from MayoClinic.org
* `make_mts_dialog_dataset.ipynb` - Main processing script for creating the training data
* `kaggle_zeroshot_qa_labeling.ipynb` - Uses Zeroshot classifier to label questions with emotions and answer as yes/no
* `make_mimic_4_clean_subset.py` - Creates clean subset of diagnoses and clinical notes from the MIMIC-IV database
* `make_mimic_4_kb.py` - Creates knowledge base with frequencies of symptoms corresponding with diagnoses
* `MedicalKnowledgeBase.py` - Class for using the knowledge base to generate findings and suggest next findings
* `generate_clinical_dialogue.py` - Creates simulated conversations to augment the data from MTS-Dialog

### Chatbots

* `kaggle_train_godel_and_chatbot.ipynb` - Notebook that fine-tunes a GODEL model and uses it in a chatbot that generates doctor questions. 
* `chatbot_no_generator.py` - Chatbot that uses procedural question generation

### Data Files

Files in the `output/` folder are produced directly from our scripts without any editing. Files in the `revised_input/` folder are either files from `output/` that we added to and revised, or that we manually wrote. 

# Citations

Ben Abacha, A.; Yim, W.; Fan, Y.; and Lin, T. 2023. An Empirical Study of Clinical Note Generation from Doctor-Patient Encounters. In Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, 2291–2302. Dubrovnik, Croatia: Association for Computational Linguistics.

Compton, R.; Valmianski, I.; Deng, L.; Huang, C.; Katariya, N.; Amatriain, X.; and Kannan, A. 2021. MEDCOD: A Medically-Accurate, Emotive, Diverse, and Controllable Dialog System. In Roy, S.; Pfohl, S.; Rocheteau, E.; Tadesse, G. A.; Oala, L.; Falck, F.; Zhou, Y.; Shen, L.; Zamzmi, G.; Mugambi, P.; Zirikly, A.; McDermott, M. B. A.; and Alsentzer, E., eds., Proceedings of Machine Learning for Health, volume 158 of Proceedings of Machine Learning Research, 110–129. PMLR.

Goldberger, A.; Amaral, L.; Glass, L.; Hausdorff, J.; Ivanov, P.; Mark, R.; Mietus, J.; Moody, G.; Peng, C.; and Stanley, H. 2000. PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals.

Johnson, A.; Bulgarelli, L.; Pollard, T.; Gow, B.; Moody, B.; Horng, S.; and Celi, R., L. A.and Mark. 2024. MIMIC-IV (version 3.1).

Johnson, A. E. W.; Pollard, T. J.; Shen, L.; Lehman, L. H.; Feng, M.; Ghassemi, M.; Moody, B.; Szolovits, P.; Celi, L. A.; and Mark, R. G. 2023. MIMIC-IV, a freely accessible electronic health record dataset.

Laurer, M.; van Atteveldt, W.; Casas, A.; and Welbers, K. 2023. Building Efficient Universal Classifiers with Natural Language Inference. ArXiv:2312.17543 [cs].

Mayo Clinic. Mayo Clinic Health System.

Peng, B.; Galley, M.; He, P.; Brockett, C.; Liden, L.; Nouri, E.; Yu, Z.; Dolan, B.; and Gao, J. 2022. GODEL: Large-Scale Pre-training for Goal-Directed Dialog. arXiv. 

Zhang, Y.; Sun, S.; Galley, M.; Chen, Y. C.; Brockett, C.; Gao, X.; Gao, J.; Liu, J.; and Dolan, B. 2020. DialoGPT: Large-Scale Generative Pre-training for Conversational Response Generation. In ACL, system demonstration.


