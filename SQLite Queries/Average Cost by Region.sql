-- Displays Average visit cost by region
SELECT
    p.region,
    COUNT(*) AS visit_count,
    ROUND(AVG(v.visit_cost), 2) AS average_visit_cost,
    ROUND(SUM(v.visit_cost), 2) AS total_visit_cost
FROM patient_information AS p
INNER JOIN patient_visits AS v
    ON p.patient_id = v.patient_id
GROUP BY p.region
ORDER BY average_visit_cost DESC;
