import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드 
df = pd.read_csv('big_data_set2_f.csv', encoding='cp949')


# 두 컬럼 평균 계산
grouped_df = (
    df.groupby('ENCODED_MCT', as_index=False)
      .agg({
          'M1_SME_RY_SAA_RAT': 'mean',   # 동일 업종내 평균대비 매출비율 평균
          'M1_SME_RY_CNT_RAT': 'mean'    # 동일 업종내 평균대비 매출건수 평균
      })
      .rename(columns={
          'M1_SME_RY_SAA_RAT': 'M1_SME_RY_SAA_RAT_mean',
          'M1_SME_RY_CNT_RAT': 'M1_SME_RY_CNT_RAT_mean'
      })
)



# 새로운 CSV 파일로 저장
grouped_df.to_csv('big_data_set2_f_na.csv', index=False)

print("✅ 동일 가맹점 기준 평균 계산 완료! → big_data_set2_f_na.csv 로 저장됨")