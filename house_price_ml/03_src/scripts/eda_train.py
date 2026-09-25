import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('01_data/splits/split_v1.csv')
train = df[df['split']=='train'].copy()
print("Train shape:", train.shape)

y = train['SalePrice']
print("\n--- SalePrice (train) ---")
print(y.describe())
print("Skew:", y.skew(), "| log1p skew:", np.log1p(y).skew())

num_cols = train.select_dtypes(include=[np.number]).columns.tolist()
for c in ['Id','SalePrice']:
    if c in num_cols: num_cols.remove(c)
cat_cols = train.select_dtypes(include=['object']).columns.tolist()

print("\n--- Missing (train only, top 10) ---")
miss = train.isnull().sum().sort_values(ascending=False)
miss = miss[miss>0]
print((miss/len(train)*100).round(1).head(10))

print("\n--- Top correlation with SalePrice (train only) ---")
corr = train[num_cols+['SalePrice']].corr()['SalePrice'].drop('SalePrice').sort_values(ascending=False)
print(corr.head(10))

print("\n--- Outlier scan (IQR, numeric, train only) ---")
outlier_counts = {}
for c in num_cols:
    q1,q3 = train[c].quantile([0.25,0.75])
    iqr = q3-q1
    if iqr==0: continue
    lo,hi = q1-3*iqr, q3+3*iqr
    n = ((train[c]<lo)|(train[c]>hi)).sum()
    if n>0: outlier_counts[c]=n
oc = pd.Series(outlier_counts).sort_values(ascending=False)
print(oc.head(10))

print("\n--- Rare categorical levels (<10 occurrences in train) ---")
rare_report = {}
for c in cat_cols:
    vc = train[c].value_counts(dropna=False)
    rare = vc[vc<10]
    if len(rare)>0:
        rare_report[c] = rare.to_dict()
for c,r in list(rare_report.items())[:8]:
    print(c, r)
print(f"... tong {len(rare_report)} cot categorical co it nhat 1 muc hiem (<10 mau)")

# Known GrLivArea outlier check (classic Ames issue)
susp = train[(train['GrLivArea']>4000)]
print(f"\nGrLivArea>4000 trong train: {len(susp)} dong, SalePrice tuong ung: {susp['SalePrice'].tolist()}")

# Plots
fig, axes = plt.subplots(2,2, figsize=(13,9))
axes[0,0].hist(y, bins=40, color='#4C72B0'); axes[0,0].set_title('SalePrice (train)')
axes[0,1].hist(np.log1p(y), bins=40, color='#55A868'); axes[0,1].set_title('log1p(SalePrice) (train)')
axes[1,0].scatter(train['GrLivArea'], y, alpha=0.4, s=12, color='#C44E52')
axes[1,0].set_xlabel('GrLivArea'); axes[1,0].set_ylabel('SalePrice'); axes[1,0].set_title('GrLivArea vs SalePrice (train)')
top10 = corr.head(10)[::-1]
axes[1,1].barh(top10.index, top10.values, color='#8172B2'); axes[1,1].set_title('Top tuong quan voi SalePrice (train)')
plt.tight_layout()
plt.savefig('02_notebooks/eda_train.png', dpi=130)
print("\nSaved 02_notebooks/eda_train.png")
