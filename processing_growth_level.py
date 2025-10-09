import pandas as pd

# 1. CSV 로드 (평균 등급 파일)
df2 = pd.read_csv("big_data_set2_f_mean.csv", encoding="cp949")

# 2. 평균 등급을 랭크로 사용
df2['ope_rank']   = pd.to_numeric(df2['MCT_OPE_MS_CN_rank_mean'], errors='coerce')
df2['sales_rank'] = pd.to_numeric(df2['RC_M1_SAA_rank_mean'], errors='coerce')

# 3. 6단계 → 3단계 버킷 함수 정의
def bucket_3_from_6(rank):
    if pd.isna(rank):
        return None
    rank = float(rank)
    if rank <= 2:       # 1~2
        return 'top'    # 상
    elif rank <= 4:     # 3~4
        return 'mid'    # 중
    else:               # 5~6
        return 'low'    # 하

def bucket_ope(rank):
    if pd.isna(rank):
        return None
    rank = float(rank)
    if rank <= 2:
        return 'short'  # 짧음
    elif rank <= 4:
        return 'mid'    # 중간
    else:
        return 'long'   # 길음

# 4. 버킷 계산
df2['ope_bucket']   = df2['ope_rank'].apply(bucket_ope)
df2['sales_bucket'] = df2['sales_rank'].apply(bucket_3_from_6)

# 5. 성장단계 분류 함수
def classify_stage_soft(row):
    ope_b   = row['ope_bucket']
    sales_b = row['sales_bucket']
    o_rank  = row['ope_rank']
    s_rank  = row['sales_rank']

    # 성장형
    if (ope_b == 'short' and sales_b == 'top') or \
       (ope_b == 'short' and not pd.isna(s_rank) and s_rank <= 3) or \
       (not pd.isna(o_rank) and o_rank <= 3 and sales_b == 'top'):
        return '성장형'

    # 잠재형
    if (ope_b == 'short' and sales_b == 'low') or \
       (ope_b == 'short' and not pd.isna(s_rank) and s_rank >= 4) or \
       (not pd.isna(o_rank) and o_rank <= 3 and sales_b == 'low'):
        return '잠재형'

    # 우량형
    if (ope_b == 'long' and sales_b == 'top') or \
       (ope_b == 'long' and not pd.isna(s_rank) and s_rank <= 3):
        return '우량형'

    # 쇠퇴형
    if (ope_b == 'long' and sales_b == 'low') or \
       (ope_b == 'long' and not pd.isna(s_rank) and s_rank >= 5):
        return '쇠퇴형'

    # 중간대 조합 (3×3 그리드)
    if ope_b == 'short' and sales_b == 'mid': return '초기안정형'
    if ope_b == 'mid'   and sales_b == 'top': return '성장안정형'
    if ope_b == 'mid'   and sales_b == 'mid': return '안정형'
    if ope_b == 'mid'   and sales_b == 'low': return '침체전조'
    if ope_b == 'long'  and sales_b == 'mid': return '성숙안정형'

    return '안정형'

# 6. 성장단계 적용
df2['성장단계'] = df2.apply(classify_stage_soft, axis=1)

# 7. 결과 확인
print(df2[['ENCODED_MCT',
           'MCT_OPE_MS_CN_rank_mean','RC_M1_SAA_rank_mean',
           'ope_rank','sales_rank','ope_bucket','sales_bucket','성장단계']].head(12))

print("\n성장단계 분포:")
print(df2['성장단계'].value_counts(dropna=False))

# 8. 결과 저장
df2.to_csv("big_data_set2_f_stage.csv", index=False, encoding='cp949')
print("\n 성장단계 결과 저장 완료: big_data_set2_f_stage.csv")
