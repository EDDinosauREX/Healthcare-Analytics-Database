-- Displays the patients with the five most expensive visits
SELECT
    p.patient_name,
    p.region,
    v.visit_type,
    ROUND(v.visit_cost, 2) AS visit_cost
FROM patient_information AS p
INNER JOIN patient_visits AS v
    ON p.patient_id = v.patient_id
ORDER BY v.visit_cost DESC
LIMIT 5;