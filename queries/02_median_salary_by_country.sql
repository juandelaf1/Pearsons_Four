-- Median salary (USD) by country, across all roles
SELECT
    country_name,
    COUNT(*)                                         AS n_records,
    ROUND(MEDIAN(salary_usd), 0)                     AS median_salary_usd,
    ROUND(AVG(salary_usd), 0)                        AS mean_salary_usd,
    ROUND(MEDIAN(salary_ppp_usd), 0)                 AS median_ppp_usd,
    ROUND(AVG(salary_ppp_usd), 0)                    AS mean_ppp_usd
FROM salaries
WHERE salary_usd IS NOT NULL
GROUP BY country_name
HAVING COUNT(*) >= 5
ORDER BY median_salary_usd DESC;
