import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
import os
from scipy import stats

sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)
out_dir = r'C:\Users\JUAN\Desktop\proyectos\Pearsons_Four\screenshots'
os.makedirs(out_dir, exist_ok=True)

# Load data
path = kagglehub.dataset_download('arshkon/linkedin-job-postings')
df = pd.read_csv(os.path.join(path, 'postings.csv'))

# Filter data roles
data_keywords = 'data scientist|data engineer|data analyst|machine learning|ml engineer|ai engineer|business intelligence|data architect|analytics|data manager'
df_data = df[df['title'].str.contains(data_keywords, case=False, na=False)].copy()
df_data['title'] = df_data['title'].str.lower().str.strip()
df_data['location'] = df_data['location'].str.lower().str.strip()

# Experience mapping
exp_map = {'internship': 0, 'entry level': 1, 'associate': 2, 'mid-senior level': 3, 'director': 4, 'executive': 5}
df_data['experience_level_num'] = df_data['formatted_experience_level'].str.lower().map(exp_map)

# Clean for stats
df_stats = df_data[(df_data['normalized_salary'] >= 1000) & (df_data['normalized_salary'] <= 2000000)].copy()
df_stats['is_remote'] = df_stats['remote_allowed'].fillna(0).astype(bool)

print(f'Data loaded: {len(df_data)} data roles, {len(df_stats)} with valid salaries')

# === GRAPH 1: Boxplot ===
plt.figure(figsize=(12, 6))
exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
sns.boxplot(data=df_stats, x='formatted_experience_level', y='normalized_salary', order=exp_order, palette='Set2')
plt.title('Salary Spread by Experience Level', fontsize=14, fontweight='bold')
plt.xlabel('Experience Level', fontsize=12)
plt.ylabel('Normalized Yearly Salary (USD)', fontsize=12)
plt.ylim(0, 500000)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_boxplot_experience.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 1: Boxplot saved')

# === GRAPH 2: Histogram + KDE ===
plt.figure(figsize=(10, 6))
sns.histplot(data=df_stats, x='normalized_salary', kde=True, bins=40, color='teal')
plt.title('Distribution of Data Role Salaries (with KDE)', fontsize=14, fontweight='bold')
plt.xlabel('Normalized Yearly Salary (USD)', fontsize=12)
plt.ylabel('Number of Job Postings', fontsize=12)
plt.xlim(0, 400000)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_histogram_kde.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 2: Histogram saved')

# === GRAPH 3: Salary Spread ===
plt.figure(figsize=(10, 6))
sal = df_stats['normalized_salary'].dropna()
plt.subplot(1, 2, 1)
plt.boxplot(sal, vert=False)
plt.title('Salary Distribution (Boxplot)')
plt.xlabel('Salary (USD)')
plt.subplot(1, 2, 2)
plt.hist(sal, bins=30, color='teal', edgecolor='white')
plt.title('Salary Distribution (Histogram)')
plt.xlabel('Salary (USD)')
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_salary_spread.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 3: Salary spread saved')

# === GRAPH 4: Top 10 Roles ===
plt.figure(figsize=(10, 6))
top_titles = df_data['title'].value_counts().head(10)
sns.barplot(x=top_titles.values, y=top_titles.index, palette='viridis')
plt.title('Top 10 Most Frequent Data Roles', fontsize=14, fontweight='bold')
plt.xlabel('Number of Postings', fontsize=12)
plt.ylabel('Job Title', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_top_roles.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 4: Top roles saved')

# === GRAPH 5: Views vs Applies ===
plt.figure(figsize=(8, 6))
from scipy.stats import pearsonr
r, p = pearsonr(df_stats['views'], df_stats['applies'])
sns.scatterplot(data=df_stats, x='views', y='applies', alpha=0.6, color='coral')
sns.regplot(data=df_stats, x='views', y='applies', scatter=False, color='darkred')
plt.title(f'Correlation: Job Views vs Applications (r = {r:.2f})', fontsize=14, fontweight='bold')
plt.xlabel('Number of Views', fontsize=12)
plt.ylabel('Number of Applications', fontsize=12)
plt.xlim(0, 1000)
plt.ylim(0, 200)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_views_vs_applies.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 5: Views vs Applies saved')

# === GRAPH 6: Line graph - Salary progression ===
exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
exp_medians = df_stats.groupby('formatted_experience_level')['normalized_salary'].median()
exp_medians = exp_medians.reindex(exp_order)
plt.figure(figsize=(10, 6))
plt.plot(range(len(exp_medians)), exp_medians.values, 'bo-', linewidth=2.5, markersize=10)
for i, v in enumerate(exp_medians.values):
    plt.text(i, v + 5000, f'${v:,.0f}', ha='center', fontsize=11, fontweight='bold')
plt.xticks(range(len(exp_medians)), exp_medians.index, fontsize=11)
plt.ylabel('Median Salary (USD)', fontsize=12)
plt.title('Salary Progression by Experience Level', fontsize=14, fontweight='bold')
plt.ylim(0, exp_medians.max() * 1.2)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_salary_progression.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 6: Line progression saved')

# === GRAPH 7: CDF ===
sal_sorted = np.sort(df_stats['normalized_salary'].dropna())
cdf = np.arange(1, len(sal_sorted) + 1) / len(sal_sorted)
plt.figure(figsize=(10, 6))
plt.plot(sal_sorted, cdf, 'b-', linewidth=2)
plt.axhline(y=0.25, color='r', linestyle='--', alpha=0.5, label='Q1')
plt.axhline(y=0.5, color='g', linestyle='--', alpha=0.5, label='Median (Q2)')
plt.axhline(y=0.75, color='orange', linestyle='--', alpha=0.5, label='Q3')
plt.axvline(x=np.median(sal_sorted), color='g', linestyle='--', alpha=0.3)
plt.text(np.median(sal_sorted) + 2000, 0.02, f'Median=${np.median(sal_sorted):,.0f}', fontsize=10, color='green', fontweight='bold')
plt.xlabel('Salary (USD)', fontsize=12)
plt.ylabel('Cumulative Probability', fontsize=12)
plt.title('Cumulative Distribution Function (CDF) of Data Salaries', fontsize=14, fontweight='bold')
plt.legend()
plt.xlim(0, 400000)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_salary_cdf.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 7: CDF saved')

# === GRAPH 8: Remote Premium comparison ===
remote_comp = df_stats.groupby('is_remote')['normalized_salary'].median()
plt.figure(figsize=(8, 6))
vals = [remote_comp.get(False, 0), remote_comp.get(True, 0)]
bars = plt.bar(['On-Site', 'Remote'], vals, color=['#e74c3c', '#2ecc71'], width=0.5)
plt.text(0, vals[0] + 2000, f'${vals[0]:,.0f}', ha='center', fontsize=12, fontweight='bold')
plt.text(1, vals[1] + 2000, f'${vals[1]:,.0f}', ha='center', fontsize=12, fontweight='bold')
premium = ((vals[1] / vals[0]) - 1) * 100 if vals[0] > 0 else 0
plt.title(f'Remote Work Premium: +{premium:.1f}%', fontsize=14, fontweight='bold')
plt.ylabel('Median Salary (USD)', fontsize=12)
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'linkedin_remote_premium.png'), dpi=150, bbox_inches='tight')
plt.close()
print('Graph 8: Remote premium saved')

print(f'\nAll graphs saved to {out_dir}')
print(f'Files: {os.listdir(out_dir)}')
