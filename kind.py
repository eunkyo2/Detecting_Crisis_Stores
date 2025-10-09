import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 데이터 로드 및 병합 ---
df1 = pd.read_csv("big_data_set1_f.csv", encoding='cp949')
df3 = pd.read_csv("big_data_set3_f.csv", encoding='cp949')
merged_df = pd.merge(df1, df3, on='ENCODED_MCT', how='inner')

# --- 2. 결측치 및 오분류 데이터 처리 ---
ratio_cols_to_clean = [
    'RC_M1_SHC_RSD_UE_CLN_RAT', 'RC_M1_SHC_WP_UE_CLN_RAT', 'RC_M1_SHC_FLP_UE_CLN_RAT'
]
bzn_col = 'HPSN_MCT_BZN_CD_NM'
zcd_col = 'HPSN_MCT_ZCD_NM'

# 특수값 -999999.9를 NaN으로 변환
for col in ratio_cols_to_clean:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
SPECIAL_MISSING_VALUE = -999999.9
merged_df[ratio_cols_to_clean] = merged_df[ratio_cols_to_clean].replace(SPECIAL_MISSING_VALUE, np.nan)

# Step 2: 업종명 결측치 제거
merged_df.dropna(subset=[bzn_col], inplace=True)
# Step 1: 비율 데이터 없는 행 제거
merged_df.dropna(subset=ratio_cols_to_clean, inplace=True)
# Step 3: 오분류 외부 지역 제거
bad_regions = [
    '미아사거리', '방배역', '서면역', '오남', '풍산지구', '동대문역사문화공원역',
    '압구정로데오', '답십리', '장한평자동차', '건대입구', '자양', '화양시장'
]
merged_df = merged_df[~merged_df[bzn_col].isin(bad_regions)]

# --- 3. 업종별 평균 계산 ---
industry_analysis = merged_df.groupby(zcd_col)[ratio_cols_to_clean].mean().round(2)
analysis_sorted = industry_analysis.sort_values(by='RC_M1_SHC_RSD_UE_CLN_RAT', ascending=False)

# --- 4. 시각화 ---
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)

plt.rcParams['font.family'] = 'Malgun Gothic'
fig, ax = plt.subplots(figsize=(12, 6))

# 상위 10개 업종만 시각화
top_n = 10
plot_data = analysis_sorted.head(top_n)
plot_data.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('업종 대분류별 평균 고객 비율', fontsize=16)
ax.set_xlabel('업종 대분류')
ax.set_ylabel('평균 고객 비율 (%)')
ax.legend(title='고객 유형')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('industry_customer_ratio_top10.png')
plt.show()
