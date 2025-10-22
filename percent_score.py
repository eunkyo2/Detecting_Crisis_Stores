import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# CSV 불러오기
df = pd.read_csv('big_data_set2_f_na.csv', encoding='cp949')

# qcut으로 3단계 버킷 계산 (각 구간에 가맹점 수 균등)
df['SAA_bucket'] = pd.qcut(df['M1_SME_RY_SAA_RAT_mean'], q=3, labels=['small','mid','many'])
df['CNT_bucket'] = pd.qcut(df['M1_SME_RY_CNT_RAT_mean'], q=3, labels=['low','mid','top'])

# 6단계 성장단계 맵핑 (최대 15점 기준)
stage_map = {
    ('low', 'small'): '쇠퇴형',
    ('low', 'mid'): '초기안정형',
    ('low', 'many'): '초기안정형',
    ('mid', 'small'): '잠재형',
    ('mid', 'mid'): '안정형',
    ('mid', 'many'): '성장형',
    ('top', 'small'): '잠재형',
    ('top', 'mid'): '성장형',
    ('top', 'many'): '우량형'
}

score_map = {
    '쇠퇴형': 15,
    '잠재형': 12,
    '초기안정형': 9,
    '안정형': 6,
    '성장형': 3,
    '우량형': 1
}

df['성장단계'] = df.apply(lambda row: stage_map.get((row['CNT_bucket'], row['SAA_bucket']), None), axis=1)
df['성장점수'] = df['성장단계'].map(score_map)

# 6️⃣ 결과 확인
print(df[['ENCODED_MCT', 'CNT_bucket', 'SAA_bucket', '성장단계', '성장점수']].head(15))

print("\n성장단계 분포:")
print(df['성장단계'].value_counts())

# 7️⃣ CSV 저장
df.to_csv('big_data_set2_f_score.csv', index=False, encoding='cp949')
print("\n✅ 6단계 성장단계(최대 15점) 저장 완료: big_data_set2_f_score.csv")

# 1️⃣ 한글 폰트 설정 (Windows용)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 2️⃣ 성장단계 막대그래프
plt.figure(figsize=(10,6))
sns.countplot(
    data=df,
    x='성장단계',
    order=['쇠퇴형','잠재형','초기안정형','안정형','성장형','우량형'],
    palette='coolwarm'
)
plt.title('6단계 성장단계 분포', fontsize=16)
plt.xlabel('성장단계', fontsize=12)
plt.ylabel('가맹점 수', fontsize=12)
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()