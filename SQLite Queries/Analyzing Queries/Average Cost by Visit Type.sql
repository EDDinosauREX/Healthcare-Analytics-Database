-- Displays the Average Cost based on the type of visit
SELECT
    visit_type,
    COUNT(*) AS visit_count,
    ROUND(AVG(visit_cost), 2) AS average_visit_cost,
    ROUND(MIN(visit_cost), 2) AS minimum_visit_cost,
    ROUND(MAX(visit_cost), 2) AS maximum_visit_cost
FROM patient_visits
GROUP BY visit_type
ORDER BY average_visit_cost DESC;