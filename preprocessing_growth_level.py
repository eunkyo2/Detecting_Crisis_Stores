import pandas as pd
import re

# 1. CSV 로드 (윈도우 한글 인코딩 대비)
df2 = pd.read_csv("big_data_set2_f.csv", encoding="cp949")

# 2. 구간 문자열 정리: 앞의 숫자_ 제거 + 공백 제거
def clean_bucket(s: str) -> str:
    s = str(s)
    s = s.strip()
    s = re.sub(r'^\d+_', '', s)
    s = s.replace(' ', '')
    return s

df2['MCT_OPE_MS_CN_clean'] = df2['MCT_OPE_MS_CN'].apply(clean_bucket)
df2['RC_M1_SAA_clean']     = df2['RC_M1_SAA'].apply(clean_bucket)

# 3. 다양한 표기 통합 정규화
#   - 하이픈(-)을 물결(~)로 통일
#   - '90%초과(하위10%이하)' 같은 꼬리표 제거 → '90%초과'
#   - '10 ~ 25 %' 등도 흡수
def normalize_key(s: str) -> str:
    s = str(s)
    s = s.replace(' ', '')
    s = s.replace('-', '~')  # 25-50% → 25~50%
    # 괄호/설명 꼬리 제거
    s = re.sub(r'\(.*?\)', '', s)  # 90%초과(하위10%이하) → 90%초과
    # 대표 케이스로 매핑
    # 첫번째 완전 일치 케이스
    base = {'10%이하','10~25%','25~50%','50~75%','75~90%','90%초과'}
    if s in base:
        return s
    # 숫자~숫자% 패턴 흡수 (예: 10~25%, 25~50% 등)
    m = re.match(r'^(10|25|50|75)~(25|50|75|90)%$', s)
    if m:
        a, b = m.groups()
        return f'{a}~{b}%'
    # 경계형들 흡수
    if s.startswith('90%초과'):
        return '90%초과'
    if s in ['10%이하','10이하','≤10%','<=10%']:
        return '10%이하'
    # 혹시 '75~90' 처럼 % 빠진 경우
    m2 = re.match(r'^(10|25|50|75)~(25|50|75|90)$', s)
    if m2:
        a, b = m2.groups()
        return f'{a}~{b}%'
    # 대표 셋 중 포함되는 텍스트 찾아 매핑
    for k in ['10%이하','10~25%','25~50%','50~75%','75~90%','90%초과']:
        if k.replace('%','') in s.replace('%',''):
            return k
    return s

df2['MCT_OPE_MS_CN_clean'] = df2['MCT_OPE_MS_CN_clean'].apply(normalize_key)
df2['RC_M1_SAA_clean']     = df2['RC_M1_SAA_clean'].apply(normalize_key)

# 4. 순위 매핑 (작을수록 상위/좋음)
rank_map = {
    '10%이하': 1,
    '10~25%': 2,
    '25~50%': 3,
    '50~75%': 4,
    '75~90%': 5,
    '90%초과': 6
}

df2['ope_rank']   = df2['MCT_OPE_MS_CN_clean'].map(rank_map)
df2['sales_rank'] = df2['RC_M1_SAA_clean'].map(rank_map)

# 5. 3×3 버킷 (rank None이면 None 유지: 뒤에서 보정)
def bucket_3_from_6(rank):
    if pd.isna(rank):
        return None
    rank = int(rank)
    if rank <= 2:       # 1~2
        return 'top'    # 상
    elif rank <= 4:     # 3~4
        return 'mid'    # 중
    else:               # 5~6
        return 'low'    # 하

def bucket_ope(rank):
    if pd.isna(rank):
        return None
    rank = int(rank)
    if rank <= 2:
        return 'short'  # 짧음
    elif rank <= 4:
        return 'mid'    # 중간
    else:
        return 'long'   # 길음

df2['ope_bucket']   = df2['ope_rank'].apply(bucket_ope)           # short/mid/long
df2['sales_bucket'] = df2['sales_rank'].apply(bucket_3_from_6)    # top/mid/low

# 6. 성장 단계 맵핑 (완화 기준 + 기본값 안정형)
def _bucket_from_rank(rank, kind):
    if pd.isna(rank):
        return None
    r = int(rank)
    if kind == 'ope':  # short/mid/long
        if r <= 2:  return 'short'
        elif r <= 4:return 'mid'
        else:       return 'long'
    else:             # top/mid/low
        if r <= 2:  return 'top'
        elif r <= 4:return 'mid'
        else:       return 'low'

def classify_stage_soft(row):
    # 버킷 None이면 rank 기반 보정
    ope_b   = row['ope_bucket']   if row['ope_bucket']   is not None else _bucket_from_rank(row['ope_rank'],   'ope')
    sales_b = row['sales_bucket'] if row['sales_bucket'] is not None else _bucket_from_rank(row['sales_rank'], 'sales')
    o_rank  = row['ope_rank']
    s_rank  = row['sales_rank']

    # 극단부(완화) — 성장형/잠재형/우량형/쇠퇴형
    # 성장형: 초기(짧음) & 매출 상~중상
    if (ope_b == 'short' and sales_b == 'top') or \
       (ope_b == 'short' and not pd.isna(s_rank) and s_rank <= 3) or \
       (not pd.isna(o_rank) and o_rank <= 3 and sales_b == 'top'):
        return '성장형'

    # 잠재형: 초기(짧음) & 매출 중하~하
    if (ope_b == 'short' and sales_b == 'low') or \
       (ope_b == 'short' and not pd.isna(s_rank) and s_rank >= 4) or \
       (not pd.isna(o_rank) and o_rank <= 3 and sales_b == 'low'):
        return '잠재형'

    # 우량형: 장기(길음) & 매출 상~중상
    if (ope_b == 'long' and sales_b == 'top') or \
       (ope_b == 'long' and not pd.isna(s_rank) and s_rank <= 3):
        return '우량형'

    # 쇠퇴형: 장기(길음) & 매출 중하~하
    if (ope_b == 'long' and sales_b == 'low') or \
       (ope_b == 'long' and not pd.isna(s_rank) and s_rank >= 5):
        return '쇠퇴형'

    # 중간대 조합(3×3 그리드)
    if ope_b == 'short' and sales_b == 'mid': return '초기안정형'
    if ope_b == 'mid'   and sales_b == 'top': return '성장안정형'
    if ope_b == 'mid'   and sales_b == 'mid': return '안정형'
    if ope_b == 'mid'   and sales_b == 'low': return '침체전조'
    if ope_b == 'long'  and sales_b == 'mid': return '성숙안정형'

    # 기본값을 '안정형'으로 떨어뜨려 기타 최소화
    return '안정형'

df2['성장단계'] = df2.apply(classify_stage_soft, axis=1)

# 7. 결과 확인
print(df2[['MCT_OPE_MS_CN','RC_M1_SAA',
           'MCT_OPE_MS_CN_clean','RC_M1_SAA_clean',
           'ope_rank','sales_rank','ope_bucket','sales_bucket','성장단계']].head(12))

print("\n성장단계 분포:")
print(df2['성장단계'].value_counts(dropna=False))
