-- Median salary (USD) per normalized role, by dataset source
SELECT
    dataset,
    role_normalized,
    COUNT(*)                                         AS n_records,
    ROUND(MEDIAN(salary_usd), 0)                     AS median_salary_usd,
    ROUND(AVG(salary_usd), 0)                        AS mean_salary_usd,
    ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary_usd), 0) AS p25,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary_usd), 0) AS p75
FROM salaries
WHERE salary_usd IS NOT NULL
GROUP BY dataset, role_normalized
ORDER BY dataset, median_salary_usd DESC;
