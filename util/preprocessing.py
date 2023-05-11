import re
from dateutil import parser

def parse_num_of_people(s):
    # '내국인 :0명외국인 :0명 내국인 :0명 외국인 :0명'와 같은 문자열을 처리하기 위해
    # 정규표현식을 이용하여 '내국인 :숫자'와 '외국인 :숫자'를 추출합니다.
    regex = r'(내국인|외국인)\s*:\s*(\d+)명'
    matches = re.findall(regex, s)
    
    # 내국인과 외국인의 총 인원 수를 계산합니다.
    num_internal = 0
    num_foreign = 0
    for match in matches:
        if match[0] == '내국인':
            num_internal += int(match[1])
        elif match[0] == '외국인':
            num_foreign += int(match[1])
    result = (num_internal + num_foreign) / 2
    return result

# 발생 일시에서 월만 뽑아오는 함수
def extract_month(s):
    return int(s.split('-')[1])

# 시설물 종류 대분류 추출 함수
def extract_facility(s):
    return s.split('-')[0]

def extract_ratio(percent_str):
    try:
        # 문자열에서 % 값 추출
        print(re.findall(r'\d+\.?\d*%', str(percent_str)))
        percent = re.findall(r'\d+\.?\d*%', str(percent_str))[0]

        # % 값을 비율 값으로 변환
        if '~' in percent:
            # 30~39% 와 같은 경우
            ratio = float(percent.split('~')[1].replace('%', '')) / 100
        else:
            # 10% 미만 과 같은 경우
            ratio = float(percent.replace('%', '')) / 100

        return ratio
    
    except:
        return 0

# 문자열 데이터를 중앙값으로 변환하는 함수
def str_to_median(data_str):

    if '~' in data_str:
        # 범위형 데이터인 경우
        # 문자열을 '~' 기준으로 분리하여 최소값과 최대값을 추출합니다.
        range_list = data_str.split('~')
        min_value = int(range_list[0])
        max_value = int(range_list[1][:-1])

        # 최소값과 최대값을 더한 후 2로 나누어 중앙값을 계산합니다.
        median_value = (min_value + max_value) / (2.0 * 100)

    elif '이상' in data_str:
        value = int(data_str[:2])
        # n% 이상일 경우 n.5%로 가정하여 중앙값을 계산합니다.
        median_value = (value + 100) / (2.0 * 100)

    elif '미만' in data_str:
        value = int(data_str[:2])
        # n% 미만일 경우 n-0.5%로 가정하여 중앙값을 계산합니다.
        median_value = value / 100

    else:
        # 범위형, 이상형, 미만형 데이터가 아닌 경우
        # 예외 처리를 하거나 None 값을 반환합니다.
        median_value = None

    # 중앙값을 반환합니다.
    return median_value

def extract_population(population_str):
    try:
        # 문자열에서 사람 값 추출
        population = re.findall(r'\d+\.?\d*인', population_str)[0]

        if '~' in population:
            # 30~39인 과 같은 경우
            num = int(population.split('~')[1].replace('인', ''))
        else:
            # 10인 미만 과 같은 경우
            num = int(population.replace('인', ''))

        return num
    except:
        return 0

import re

# 문자열 데이터를 중앙값으로 변환하는 함수
def extract_cost(data_str):
    # 정규식을 사용하여 문자열에서 금액 범위를 추출합니다.
    range_pattern = r'(\d+억 \~ \d+억원 미만)'
    range_match = re.search(range_pattern, data_str)

    if range_match:
        # 금액 범위가 있는 경우
        # 금액 범위를 문자열에서 추출하여, 최소값과 최대값을 계산합니다.
        range_str = range_match.group(1)
        range_values = range_str.split(' ~ ')
        min_value = int(range_values[0].replace('억', '')) * 100000000
        max_value = int(range_values[1].replace('억원 미만', '')) * 100000000

        # 최소값과 최대값을 더한 후 2로 나누어 중앙값을 계산합니다.
        median_value = (min_value + max_value) / 2.0

    else:
        # 금액 범위가 없는 경우
        # 예외 처리를 하거나 None 값을 반환합니다.
        median_value = None

    # 중앙값을 반환합니다.
    return median_value


# 날짜 수 세기 함수
def count_days(date_string):
    try:
        date_str = date_string.split('(해당공종 :')[0].strip()

        str_arr = date_str.split(' ~ ')
        start_date_str = str_arr[0]
        end_date_str = str_arr[1]
        start_date = parser.parse(start_date_str)
        end_date = parser.parse(end_date_str)
        if (end_date - start_date).days <= 0:
            sub_date = date_string.split('(해당공종 :')[1].strip()
            sub_date_str = sub_date.split(')')[0].strip()

            str_arr = sub_date_str.split(' ~ ')
            start_date_str = str_arr[0]
            end_date_str = str_arr[1]
            start_date = parser.parse(start_date_str)
            end_date = parser.parse(end_date_str)

        return (end_date - start_date).days
    except:
        pass

# 피해규모 계산 함수
def calc_damage_scale(df):
    damages_scale = 3 * df['사망자수(명)'] + df['부상자수(명)']
    # + 0.1 * np.sqrt(df['피해금액'])
    return damages_scale
# CSV 파일을 DataFrame으로 읽어오기

import pandas as pd

def calculate_safety_ratios(df):
    # 전체 안전사고 발생 건수
    total_accidents = len(df)
    
    # 공종별 안전사고 발생 건수
    group_accidents = df.groupby('공종')['공종'].count().reset_index(name='공종별 안전사고 발생 건수')
    
    # 공종별 안전사고 발생 비율
    group_accidents['공종별 안전사고 발생 비율'] = group_accidents['공종별 안전사고 발생 건수'] / total_accidents * 100
    
    # 공종별 사망자 비율
    group_fatalities = df.groupby('공종')['사망자수(명)'].sum().reset_index(name='공종별 사망자수')
    group_fatalities['공종별 사망자 비율'] = group_fatalities['공종별 사망자수'] / group_fatalities['공종별 사망자수'].sum() * 100
    
    # 공종별 부상자 비율
    group_injuries = df.groupby('공종')['부상자수(명)'].sum().reset_index(name='공종별 부상자수')
    group_injuries['공종별 부상자 비율'] = group_injuries['공종별 부상자수'] / group_injuries['공종별 부상자수'].sum() * 100
    
    # 공종별 안전사고 발생강도 비율
    group_accident_intensity = pd.merge(group_fatalities, group_injuries, on='공종')
    group_accident_intensity['공종별 안전사고 발생강도 비율'] = group_accident_intensity['공종별 사망자 비율'] * 3 + group_accident_intensity['공종별 부상자 비율']
    
    # 공종별 위험도 평가지수
    group_safety_index = pd.merge(group_accidents, group_accident_intensity, on='공종')
    group_safety_index['공종별 위험도 평가지수'] = group_safety_index['공종별 안전사고 발생 비율'] + group_safety_index['공종별 안전사고 발생강도 비율']
    
    return group_safety_index


# 공종에서 중분류만 추출하는 함수
def extract_middle_class(s):
    if(type(s) == float):
        return("없음")
    return s.split(' > ')[1]
