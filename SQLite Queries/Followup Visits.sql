-- Displays follow-up visits occur after diagnosis
SELECT
    p.patient_name,
    d.diagnosis_date,
    v.visit_date,
    v.visit_type,
    CAST(
        julianday(v.visit_date)
        - julianday(d.diagnosis_date)
        AS INTEGER
    ) AS days_after_diagnosis
FROM patient_information AS p
INNER JOIN patient_diagnosis AS d
    ON p.patient_id = d.patient_id
INNER JOIN patient_visits AS v
    ON p.patient_id = v.patient_id
WHERE v.visit_type = 'Follow-Up'
ORDER BY days_after_diagnosis;