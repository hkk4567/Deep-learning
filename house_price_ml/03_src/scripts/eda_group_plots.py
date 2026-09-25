import pandas as pd, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

df = pd.read_csv('01_data/splits/split_v1_selected_features.csv')
train = df[df['split']=='train'].copy()
y = train['SalePrice']

groups = {
 "N1_KhuDat": ["MSSubClass","MSZoning","LotFrontage","LotArea","Street","Alley","LotShape","LandContour","Utilities","LotConfig","LandSlope"],
 "N2_ViTri": ["Neighborhood","Condition1","Condition2"],
 "N3_ChatLuongNha": ["BldgType","HouseStyle","OverallQual","OverallCond","YearBuilt","YearRemodAdd","RoofStyle","RoofMatl","Exterior1st","Exterior2nd","MasVnrType","MasVnrArea","ExterQual","ExterCond","Foundation"],
 "N4_MongTangHam": ["BsmtQual","BsmtCond","BsmtExposure","BsmtFinType1","BsmtFinSF1","BsmtFinType2","BsmtFinSF2","BsmtUnfSF","TotalBsmtSF","BsmtFullBath","BsmtHalfBath"],
 "N5_HeThong": ["Heating","HeatingQC","CentralAir","Electrical"],
 "N6_DienTichSinhHoat": ["1stFlrSF","2ndFlrSF","LowQualFinSF","GrLivArea","FullBath","HalfBath","BedroomAbvGr","KitchenAbvGr","KitchenQual","TotRmsAbvGrd","Functional"],
 "N7_Garage": ["GarageType","GarageYrBlt","GarageFinish","GarageCars","GarageArea","GarageQual","GarageCond"],
 "N8_DuongVao": ["PavedDrive"],
 "N9_GiaoDich": ["MoSold","YrSold","SaleType","SaleCondition"],
}

def plot_group(name, cols):
    n = len(cols)
    ncols = 3 if n>1 else 1
    nrows = math.ceil(n/ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(5.2*ncols, 4*nrows))
    axes = np.array(axes).reshape(-1) if n>1 else [axes]
    for i, c in enumerate(cols):
        ax = axes[i]
        s = train[c]
        if s.dtype.kind in 'if':
            ax.scatter(s, y, alpha=0.35, s=10, color='#4C72B0')
            corr = s.corr(y)
            ax.set_title(f"{c} (corr={corr:.2f})", fontsize=10)
            ax.set_xlabel(c, fontsize=8)
        else:
            d = pd.DataFrame({'c': s.astype('object').fillna('NA'), 'y': y})
            order = d.groupby('c')['y'].median().sort_values().index
            data = [d[d['c']==lvl]['y'].values for lvl in order]
            ax.boxplot(data, labels=order, showfliers=False)
            ax.set_title(c, fontsize=10)
            ax.tick_params(axis='x', rotation=60, labelsize=7)
        ax.set_ylabel('SalePrice', fontsize=8)
        ax.tick_params(axis='y', labelsize=7)
    for j in range(n, len(axes)):
        axes[j].axis('off')
    fig.suptitle(name, fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0,0,1,0.97])
    out = f"06_reports/eda/eda_plots/by_group/{name}.png"
    plt.savefig(out, dpi=120)
    plt.close(fig)
    print("Saved", out)

for name, cols in groups.items():
    plot_group(name, cols)
