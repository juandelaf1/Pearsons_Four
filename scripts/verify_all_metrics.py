import pandas as pd
import numpy as np
import kagglehub
import os
from scipy.stats import pearsonr, spearmanr, f_oneway, ttest_ind

path = kagglehub.dataset_download("arshkon/linkedin-job-postings")
df = pd.read_csv(os.path.join(path, "postings.csv"))

# Filter data roles
data_keywords = "data scientist|data engineer|data analyst|machine learning|ml engineer|ai engineer|business intelligence|data architect|analytics|data manager"
df_data = df[df["title"].str.contains(data_keywords, case=False, na=False)].copy()

# Clean for stats
df_clean = df_data[(df_data["normalized_salary"] >= 1000) & (df_data["normalized_salary"] <= 2000000)].copy()
df_clean["is_remote"] = df_clean["remote_allowed"].fillna(0).astype(bool)
exp_map = {"internship": 0, "entry level": 1, "associate": 2, "mid-senior level": 3, "director": 4, "executive": 5}
df_clean["experience_level_num"] = df_clean["formatted_experience_level"].str.lower().map(exp_map)

sal = df_clean["normalized_salary"].dropna()

print("=" * 60)
print("CORRECTED METRICS - DATA ROLES ONLY")
print("=" * 60)

# 1. Descriptive
print(f"\n1. DESCRIPTIVE STATISTICS")
print(f"   Records: {len(sal)}")
print(f"   Mean:    ${sal.mean():,.0f}")
print(f"   Median:  ${sal.median():,.0f}")
print(f"   Std:     ${sal.std():,.0f}")
print(f"   Q1:      ${sal.quantile(0.25):,.0f}")
print(f"   Q3:      ${sal.quantile(0.75):,.0f}")

# 2. Experience levels
print(f"\n2. SALARY BY EXPERIENCE LEVEL")
exp_order = ["Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
for level in exp_order:
    d = df_clean[df_clean["formatted_experience_level"] == level]["normalized_salary"]
    if len(d) > 0:
        print(f"   {level:20s}: median=${d.median():>8,.0f}  mean=${d.mean():>9,.0f}  (n={len(d)})")

# 3. Remote premium (DATA ROLES ONLY)
remote = df_clean[df_clean["is_remote"]]["normalized_salary"].dropna()
onsite = df_clean[~df_clean["is_remote"]]["normalized_salary"].dropna()
print(f"\n3. REMOTE PREMIUM (DATA ROLES)")
print(f"   Remote median:  ${remote.median():>8,.0f}  (n={len(remote)})")
print(f"   On-site median: ${onsite.median():>8,.0f}  (n={len(onsite)})")
prem = ((remote.median() / onsite.median()) - 1) * 100
t_stat, p_val = ttest_ind(remote, onsite, equal_var=False)
print(f"   Premium: {prem:+.1f}%  (Welch t-test: p={p_val:.4f})")

# 4. Correlations (Pearson + Spearman)
v = df_clean[["normalized_salary", "views", "applies", "experience_level_num", "is_remote"]].dropna()
print(f"\n4. CORRELATIONS (n={len(v)})")
print(f"   {'Pair':30s} {'Pearson r':>12s} {'Spearman rho':>12s}")
for col in ["views", "applies", "experience_level_num", "is_remote"]:
    r_p, p_p = pearsonr(v["normalized_salary"], v[col])
    r_s, p_s = spearmanr(v["normalized_salary"], v[col])
    print(f"   {'Salary vs ' + col:30s} {r_p:>8.3f} (p={p_p:.4f})  {r_s:>8.3f} (p={p_s:.4f})")

# Views vs Applies
r_va, p_va = pearsonr(v["views"], v["applies"])
print(f"   {'Views vs Applies':30s} {r_va:>8.3f} (p={p_va:.4f})")

# 5. ANOVA
print(f"\n5. ANOVA - EXPERIENCE vs SALARY")
groups = [g["normalized_salary"].values for _, g in df_clean.groupby("formatted_experience_level")]
f_stat, p_anova = f_oneway(*groups)
print(f"   F-statistic: {f_stat:.2f}")
print(f"   p-value: {p_anova:.6f}")
print(f"   Significant: {'YES' if p_anova < 0.05 else 'NO'}")

# 6. Conditional probability Python
print(f"\n6. CONDITIONAL PROBABILITY - PYTHON")
high_threshold = sal.quantile(0.75)
df_clean["is_high_salary"] = df_clean["normalized_salary"] > high_threshold
df_clean["has_python"] = df_clean["skills_desc"].str.contains("Python", case=False, na=False)
p_py = df_clean[df_clean["has_python"]]["is_high_salary"].mean() * 100
p_no = df_clean[~df_clean["has_python"]]["is_high_salary"].mean() * 100
print(f"   High salary threshold: >${high_threshold:,.0f}")
print(f"   P(High Salary | Python)    = {p_py:.2f}%")
print(f"   P(High Salary | No Python) = {p_no:.2f}%")
print(f"   Lift: +{((p_py/p_no)-1)*100:.1f}%")

# 7. ALL POSTINGS (for comparison)
print(f"\n{'='*60}")
print(f"COMPARISON - ALL POSTINGS (not just data roles)")
print(f"{'='*60}")
sal_all = df["normalized_salary"].dropna()
clean_all = sal_all[(sal_all >= 1000) & (sal_all <= 2000000)]
print(f"   Median overall: ${clean_all.median():,.0f}")
df_all = df[df["normalized_salary"].between(1000, 2000000)].copy()
df_all["is_remote"] = df_all["remote_allowed"].fillna(0).astype(bool)
r_all = df_all[df_all["is_remote"]]["normalized_salary"]
o_all = df_all[~df_all["is_remote"]]["normalized_salary"]
print(f"   Remote median:  ${r_all.median():,.0f}")
print(f"   On-site median: ${o_all.median():,.0f}")
prem_all = ((r_all.median() / o_all.median()) - 1) * 100
print(f"   Premium: +{prem_all:.1f}%")

# 8. Spain context
print(f"\n{'='*60}")
print(f"SPAIN CONTEXT (from portfolio_notebooks)")
print(f"{'='*60}")
print(f"   INE Sector J (2024):      42,742 EUR")
print(f"   Ametic/Expansion (2025):  48,900 EUR")
print(f"   Manfred median (2026):    ~45,000 EUR")
print(f"   LinkedIn Data Roles:      ${sal.median():,.0f} USD")
print(f"   Adjustment factor (USD->EUR Spain): ~0.48x")
print(f"   Adjusted Spain estimate:  ${sal.median()*0.48:,.0f} USD = ~{sal.median()*0.48*0.92:,.0f} EUR")
