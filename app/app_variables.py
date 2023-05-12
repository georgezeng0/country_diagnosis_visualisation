# Variables 
data_url = "https://raw.githubusercontent.com/drpawelo/python-advanced-HSC/main/week_05/starting_code/OCED_simplified.csv"

# Dictionary to map categories of diagnoses to columns
diagnoses_categories_map = {
    "Infectious and parasitic diseases": [
        "Intestinal infectious diseases except diarrhoea_Per 100 000 population",
        "Diarrhoea and gastroenteritis of presumed infectious origin_Per 100 000 population",
        "Tuberculosis_Per 100 000 population",
        "Septicaemia_Per 100 000 population",
        "Human immunodeficiency virus (HIV) disease_Per 100 000 population",
        "Other infectious and parasitic diseases_Per 100 000 population",
    ],
    "Neoplasms": [
        "Malignant neoplasm of colon, rectum and anus_Per 100 000 population",
        "Malignant neoplasm of trachea, bronchus and lung_Per 100 000 population",
        "Malignant neoplasm of skin_Per 100 000 population",
        "Malignant neoplasm of breast_Per 100 000 females",
        "Malignant neoplasm of uterus_Per 100 000 females",
        "Malignant neoplasm of ovary_Per 100 000 females",
        "Malignant neoplasm of prostate_Per 100 000 males",
        "Malignant neoplasm of bladder_Per 100 000 population",
        "Other Malignant neoplasms_Per 100 000 population",
        "Carcinoma in situ_Per 100 000 population",
        "Benign neoplasm of colon, rectum and anus_Per 100 000 population",
        "Leiomyoma of uterus_Per 100 000 females",
        "Other Benign neoplasms and neoplasms of uncertain or unknown behaviour_Per 100 000 population",
    ],
    "Diseases of the blood and bloodforming organs": [
        "Anaemias_Per 100 000 population",
        "Other diseases of the blood and bloodforming organs_Per 100 000 population",
    ],
    "Endocrine, nutritional and metabolic diseases": [
        "Diabetes mellitus_Per 100 000 population",
        "Other endocrine, nutritional and metabolic diseases_Per 100 000 population",
    ],
    "Mental and behavioural disorders": [
        "Dementia_Per 100 000 population",
        "Mental and behavioural disorders due to alcohol_Per 100 000 population",
        "Mental and behavioural disorders due to use of Other psychoactive substance_Per 100 000 population",
        "Schizophrenia, schizotypal and delusional disorders_Per 100 000 population",
        "Mood (affective) disorders_Per 100 000 population",
        "Other Mental and behavioural disorders_Per 100 000 population",
    ],
    "Diseases of the nervous system": [
        "Alzheimer's disease_Per 100 000 population",
        "Multiple sclerosis_Per 100 000 population",
        "Epilepsy_Per 100 000 population",
        "Transient cerebral ischaemic attacks and related syndromes_Per 100 000 population",
        "Other diseases of the nervous system_Per 100 000 population",
    ],
    "Diseases of the eye and adnexa": [
        "Cataract_Per 100 000 population",
        "Other diseases of the eye and adnexa_Per 100 000 population",
    ],
    "Diseases of the ear and mastoid process": [
        "Diseases of the ear and mastoid process_Per 100 000 population"
    ],
    "Diseases of the circulatory system": [
        "Hypertensive diseases_Per 100 000 population",
        "Angina pectoris_Per 100 000 population",
        "Acute myocardial infarction_Per 100 000 population",
        "Other ischaemic heart disease_Per 100 000 population",
        "Pulmonary heart disease and diseases of Pulmonary circulation_Per 100 000 population",
        "Conduction disorders and cardiac arrhythmias_Per 100 000 population",
        "Heart failure_Per 100 000 population",
        "Cerebrovascular diseases_Per 100 000 population",
        "Atherosclerosis_Per 100 000 population",
        "Varicose veins of lower extremities_Per 100 000 population",
        "Other diseases of the circulatory system_Per 100 000 population",
    ],
    "Diseases of the respiratory system": [
        "Acute upper respiratory infections and influenza_Per 100 000 population",
        "Pneumonia_Per 100 000 population",
        "Other acute lower respiratory infections_Per 100 000 population",
        "Chronic diseases of tonsils and adenoids_Per 100 000 population",
        "Other diseases of upper respiratory tract_Per 100 000 population",
        "Chronic obstructive Pulmonary disease and bronchiectasis_Per 100 000 population",
        "Asthma_Per 100 000 population",
        "Other diseases of the respiratory system_Per 100 000 population",
    ],
    "Diseases of the digestive system": [
        "Disorders of teeth and supporting structures_Per 100 000 population",
        "Other diseases of oral cavity, salivary glands and jaws_Per 100 000 population",
        "Diseases of oesophagus_Per 100 000 population",
        "Peptic ulcer_Per 100 000 population",
        "Dyspepsia and Other diseases of stomach and duodenum_Per 100 000 population",
        "Diseases of appendix_Per 100 000 population",
        "Inguinal hernia_Per 100 000 population",
        "Other abdominal hernia_Per 100 000 population",
        "Crohn's disease and ulcerative colitis_Per 100 000 population",
        "Other noninfective gastroenteritis and colitis_Per 100 000 population",
        "Paralytic ileus and Intestinal obstruction without hernia_Per 100 000 population",
        "Diverticular disease of intestine_Per 100 000 population",
        "Diseases of anus and rectum_Per 100 000 population",
        "Other diseases of intestine_Per 100 000 population",
        "Alcoholic liver disease_Per 100 000 population",
        "Other diseases of liver_Per 100 000 population",
        "Cholelithiasis_Per 100 000 population",
        "Other diseases of gall bladder and biliary tract_Per 100 000 population",
        "Diseases of pancreas_Per 100 000 population",
        "Other diseases of the digestive system_Per 100 000 population",
    ],
    "Diseases of the skin and subcutaneous tissue": [
        "Infections of the skin and subcutaneous tissue_Per 100 000 population",
        "Dermatitis, eczema and papulosquamous disorders_Per 100 000 population",
        "Other diseases of the skin and subcutaneous tissue_Per 100 000 population",
    ],
    "Diseases of musculoskeletal system and connective tissue": [
        "Coxarthrosis (arthrosis of hip)_Per 100 000 population",
        "Gonarthrosis (arthrosis of knee)_Per 100 000 population",
        "Internal derangement of knee_Per 100 000 population",
        "Other arthropathies_Per 100 000 population",
        "Systemic connective tissue disorders_Per 100 000 population",
        "Deforming dorsopathies and spondylopathies_Per 100 000 population",
        "Intervertebral disc disorders_Per 100 000 population",
        "Dorsalgia_Per 100 000 population",
        "Soft tissue disorders_Per 100 000 population",
        "Other disorders of the musculoskeletal system and connective tissue_Per 100 000 population",
    ],
    "Diseases of the genitourinary system": [
        "Glomerular and renal tubulo-interstitial diseases_Per 100 000 population",
        "Renal failure_Per 100 000 population",
        "Urolithiasis_Per 100 000 population",
        "Other diseases of the urinary system_Per 100 000 population",
        "Hyperplasia of prostate_Per 100 000 males",
        "Other diseases of Male genital organs_Per 100 000 males",
        "Disorders of breast_Per 100 000 females",
        "Inflammatory diseases of Female pelvic organs_Per 100 000 females",
        "Menstrual, menopausal and Other Female genital conditions_Per 100 000 females",
        "Other disorders of the genitourinary system_Per 100 000 females",
    ],
    "Pregnancy, childbirth and the puerperium": [
        "Medical abortion_Per 100 000 females",
        "Other pregnancy with abortive outcome_Per 100 000 females",
        "Complications of pregnancy in the antenatal period_Per 100 000 females",
        "Complications of pregnancy predominantly during labour and delivery_Per 100 000 females",
        "Single spontaneous delivery_Per 100 000 females",
        "Other delivery_Per 100 000 females",
        "Complications predominantly related to the puerperium_Per 100 000 females",
        "Other obstetric conditions_Per 100 000 females",
    ],
    "Certain conditions originating in the perinatal period": [
        "Disorders related to short gestation and low birthweight_Per 100 000 population",
        "Other conditions originating in the perinatal period_Per 100 000 population",
    ],
    "Congenital malformations, deformations and chromosomal abnormalities": [
        "Congenital malformations, deformations and chromosomal abnormalities_Per 100 000 population"
    ],
    "Symptoms, signs and abnormal clinical and laboratory findings, n.e.c.": [
        "Pain in throat and chest_Per 100 000 population",
        "Abdominal and pelvic Pain_Per 100 000 population",
        "Unknown and unspecified causes of morbidity_Per 100 000 population",
        "Other symptoms, signs and abnormal clinical and laboratory findings_Per 100 000 population",
    ],
    "Injury, poisoning and other consequences of external causes": [
        "Intracranial injury_Per 100 000 population",
        "Other injuries to the head_Per 100 000 population",
        "Fracture of forearm_Per 100 000 population",
        "Fracture of femur_Per 100 000 population",
        "Fracture of lower leg, including ankle_Per 100 000 population",
        "Other injuries_Per 100 000 population",
        "Burns and corrosions_Per 100 000 population",
        "Poisonings by drugs, medicaments, and biological substances and toxic effects_Per 100 000 population",
        "Complications of Surgical and medical care, n.e.c._Per 100 000 population",
        "Sequelae of injuries, of poisoning and of Other external causes_Per 100 000 population",
        "Other and unspecified effects of external causes_Per 100 000 population",
    ],
    "Factors influencing health status and contact with health services": [
        "Medical observation and evaluation for suspected diseases and conditions_Per 100 000 population",
        "Contraceptive management_Per 100 000 population",
        "Liveborn infants according to place of birth_Per 100 000 population",
        "Other medical care (including radiotherapy and chemotherapy sessions)_Per 100 000 population",
        "Other factors influencing Health status and contact with Health services_Per 100 000 population",
    ],
}

diagnoses_categories_map_aggregates = {
    "Infectious and parasitic diseases": "Infectious and parasitic diseases_Per 100 000 population",
    "Neoplasms": "Neoplasms_Per 100 000 population",
    "Diseases of the blood and bloodforming organs": "Diseases of the blood and bloodforming organs_Per 100 000 population",
    "Endocrine, nutritional and metabolic diseases": "Endocrine, nutritional and metabolic diseases_Per 100 000 population",
    "Mental and behavioural disorders": "Mental and behavioural disorders_Per 100 000 population",
    "Diseases of the nervous system": "Diseases of the nervous system_Per 100 000 population",
    "Diseases of the eye and adnexa": "Diseases of the eye and adnexa_Per 100 000 population",
    # "Diseases of the ear and mastoid process":  'Diseases of the ear and mastoid process_Per 100 000 population', # Duplicate
    "Diseases of the circulatory system": "Diseases of the circulatory system_Per 100 000 population",
    "Diseases of the respiratory system": "Diseases of the respiratory system_Per 100 000 population",
    "Diseases of the digestive system": "Diseases of the digestive system_Per 100 000 population",
    "Diseases of the skin and subcutaneous tissue": "Diseases of the skin and subcutaneous tissue_Per 100 000 population",
    "Diseases of musculoskeletal system and connective tissue": "Diseases of musculoskeletal system and connective tissue_Per 100 000 population",
    "Diseases of the genitourinary system": "Diseases of the genitourinary system_Per 100 000 population",
    "Pregnancy, childbirth and the puerperium": "Pregnancy, childbirth and the puerperium_Per 100 000 females",
    "Certain conditions originating in the perinatal period": "Certain conditions originating in the perinatal period_Per 100 000 population",
    # "Congenital malformations, deformations and chromosomal abnormalities": 'Congenital malformations, deformations and chromosomal abnormalities_Per 100 000 population', # Duplicate
    "Symptoms, signs and abnormal clinical and laboratory findings, n.e.c.": "Symptoms, signs and abnormal clinical and laboratory findings, n.e.c._Per 100 000 population",
    "Injury, poisoning and other consequences of external causes": "Injury, poisoning and other consequences of external causes_Per 100 000 population",
    "Factors influencing health status and contact with health services": "Factors influencing health status and contact with health services_Per 100 000 population",
}
