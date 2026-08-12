from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# File locations
# ---------------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"

SOURCE_FILE = DATA_FOLDER / "Pokemon Database - Pokemon.csv"

PATIENT_FILE = DATA_FOLDER / "patient_information.csv"
DIAGNOSIS_FILE = DATA_FOLDER / "patient_diagnosis.csv"
TREATMENT_FILE = DATA_FOLDER / "patient_treatments.csv"
VISIT_FILE = DATA_FOLDER / "patient_visits.csv"


# ---------------------------------------------------------
# Reproducible random number generator
# ---------------------------------------------------------

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


# ---------------------------------------------------------
# Diagnosis and treatment information
# ---------------------------------------------------------

DIAGNOSES = [
    "Hypertension",
    "Type 2 Diabetes",
    "Hyperlipidemia",
    "Obesity",
    "Coronary Artery Disease",
    "Heart Failure",
    "Chronic Kidney Disease",
    "Asthma",
    "Chronic Obstructive Pulmonary Disease",
    "Pneumonia",
    "Sleep Apnea",
    "Anemia",
    "Insomnia",
    "Osteoarthritis",
    "Osteoporosis",
    "Epilepsy",
]

TREATMENTS = {
    "Hypertension": ["Lisinopril", "Losartan", "Amlodipine"],
    "Type 2 Diabetes": ["Metformin", "Insulin", "Ozempic"],
    "Hyperlipidemia": ["Atorvastatin", "Rosuvastatin"],
    "Obesity": ["Wegovy", "Lifestyle Counseling"],
    "Coronary Artery Disease": ["Aspirin", "Atorvastatin"],
    "Heart Failure": ["Furosemide", "Carvedilol"],
    "Chronic Kidney Disease": ["Losartan", "Sodium Bicarbonate"],
    "Asthma": ["Albuterol", "Fluticasone"],
    "Chronic Obstructive Pulmonary Disease": [
        "Tiotropium",
        "Albuterol",
    ],
    "Pneumonia": ["Amoxicillin", "Azithromycin"],
    "Sleep Apnea": ["CPAP Therapy"],
    "Anemia": ["Iron Supplements", "Vitamin B12"],
    "Insomnia": ["Melatonin", "CBT-I"],
    "Osteoarthritis": ["Ibuprofen", "Physical Therapy"],
    "Osteoporosis": ["Alendronate", "Calcium + Vitamin D"],
    "Epilepsy": ["Levetiracetam", "Lamotrigine"],
}

VISIT_COST_RANGES = {
    "Primary Care": (100, 400),
    "Specialist": (200, 700),
    "Emergency": (800, 2500),
    "Urgent Care": (150, 600),
    "Follow-Up": (75, 300),
}


# ---------------------------------------------------------
# Create patient table
# ---------------------------------------------------------

def create_patient_table() -> pd.DataFrame:
    """Create a balanced sample of 25 records from each region."""

    pokemon = pd.read_csv(SOURCE_FILE)

    pokemon["Region"] = pokemon["Region"].replace(
        {
            "Kitakami (Paldea)": "Paldea",
            "Blueberry (Paldea)": "Paldea",
        }
    )

    pokemon = pokemon[pokemon["Region"] != "Hisui"].copy()

    patients = (
        pokemon.groupby("Region", group_keys=False)
        .sample(n=25, random_state=RANDOM_SEED)
        .reset_index(drop=True)
    )

    patients.insert(
        0,
        "PatientID",
        range(1, len(patients) + 1),
    )

    # Keep a smaller set of fields so the patient table is easier to use.
    patients = patients[
        [
            "PatientID",
            "National Dex Number",
            "Name",
            "Region",
            "Type I",
            "Type II",
            "Hp",
            "Atk",
            "Def",
            "Sp Atk",
            "Sp Def",
            "Speed",
            "Stat Total",
        ]
    ].copy()

    # Rename columns to SQL-friendly snake_case names.
    patients = patients.rename(
        columns={
            "PatientID": "patient_id",
            "National Dex Number": "national_dex_number",
            "Name": "patient_name",
            "Region": "region",
            "Type I": "primary_type",
            "Type II": "secondary_type",
            "Hp": "hp",
            "Atk": "attack",
            "Def": "defense",
            "Sp Atk": "special_attack",
            "Sp Def": "special_defense",
            "Speed": "speed",
            "Stat Total": "stat_total",
        }
    )

    patients.to_csv(PATIENT_FILE, index=False)

    return patients


# ---------------------------------------------------------
# Create diagnosis table
# ---------------------------------------------------------

def create_diagnosis_table(
    patients: pd.DataFrame,
) -> pd.DataFrame:
    """Assign one synthetic diagnosis to each patient."""

    start_date = pd.Timestamp("2022-01-01")
    end_date = pd.Timestamp("2025-12-31")

    total_days = (end_date - start_date).days

    diagnoses = pd.DataFrame(
        {
            "diagnosis_id": range(1, len(patients) + 1),
            "patient_id": patients["patient_id"],
            "diagnosis": rng.choice(
                DIAGNOSES,
                size=len(patients),
            ),
            "diagnosis_date": start_date
            + pd.to_timedelta(
                rng.integers(
                    0,
                    total_days + 1,
                    size=len(patients),
                ),
                unit="D",
            ),
        }
    )

    diagnoses.to_csv(
        DIAGNOSIS_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )

    return diagnoses


# ---------------------------------------------------------
# Create treatment table
# ---------------------------------------------------------

def create_treatment_table(
    diagnoses: pd.DataFrame,
) -> pd.DataFrame:
    """Assign a diagnosis-appropriate treatment."""

    treatment_names = [
        rng.choice(TREATMENTS[diagnosis])
        for diagnosis in diagnoses["diagnosis"]
    ]

    treatment_delays = rng.integers(
        0,
        31,
        size=len(diagnoses),
    )

    treatments = pd.DataFrame(
        {
            "treatment_id": range(1, len(diagnoses) + 1),
            "diagnosis_id": diagnoses["diagnosis_id"],
            "patient_id": diagnoses["patient_id"],
            "treatment": treatment_names,
            "treatment_start_date": (
                pd.to_datetime(diagnoses["diagnosis_date"])
                + pd.to_timedelta(treatment_delays, unit="D")
            ),
        }
    )

    treatments.to_csv(
        TREATMENT_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )

    return treatments


# ---------------------------------------------------------
# Create visit table
# ---------------------------------------------------------

def create_visit_table(
    diagnoses: pd.DataFrame,
) -> pd.DataFrame:
    """Create one synthetic visit for each patient."""

    visit_types = list(VISIT_COST_RANGES.keys())

    selected_visit_types = rng.choice(
        visit_types,
        size=len(diagnoses),
    )

    visit_dates = []
    visit_costs = []

    for diagnosis_date, visit_type in zip(
        pd.to_datetime(diagnoses["diagnosis_date"]),
        selected_visit_types,
    ):
        if visit_type == "Follow-Up":
            # Follow-up visits occur 1–90 days after diagnosis.
            days_after = int(rng.integers(1, 91))
            visit_date = diagnosis_date + pd.Timedelta(
                days=days_after
            )
        else:
            # Other visits may occur up to 60 days before or
            # 90 days after diagnosis.
            date_difference = int(rng.integers(-60, 91))
            visit_date = diagnosis_date + pd.Timedelta(
                days=date_difference
            )

        minimum_cost, maximum_cost = VISIT_COST_RANGES[
            visit_type
        ]

        visit_cost = round(
            float(rng.uniform(minimum_cost, maximum_cost)),
            2,
        )

        visit_dates.append(visit_date)
        visit_costs.append(visit_cost)

    visits = pd.DataFrame(
        {
            "visit_id": range(1, len(diagnoses) + 1),
            "patient_id": diagnoses["patient_id"],
            "visit_date": visit_dates,
            "visit_type": selected_visit_types,
            "visit_cost": visit_costs,
        }
    )

    visits.to_csv(
        VISIT_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )

    return visits


# ---------------------------------------------------------
# Run the complete workflow
# ---------------------------------------------------------

def main() -> None:
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_FILE}"
        )

    patients = create_patient_table()
    diagnoses = create_diagnosis_table(patients)
    treatments = create_treatment_table(diagnoses)
    visits = create_visit_table(diagnoses)

    print("Healthcare-style datasets created successfully.")
    print(f"Patients: {len(patients)}")
    print(f"Diagnoses: {len(diagnoses)}")
    print(f"Treatments: {len(treatments)}")
    print(f"Visits: {len(visits)}")
    print(f"Files saved in: {DATA_FOLDER}")


if __name__ == "__main__":
    main()