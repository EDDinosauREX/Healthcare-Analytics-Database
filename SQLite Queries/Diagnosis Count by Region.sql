--Displays the diagnosis count by region
SELECT
    p.region,
    d.diagnosis,
    COUNT(*) AS diagnosis_count
FROM patient_information AS p
INNER JOIN patient_diagnosis AS d
    ON p.patient_id = d.patient_id
GROUP BY
    p.region,
    d.diagnosis
ORDER BY
    p.region,
    diagnosis_count DESC;