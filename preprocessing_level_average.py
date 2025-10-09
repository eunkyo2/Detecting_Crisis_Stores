import pandas as pd
import re

# 1. CSV 불러오기
df2 = pd.read_csv("big_data_set2_f.csv", encoding="cp949")

# 2. 문자열 정리 함수
def clean_bucket(s: str) -> str:
    s = str(s).strip()
    s = re.sub(r'^\d+_', '', s)
    s = s.replace(' ', '')
    return s

def normalize_key(s: str) -> str:
    s = str(s).replace(' ', '').replace('-', '~')
    s = re.sub(r'\(.*?\)', '', s)
    base = {'10%이하','10~25%','25~50%','50~75%','75~90%','90%초과'}
    if s in base:
        return s
    m = re.match(r'^(10|25|50|75)~(25|50|75|90)%$', s)
    if m:
        a, b = m.groups()
        return f'{a}~{b}%'
    if s.startswith('90%초과'):
        return '90%초과'
    if s in ['10%이하','10이하','≤10%','<=10%']:
        return '10%이하'
    m2 = re.match(r'^(10|25|50|75)~(25|50|75|90)$', s)
    if m2:
        a, b = m2.groups()
        return f'{a}~{b}%'
    for k in ['10%이하','10~25%','25~50%','50~75%','75~90%','90%초과']:
        if k.replace('%','') in s.replace('%',''):
            return k
    return s

# 3. 정제
df2['MCT_OPE_MS_CN_clean'] = df2['MCT_OPE_MS_CN'].apply(clean_bucket).apply(normalize_key)
df2['RC_M1_SAA_clean']     = df2['RC_M1_SAA'].apply(clean_bucket).apply(normalize_key)

# 4. 등급 매핑 (공통 사용)
rank_map = {
    '10%이하': 1,
    '10~25%': 2,
    '25~50%': 3,
    '50~75%': 4,
    '75~90%': 5,
    '90%초과': 6
}

df2['MCT_OPE_MS_CN_rank'] = df2['MCT_OPE_MS_CN_clean'].map(rank_map)
df2['RC_M1_SAA_rank']     = df2['RC_M1_SAA_clean'].map(rank_map)

# 5. ENCODED_MCT 기준 평균 계산 (두 컬럼 모두)
mean_rank_df = (
    df2.groupby('ENCODED_MCT', as_index=False)
       .agg({
           'MCT_OPE_MS_CN_rank': 'mean',   # 운영개월 등급 평균
           'RC_M1_SAA_rank': 'mean'        # 매출금액구간 등급 평균
       })
       .rename(columns={
           'MCT_OPE_MS_CN_rank': 'MCT_OPE_MS_CN_rank_mean',
           'RC_M1_SAA_rank': 'RC_M1_SAA_rank_mean'
       })
)

# 6. 결과 확인 및 저장
print(mean_rank_df.head(20))
mean_rank_df.to_csv("big_data_set2_f_mean.csv", index=False, encoding='cp949')
print("평균 등급 저장 완료: big_data_set2_f_mean.csv")
