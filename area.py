import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 데이터 로드 및 병합 ---
df1 = pd.read_csv("big_data_set1_f.csv", encoding='cp949')
df3 = pd.read_csv("big_data_set3_f.csv", encoding='cp949')
merged_df = pd.merge(df1, df3, on='ENCODED_MCT', how='inner')

# --- 2. 결측치 처리 ---
ratio_cols_to_clean = [
    'RC_M1_SHC_RSD_UE_CLN_RAT', # 거주고객 비율
    'RC_M1_SHC_WP_UE_CLN_RAT',  # 직장이용 비율
    'RC_M1_SHC_FLP_UE_CLN_RAT'  # 유동인구 비율
]

for col in ratio_cols_to_clean:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

SPECIAL_MISSING_VALUE = -999999.9
merged_df[ratio_cols_to_clean] = merged_df[ratio_cols_to_clean].replace(SPECIAL_MISSING_VALUE, np.nan)
merged_df.dropna(subset=ratio_cols_to_clean, inplace=True)

# --- 3. 오분류 외부 지역 제거 ---
bad_regions = [
    '미아사거리', '방배역', '서면역', '오남', '풍산지구', '동대문역사문화공원역',
    '압구정로데오', '답십리', '장한평자동차', '건대입구', '자양', '화양시장'
]
merged_df = merged_df[~merged_df['HPSN_MCT_BZN_CD_NM'].isin(bad_regions)]

# --- 4. 지역별 그룹화 및 평균 계산 ---
grouping_col = 'HPSN_MCT_BZN_CD_NM'
region_analysis = merged_df.groupby(grouping_col)[ratio_cols_to_clean].mean().round(2)
region_analysis_sorted = region_analysis.sort_values(by='RC_M1_SHC_RSD_UE_CLN_RAT', ascending=False)

# 콘솔 출력
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', None)
print(region_analysis_sorted)

# --- 5. 시각화 (Stacked Bar Chart) ---
plt.rcParams['font.family'] = 'Malgun Gothic'
fig, ax = plt.subplots(figsize=(14, 7))

# 상위 10개 지역만 시각화
top_n = 10
plot_data = region_analysis_sorted.head(top_n)

# 스택형 막대 생성
plot_data.plot(kind='bar', stacked=True, ax=ax, width=0.8)

# 제목과 레이블 설정
ax.set_title('상위 10개 지역별 고객 비율', fontsize=16)
ax.set_xlabel('지역')
ax.set_ylabel('평균 고객 비율 (%)')
ax.legend(title='고객 유형')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top10_region_customer_ratio.png')
plt.show()
