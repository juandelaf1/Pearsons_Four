-- Market sizing: record count and salary distribution by role + seniority + country
SELECT
    role_normalized,
    seniority,
    country_name,
    COUNT(*)                                         AS n_records,
    ROUND(MEDIAN(salary_usd), 0)                     AS median_salary,
    ROUND(MIN(salary_usd), 0)                        AS min_salary,
    ROUND(MAX(salary_usd), 0)                        AS max_salary,
    ROUND(STDDEV(salary_usd), 0)                     AS std_salary
FROM salaries
WHERE salary_usd IS NOT NULL
GROUP BY role_normalized, seniority, country_name
HAVING COUNT(*) >= 3
ORDER BY n_records DESC;
