import matplotlib.pyplot as plt
from processing_growth_level import df2
import platform

# 한글 폰트 깨짐 방지
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 준비
COL_STAGE = '성장단계'

# 성장 단계별 순서 지정 (보고서/시각적으로 깔끔하게)
stage_order = [
    '성장형', '잠재형', '초기안정형', '성장안정형',
    '안정형', '침체전조', '성숙안정형', '우량형', '쇠퇴형'
]

# 단계별 가맹점 수 계산
stage_counts = df2[COL_STAGE].value_counts().reindex(stage_order, fill_value=0)

# 2. 색상 매핑
color_map = {
    '성장형': '#5DADE2',      # 파랑톤 (성장)
    '잠재형': '#85C1E9',      # 옅은 파랑
    '초기안정형': '#85C1E9',  # 옅은 파랑
    '성장안정형': '#3498DB',  # 진한 파랑
    '안정형': '#1E90FF',      # 표준 블루
    '침체전조': '#FFA500',    # 주황
    '성숙안정형': '#2E86C1',  # 중간 파랑
    '우량형': '#2874A6',      # 진파랑
    '쇠퇴형': '#FF0000',      # 빨강
}

bar_colors = [color_map.get(stage, '#A9A9A9') for stage in stage_order]

# 3. 막대 그래프 시각화
plt.figure(figsize=(10, 6))
plt.bar(stage_order, stage_counts, color=bar_colors, edgecolor='black', alpha=0.85)

# 수치 라벨 표시
for i, v in enumerate(stage_counts):
    plt.text(i, v + (max(stage_counts) * 0.01), str(v), ha='center', va='bottom', fontsize=10)

# 축 / 제목 설정
plt.xlabel('Growth Stage', fontsize=12)
plt.ylabel('Number of Stores', fontsize=12)
plt.title('Number of Stores by Growth Stage', fontsize=14, fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
