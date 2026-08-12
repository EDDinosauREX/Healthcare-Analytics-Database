-- Displays the patients record
SELECT
    p.patient_id,
    p.patient_name,
    p.region,
    d.diagnosis,
    d.diagnosis_date,
    t.treatment,
    t.treatment_start_date,
    v.visit_type,
    v.visit_date,
    ROUND(v.visit_cost, 2) AS visit_cost
FROM patient_information AS p
INNER JOIN patient_diagnosis AS d
    ON p.patient_id = d.patient_id
INNER JOIN patient_treatments AS t
    ON d.diagnosis_id = t.diagnosis_id
INNER JOIN patient_visits AS v
    ON p.patient_id = v.patient_id
ORDER BY p.patient_id;
