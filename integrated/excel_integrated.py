import pandas as pd
import glob
import logging

# 로그 설정: 타임스탬프, 로그 레벨, 메시지를 포함하여 출력 (로그 레벨은 INFO 이상)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 엑셀 파일 경로 패턴 지정 (필요에 맞게 수정)
file_pattern = './0_data/*.xlsx'
file_list = glob.glob(file_pattern)

if not file_list:
    logging.warning("지정된 패턴에 맞는 엑셀 파일을 찾을 수 없습니다: %s", file_pattern)
else:
    logging.info("총 %d개의 엑셀 파일을 찾았습니다.", len(file_list))

# 모든 데이터를 저장할 리스트 초기화
all_data = []

# 각 엑셀 파일 처리
for file_idx, file in enumerate(file_list, start=1):
    logging.info("(%d/%d) 파일 처리 시작: %s", file_idx, len(file_list), file)
    try:
        # 엑셀 파일 열기
        xls = pd.ExcelFile(file)
        sheet_names = xls.sheet_names
        logging.info("   파일 내 시트 목록: %s", sheet_names)
        
        # 각 시트를 처리
        for sheet_idx, sheet in enumerate(sheet_names, start=1):
            logging.info("      (%d/%d) 시트 읽기 시작: %s", sheet_idx, len(sheet_names), sheet)
            try:
                df = xls.parse(sheet)
                logging.info("         시트 '%s' 데이터 읽기 성공 (행: %d, 열: %d)", sheet, len(df), len(df.columns))
                all_data.append(df)
            except Exception as parse_error:
                logging.error("         시트 '%s' 읽는 중 오류 발생: %s", sheet, parse_error)
    except Exception as e:
        logging.error("   파일 '%s' 처리 중 오류 발생: %s", file, e)

# 모든 시트의 데이터를 하나의 DataFrame으로 병합 후 CSV 파일로 저장
if all_data:
    try:
        merged_df = pd.concat(all_data, ignore_index=True)
        logging.info("데이터 병합 완료. 최종 병합된 데이터의 행 수: %d", len(merged_df))
        
        output_csv = "../total_data.csv"
        merged_df.to_csv(output_csv, index=False, encoding='CP949')
        logging.info("CSV 파일로 저장 완료: %s", output_csv)
    except Exception as merge_error:
        logging.error("데이터 병합 또는 저장 중 오류 발생: %s", merge_error)
else:
    logging.warning("병합할 데이터가 없습니다. 입력 엑셀 파일 및 시트를 확인하세요.")
