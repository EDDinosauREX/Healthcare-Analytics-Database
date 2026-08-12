-- Displays the average delay for a treatment
SELECT
    d.diagnosis,
    COUNT(*) AS patient_count,
    ROUND(
        AVG(
            julianday(t.treatment_start_date)
            - julianday(d.diagnosis_date)
        ),
        2
    ) AS average_days_to_treatment
FROM patient_diagnosis AS d
INNER JOIN patient_treatments AS t
    ON d.diagnosis_id = t.diagnosis_id
GROUP BY d.diagnosis
ORDER BY average_days_to_treatment DESC;