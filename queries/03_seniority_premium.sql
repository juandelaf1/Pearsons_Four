-- Salary premium per seniority level relative to Entry within each role
WITH base AS (
    SELECT
        role_normalized,
        seniority,
        ROUND(MEDIAN(salary_usd), 0) AS median_salary
    FROM salaries
    WHERE salary_usd IS NOT NULL AND seniority IS NOT NULL
    GROUP BY role_normalized, seniority
),
entry AS (
    SELECT role_normalized, median_salary AS entry_salary
    FROM base
    WHERE seniority = 'Entry'
)
SELECT
    b.role_normalized,
    b.seniority,
    b.median_salary,
    ROUND(b.median_salary - e.entry_salary, 0)              AS premium_usd,
    ROUND(100.0 * (b.median_salary - e.entry_salary) / NULLIF(e.entry_salary, 0), 1) AS premium_pct
FROM base b
LEFT JOIN entry e ON b.role_normalized = e.role_normalized
WHERE b.seniority != 'Entry'
ORDER BY b.role_normalized, premium_pct DESC;
