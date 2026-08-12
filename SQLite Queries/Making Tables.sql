PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS patient_visits;
DROP TABLE IF EXISTS patient_treatments;
DROP TABLE IF EXISTS patient_diagnosis;
DROP TABLE IF EXISTS patient_information;


CREATE TABLE patient_information (
    patient_id INTEGER PRIMARY KEY,
    national_dex_number INTEGER NOT NULL,
    patient_name TEXT NOT NULL,
    region TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_type TEXT,
    hp INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    special_attack INTEGER NOT NULL,
    special_defense INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    stat_total INTEGER NOT NULL
);


CREATE TABLE patient_diagnosis (
    diagnosis_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    diagnosis TEXT NOT NULL,
    diagnosis_date TEXT NOT NULL,

    FOREIGN KEY (patient_id)
        REFERENCES patient_information(patient_id)
);


CREATE TABLE patient_treatments (
    treatment_id INTEGER PRIMARY KEY,
    diagnosis_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    treatment TEXT NOT NULL,
    treatment_start_date TEXT NOT NULL,

    FOREIGN KEY (diagnosis_id)
        REFERENCES patient_diagnosis(diagnosis_id),

    FOREIGN KEY (patient_id)
        REFERENCES patient_information(patient_id)
);


CREATE TABLE patient_visits (
    visit_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    visit_date TEXT NOT NULL,
    visit_type TEXT NOT NULL,
    visit_cost REAL NOT NULL CHECK (visit_cost >= 0),

    FOREIGN KEY (patient_id)
        REFERENCES patient_information(patient_id)
);