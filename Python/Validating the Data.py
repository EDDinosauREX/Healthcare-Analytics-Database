from pathlib import Path

import pandas as pd


PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"

PATIENT_FILE = DATA_FOLDER / "patient_information.csv"
DIAGNOSIS_FILE = DATA_FOLDER / "patient_diagnosis.csv"
TREATMENT_FILE = DATA_FOLDER / "patient_treatments.csv"
VISIT_FILE = DATA_FOLDER / "patient_visits.csv"


def validate_primary_keys(
    patients: pd.DataFrame,
    diagnoses: pd.DataFrame,
    treatments: pd.DataFrame,
    visits: pd.DataFrame,
) -> None:
    assert patients["patient_id"].is_unique, (
        "Duplicate patient IDs found."
    )

    assert diagnoses["diagnosis_id"].is_unique, (
        "Duplicate diagnosis IDs found."
    )

    assert treatments["treatment_id"].is_unique, (
        "Duplicate treatment IDs found."
    )

    assert visits["visit_id"].is_unique, (
        "Duplicate visit IDs found."
    )


def validate_foreign_keys(
    patients: pd.DataFrame,
    diagnoses: pd.DataFrame,
    treatments: pd.DataFrame,
    visits: pd.DataFrame,
) -> None:
    valid_patient_ids = set(patients["patient_id"])
    valid_diagnosis_ids = set(diagnoses["diagnosis_id"])

    assert diagnoses["patient_id"].isin(
        valid_patient_ids
    ).all(), "Diagnosis table contains an invalid patient ID."

    assert treatments["patient_id"].isin(
        valid_patient_ids
    ).all(), "Treatment table contains an invalid patient ID."

    assert visits["patient_id"].isin(
        valid_patient_ids
    ).all(), "Visit table contains an invalid patient ID."

    assert treatments["diagnosis_id"].isin(
        valid_diagnosis_ids
    ).all(), "Treatment table contains an invalid diagnosis ID."


def validate_missing_values(
    patients: pd.DataFrame,
    diagnoses: pd.DataFrame,
    treatments: pd.DataFrame,
    visits: pd.DataFrame,
) -> None:
    required_patient_columns = [
        "patient_id",
        "patient_name",
        "region",
        "primary_type",
    ]

    required_diagnosis_columns = [
        "diagnosis_id",
        "patient_id",
        "diagnosis",
        "diagnosis_date",
    ]

    required_treatment_columns = [
        "treatment_id",
        "diagnosis_id",
        "patient_id",
        "treatment",
        "treatment_start_date",
    ]

    required_visit_columns = [
        "visit_id",
        "patient_id",
        "visit_date",
        "visit_type",
        "visit_cost",
    ]

    assert not patients[
        required_patient_columns
    ].isna().any().any(), "Missing required patient values found."

    assert not diagnoses[
        required_diagnosis_columns
    ].isna().any().any(), "Missing diagnosis values found."

    assert not treatments[
        required_treatment_columns
    ].isna().any().any(), "Missing treatment values found."

    assert not visits[
        required_visit_columns
    ].isna().any().any(), "Missing visit values found."


def validate_dates(
    diagnoses: pd.DataFrame,
    treatments: pd.DataFrame,
    visits: pd.DataFrame,
) -> None:
    diagnoses["diagnosis_date"] = pd.to_datetime(
        diagnoses["diagnosis_date"]
    )

    treatments["treatment_start_date"] = pd.to_datetime(
        treatments["treatment_start_date"]
    )

    visits["visit_date"] = pd.to_datetime(
        visits["visit_date"]
    )

    treatment_check = treatments.merge(
        diagnoses[
            [
                "diagnosis_id",
                "diagnosis_date",
            ]
        ],
        on="diagnosis_id",
        how="left",
    )

    assert (
        treatment_check["treatment_start_date"]
        >= treatment_check["diagnosis_date"]
    ).all(), "A treatment started before its diagnosis date."

    follow_up_check = visits.merge(
        diagnoses[
            [
                "patient_id",
                "diagnosis_date",
            ]
        ],
        on="patient_id",
        how="left",
    )

    follow_up_rows = follow_up_check[
        follow_up_check["visit_type"] == "Follow-Up"
    ]

    assert (
        follow_up_rows["visit_date"]
        > follow_up_rows["diagnosis_date"]
    ).all(), "A follow-up visit occurred before diagnosis."


def validate_costs(visits: pd.DataFrame) -> None:
    assert visits["visit_cost"].ge(0).all(), (
        "A negative visit cost was found."
    )


def main() -> None:
    patients = pd.read_csv(PATIENT_FILE)
    diagnoses = pd.read_csv(DIAGNOSIS_FILE)
    treatments = pd.read_csv(TREATMENT_FILE)
    visits = pd.read_csv(VISIT_FILE)

    validate_primary_keys(
        patients,
        diagnoses,
        treatments,
        visits,
    )

    validate_foreign_keys(
        patients,
        diagnoses,
        treatments,
        visits,
    )

    validate_missing_values(
        patients,
        diagnoses,
        treatments,
        visits,
    )

    validate_dates(
        diagnoses,
        treatments,
        visits,
    )

    validate_costs(visits)

    print("All data validation checks passed.")
    print(f"Patient records checked: {len(patients)}")
    print(f"Diagnosis records checked: {len(diagnoses)}")
    print(f"Treatment records checked: {len(treatments)}")
    print(f"Visit records checked: {len(visits)}")


if __name__ == "__main__":
    main()