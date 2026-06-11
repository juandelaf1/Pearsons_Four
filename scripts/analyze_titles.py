"""Analyze job titles and create normalization mapping."""
import pandas as pd
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DF = BASE / 'data' / 'linkedin_data_roles_procesed.csv'

df = pd.read_csv(DF)

titles = df['title'].str.lower().str.strip()
counts = titles.value_counts()

print(f"Unique titles: {len(counts)}")
print(f"Total records: {len(df)}")
print("\n=== TOP 50 TITLES ===")
for title, count in counts.head(50).items():
    pct = count / len(df) * 100
    print(f"  {title:60s} | {count:4d} ({pct:4.1f}%)")

print(f"\n=== TAIL (titles appearing once) ===")
singletons = (counts == 1).sum()
print(f"Titles with 1 occurrence: {singletons} ({singletons/len(counts)*100:.1f}% of unique)")
under_3 = (counts < 3).sum()
print(f"Titles with <3 occurrences: {under_3} ({under_3/len(counts)*100:.1f}% of unique)")
under_5 = (counts < 5).sum()
print(f"Titles with <5 occurrences: {under_5} ({under_5/len(counts)*100:.1f}% of unique)")

print(f"\n=== COUNTS DISTRIBUTION ===")
print(f"  Mean:      {counts.mean():.1f}")
print(f"  Median:    {counts.median():.0f}")
print(f"  Max:       {counts.max()}")
print(f"  Top 1:     {counts.iloc[0]} ({counts.iloc[0]/len(df)*100:.1f}%)")
print(f"  Top 5:     {counts.iloc[:5].sum()} ({counts.iloc[:5].sum()/len(df)*100:.1f}%)")
print(f"  Top 10:    {counts.iloc[:10].sum()} ({counts.iloc[:10].sum()/len(df)*100:.1f}%)")
print(f"  Top 20:    {counts.iloc[:20].sum()} ({counts.iloc[:20].sum()/len(df)*100:.1f}%)")
