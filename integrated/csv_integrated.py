import pandas as pd
import os
import csv
import glob



# 파일 경로 패턴 지정
file_pattern = './0_data/*.csv'

# 해당 패턴에 맞는 모든 파일 가져오기
file_list = glob.glob(file_pattern)

# 파일들을 담을 빈 리스트 생성
all_data = []

# 각 파일을 읽어와서 리스트에 추가
for file in file_list:
    df = pd.read_csv(file, encoding='CP949')
    all_data.append(df)

merged_df = pd.concat(all_data, ignore_index=True)

df = merged_df

df.to_csv("../total_data.csv", encoding='CP949')


