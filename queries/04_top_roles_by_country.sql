-- Top 3 best-paid roles in each country (minimum 5 records per group)
WITH ranked AS (
    SELECT
        country_name,
        role_normalized,
        COUNT(*)                                         AS n_records,
        ROUND(MEDIAN(salary_usd), 0)                     AS median_salary,
        ROW_NUMBER() OVER (
            PARTITION BY country_name
            ORDER BY MEDIAN(salary_usd) DESC
        )                                                AS rn
    FROM salaries
    WHERE salary_usd IS NOT NULL
    GROUP BY country_name, role_normalized
    HAVING COUNT(*) >= 5
)
SELECT country_name, role_normalized, n_records, median_salary
FROM ranked
WHERE rn <= 3
ORDER BY country_name, rn;
