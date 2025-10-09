# plot_stage_scatter.py
import numpy as np
import matplotlib.pyplot as plt
import platform
import pandas as pd
from preprocessing_growth_level import df2  # df2가 이미 만들어진다고 가정

# =========================
# 💡 한글 폰트 깨짐 방지 (시작 부분에 배치)
# =========================
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')  # Windows: 맑은 고딕
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')    # macOS
else:
    plt.rc('font', family='NanumGothic')    # Linux/Colab 등
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# =========================
# --- 컬럼 설정 ---
# =========================
COL_OPE   = 'MCT_OPE_MS_CN_clean'   # x축
COL_SALES = 'RC_M1_SAA_clean'       # y축
STAGE_CANDIDATES = ['growth_level', '성장단계']

# 성장단계 컬럼 존재 확인
stage_cols = [c for c in STAGE_CANDIDATES if c in df2.columns]
if not stage_cols:
    raise KeyError(f"성장단계 컬럼이 없음. 후보 중 하나를 df2에 만들어줘: {STAGE_CANDIDATES}")
COL_STAGE = stage_cols[0]

# =========================
# --- 구간 순서 지정 ---
# =========================
ope_order   = ['10%이하', '10~25%', '25~50%', '50~75%', '75~90%', '90%초과']
sales_order = ['10%이하', '10~25%', '25~50%', '50~75%', '75~90%', '90%초과']

# =========================
# --- 구간 정규화 함수 ---
# =========================
def normalize_key(x):
    if pd.isna(x):
        return x
    s = str(x).replace(' ', '').replace('-', '~')
    if '(' in s:
        s = s.split('(')[0]
    if s.startswith('90%초과'):
        return '90%초과'
    if s in ['10~25', '25~50', '50~75', '75~90']:
        s += '%'
    return s

for c in [COL_OPE, COL_SALES]:
    if c not in df2.columns:
        raise KeyError(f"컬럼 없음: {c}  (preprocessing2.py에서 생성됐는지 확인)")

df2[COL_OPE]   = df2[COL_OPE].apply(normalize_key)
df2[COL_SALES] = df2[COL_SALES].apply(normalize_key)

# 유효 구간만 필터링
df2 = df2[df2[COL_OPE].isin(ope_order) & df2[COL_SALES].isin(sales_order)].copy()

# 좌표 매핑
x_map = {v: i for i, v in enumerate(ope_order)}
y_map = {v: i for i, v in enumerate(sales_order)}
df2['x'] = df2[COL_OPE].map(x_map)
df2['y'] = df2[COL_SALES].map(y_map)

# =========================
# --- 성장단계 라벨 통합 ---
# =========================
danger_alias = {
    '잠재형': '잠재형', 'Latent_type': '잠재형', 'latent_type': '잠재형', 'latent': '잠재형',
    '침체전조': '침체전조', 'recession': '침체전조', 'warning': '침체전조',
    '쇠퇴형': '쇠퇴형', 'decline': '쇠퇴형'
}
safe_set = set(['안정형','성장형','우량형','성숙안정형','성장안정형',
                'stable','growth','mature','premium','balanced','growth_stable','mature_stable'])

def stage_unify(v):
    if pd.isna(v):
        return '기타'
    s = str(v).strip()
    if s in danger_alias:
        return danger_alias[s]
    if s in safe_set:
        return '안전군'
    if s in ['잠재형','침체전조','쇠퇴형','안정형','성장형','우량형','성숙안정형','성장안정형']:
        return s
    return '기타'

df2['stage_unified'] = df2[COL_STAGE].apply(stage_unify)

# =========================
# --- 색상 맵 정의 ---
# =========================
color_map = {
    '잠재형':  '#FFD700',  # 노랑
    '침체전조':'#FFA500',  # 주황
    '쇠퇴형':  '#FF0000',  # 빨강
    '안전군':  '#1E90FF',  # 파랑
    '기타':    '#A9A9A9'   # 회색
}

# jitter (점 겹침 방지)
rng = np.random.default_rng(42)
df2['xj'] = df2['x'] + rng.uniform(-0.15, 0.15, len(df2))
df2['yj'] = df2['y'] + rng.uniform(-0.15, 0.15, len(df2))

# =========================
# --- 시각화 ---
# =========================
plt.figure(figsize=(9, 8))
for xi in range(len(ope_order)+1):
    plt.axvline(x=xi-0.5, color='lightgray', linewidth=0.8)
for yi in range(len(sales_order)+1):
    plt.axhline(y=yi-0.5, color='lightgray', linewidth=0.8)

# 순서: 안전군 먼저, 위험군 나중
draw_order = ['안전군', '잠재형', '침체전조', '쇠퇴형', '기타']
for lab in draw_order:
    sub = df2[df2['stage_unified'] == lab]
    if len(sub) == 0:
        continue
    plt.scatter(
        sub['xj'], sub['yj'], s=18,
        c=color_map[lab], alpha=0.8 if lab != '안전군' else 0.5,
        edgecolors='none', label=lab
    )

plt.xticks(range(len(ope_order)), ope_order, fontsize=11)
plt.yticks(range(len(sales_order)), sales_order, fontsize=11)
plt.gca().invert_yaxis()

plt.xlabel('운영개월수 구간', fontsize=13)
plt.ylabel('매출금액 구간', fontsize=13)
plt.title('가맹점 성장단계 분포 (위험군 vs 안전군)', fontsize=14)
plt.legend(title='성장단계', loc='upper right')
plt.tight_layout()
plt.show()
