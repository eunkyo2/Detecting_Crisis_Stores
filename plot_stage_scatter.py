import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform

# 1. CSV 로드 (성장단계 포함된 파일 사용)
df = pd.read_csv("big_data_set2_f_stage.csv", encoding="cp949")

# 2. 폰트 설정 (한글 깨짐 방지)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 3. 주요 컬럼 지정
X_COL = 'MCT_OPE_MS_CN_rank_mean'  # 운영개월 평균
Y_COL = 'RC_M1_SAA_rank_mean'      # 매출금액 평균
STAGE_COL = '성장단계'              # 성장단계

# 4. 데이터 정리
df = df.dropna(subset=[X_COL, Y_COL])
df[X_COL] = pd.to_numeric(df[X_COL], errors='coerce')
df[Y_COL] = pd.to_numeric(df[Y_COL], errors='coerce')

# jitter 추가 (점 겹침 방지)
rng = np.random.default_rng(42)
df['xj'] = df[X_COL] + rng.uniform(-0.05, 0.05, len(df))
df['yj'] = df[Y_COL] + rng.uniform(-0.05, 0.05, len(df))

# 5. 색상 구분
def get_color(stage):
    if stage == '쇠퇴형':
        return '#FF0000'  # 빨강
    elif stage in ['침체전조', '침제전조']:
        return '#FFA500'  # 주황
    else:
        return '#1E90FF'  # 파랑

df['color'] = df[STAGE_COL].apply(get_color)

# 6. 산점도 시각화
plt.figure(figsize=(8, 6))
plt.scatter(df['xj'], df['yj'], s=20, alpha=0.7, c=df['color'], edgecolors='none')

plt.xlabel('운영개월 평균 등급 (MCT_OPE_MS_CN_rank_mean)', fontsize=12)
plt.ylabel('매출금액 평균 등급 (RC_M1_SAA_rank_mean)', fontsize=12)
plt.title('가맹점 운영개월 vs 매출 등급 평균 분포 (쇠퇴·침체전조 구분)', fontsize=14)

plt.xticks(range(1, 7))
plt.yticks(range(1, 7))
plt.grid(alpha=0.3)

# 범례 수동 추가
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='쇠퇴형', markerfacecolor='#FF0000', markersize=6),
    Line2D([0], [0], marker='o', color='w', label='침체전조', markerfacecolor='#FFA500', markersize=6),
    Line2D([0], [0], marker='o', color='w', label='기타', markerfacecolor='#1E90FF', markersize=6)
]
plt.legend(handles=legend_elements, title='성장단계', loc='upper right')

plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform

# 1. CSV 로드 (성장단계 포함된 파일 사용)
df = pd.read_csv("big_data_set2_f_stage.csv", encoding="cp949")

# 2. 폰트 설정 (한글 깨짐 방지)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 3. 주요 컬럼 지정
X_COL = 'MCT_OPE_MS_CN_rank_mean'  # 운영개월 평균
Y_COL = 'RC_M1_SAA_rank_mean'      # 매출금액 평균
STAGE_COL = '성장단계'              # 성장단계

# 4. 데이터 정리
df = df.dropna(subset=[X_COL, Y_COL])
df[X_COL] = pd.to_numeric(df[X_COL], errors='coerce')
df[Y_COL] = pd.to_numeric(df[Y_COL], errors='coerce')

# jitter 추가 (점 겹침 방지)
rng = np.random.default_rng(42)
df['xj'] = df[X_COL] + rng.uniform(-0.05, 0.05, len(df))
df['yj'] = df[Y_COL] + rng.uniform(-0.05, 0.05, len(df))

# 5. 색상 구분
def get_color(stage):
    if stage == '쇠퇴형':
        return '#FF0000'  # 빨강
    elif stage in ['침체전조', '침체전조']:
        return '#FFA500'  # 주황
    else:
        return '#1E90FF'  # 파랑

df['color'] = df[STAGE_COL].apply(get_color)

# 6. 산점도 시각화
plt.figure(figsize=(8, 6))
plt.scatter(df['xj'], df['yj'], s=20, alpha=0.7, c=df['color'], edgecolors='none')

plt.xlabel('운영개월 평균 등급 (MCT_OPE_MS_CN_rank_mean)', fontsize=12)
plt.ylabel('매출금액 평균 등급 (RC_M1_SAA_rank_mean)', fontsize=12)
plt.title('가맹점 운영개월 vs 매출 등급 평균 분포 (쇠퇴·침체전조 구분)', fontsize=14)

plt.xticks(range(1, 7))
plt.yticks(range(1, 7))
plt.grid(alpha=0.3)

# 범례 수동 추가
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='쇠퇴형', markerfacecolor='#FF0000', markersize=6),
    Line2D([0], [0], marker='o', color='w', label='침체전조', markerfacecolor='#FFA500', markersize=6),
    Line2D([0], [0], marker='o', color='w', label='기타', markerfacecolor='#1E90FF', markersize=6)
]
plt.legend(handles=legend_elements, title='성장단계', loc='upper right')

plt.tight_layout()
plt.show()
