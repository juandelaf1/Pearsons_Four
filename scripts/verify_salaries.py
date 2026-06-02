import pandas as pd
import numpy as np
import kagglehub
import os
from scipy.stats import pearsonr

# Load LinkedIn data
path = kagglehub.dataset_download("arshkon/linkedin-job-postings")
df = pd.read_csv(os.path.join(path, "postings.csv"))

# Filter data roles
data_keywords = "data scientist|data engineer|data analyst|machine learning|ml engineer|ai engineer|business intelligence|data architect|analytics|data manager"
df_data = df[df["title"].str.contains(data_keywords, case=False, na=False)].copy()

# Salary stats on data roles
sal = df_data["normalized_salary"].dropna()
print("=== RAW DATA ROLES SALARY (before any filtering) ===")
print(f"Records with salary: {len(sal)}")
print(f"Mean: ${sal.mean():,.0f}")
print(f"Median: ${sal.median():,.0f}")
print(f"Std: ${sal.std():,.0f}")
print(f"Min: ${sal.min():,.0f}")
print(f"Max: ${sal.max():,.0f}")
print(f"Q1: ${sal.quantile(0.25):,.0f}")
print(f"Q3: ${sal.quantile(0.75):,.0f}")

# Suspicious values
print(f"\nSalaries < $1,000: {len(sal[sal < 1000])} rows")
print(f"Salaries > $1,000,000: {len(sal[sal > 1000000])} rows")
print(f"Salaries > $500,000: {len(sal[sal > 500000])} rows")

# After basic filtering
clean = sal[(sal >= 1000) & (sal <= 2000000)]
print("\n=== AFTER FILTERING (< $1K and > $2M removed) ===")
print(f"Records: {len(clean)}")
print(f"Mean: ${clean.mean():,.0f}")
print(f"Median: ${clean.median():,.0f}")
print(f"Min: ${clean.min():,.0f}")
print(f"Max: ${clean.max():,.0f}")
print(f"Q1: ${clean.quantile(0.25):,.0f}")
print(f"Q3: ${clean.quantile(0.75):,.0f}")

# Remote premium
df_clean = df_data[(df_data["normalized_salary"] >= 1000) & (df_data["normalized_salary"] <= 2000000)].copy()
df_clean["is_remote"] = df_clean["remote_allowed"].fillna(0).astype(bool)
remote = df_clean[df_clean["is_remote"]]["normalized_salary"].dropna()
onsite = df_clean[~df_clean["is_remote"]]["normalized_salary"].dropna()
print("\n=== REMOTE PREMIUM ===")
print(f"Remote median: ${remote.median():,.0f} (n={len(remote)})")
print(f"On-site median: ${onsite.median():,.0f} (n={len(onsite)})")
premium = ((remote.median() / onsite.median()) - 1) * 100
print(f"Premium: +{premium:.1f}%")

# Experience levels
exp_order = ["Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
print("\n=== SALARY BY EXPERIENCE (median) ===")
for level in exp_order:
    d = df_clean[df_clean["formatted_experience_level"] == level]["normalized_salary"]
    if len(d) > 0:
        print(f"{level:25s}: ${d.median():>8,.0f} (n={len(d)})")

# Correlation views vs applies
r, p = pearsonr(df_clean["views"], df_clean["applies"])
print(f"\n=== VIEWS VS APPLIES ===")
print(f"Pearson r = {r:.2f}, p = {p:.4f}")

# Views vs Salary
r2, p2 = pearsonr(df_clean["views"], df_clean["normalized_salary"])
print(f"Views vs Salary: r = {r2:.2f}, p = {p2:.4f}")

# Location analysis
print("\n=== LOCATION ANALYSIS ===")
spain = df_data[df_data["location"].str.contains("spain|españa|madrid|barcelona", case=False, na=False)]
print(f"Spain-related postings: {len(spain)}")
if len(spain) > 0:
    print(spain["location"].value_counts().head(10))

# Industry analysis
print("\n=== TOP INDUSTRIES ===")
company_ind = pd.read_csv(os.path.join(path, "companies", "company_industries.csv"))
df_ind = df_clean.merge(company_ind, on="company_id", how="left")
print(df_ind["industry"].value_counts().head(10))

# Check on ALL postings (not just data roles)
print("\n=== ALL POSTINGS (ALL roles, not just data) ===")
sal_all = df["normalized_salary"].dropna()
clean_all = sal_all[(sal_all >= 1000) & (sal_all <= 2000000)]
print(f"Records: {len(clean_all)}")
print(f"Median: ${clean_all.median():,.0f}")
print(f"Mean: ${clean_all.mean():,.0f}")

df_all = df[df["normalized_salary"].between(1000, 2000000)].copy()
df_all["is_remote"] = df_all["remote_allowed"].fillna(0).astype(bool)
r = df_all[df_all["is_remote"]]["normalized_salary"]
o = df_all[~df_all["is_remote"]]["normalized_salary"]
print(f"Remote median: ${r.median():,.0f} (n={len(r)})")
print(f"Onsite median: ${o.median():,.0f} (n={len(o)})")
print(f"Premium: +{((r.median()/o.median())-1)*100:.1f}%")
