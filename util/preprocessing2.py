## preprocessing2 파일
# data_cleasing과 data_cleansing2에 필요한 추가적인 추출 함수
# 기온, 습도 이상치 판별 함수
# 해당 날짜의 평균 기온, 평균 습도 반환 함수
import pandas as pd
import re

# 년월일을 yyyymmdd형식의 8자리 수로 반환하는 함수
def extract_yyyymmdd(s):
    date = s.split()[0]
    list =  date.split('-')
    return int(list[0]+list[1]+list[2])

# 사고신고사유를 분리하는 함수
def extract_sago(s):
    rtn = [0,0,0,0]
    if('사망 1명 이상' in s):
        rtn[0] += 1
    if('3일이상 휴업이 필요한 부상' in s):
        rtn[1] += 1
    if('1000만원 이상의 재산피해' in s):
        rtn[2] += 1
    if('기타' in s):
        rtn[3] += 1
    return rtn

'''
'100억초과 200억이하' '20억초과 30억이하' '200억초과 300억이하' '50억초과 60억이하' '40억초과 50억이하'
 '90억초과 100억이하' '1억초과 5억이하' '10억초과 20억이하' '300억초과 400억이하' '5억초과 10억이하'
 '80억초과 90억이하' '30억초과 40억이하' '70억초과 80억이하' '500억초과 1000억이하'
 '400억초과 500억이하' '1000억초과 2000억이하' '60억초과 70억이하' '2000억초과' '1억이하'
 '''
# 문자열 데이터를 중앙값으로 변환하는 함수
def extract_cost1(data_str):
    # 정규식을 사용하여 문자열에서 금액 범위를 추출합니다.
    try:
        range_pattern = r'(\d+억초과 \d+억이하)'
        range_match = re.search(range_pattern, data_str)
        if range_match:
            # 금액 범위가 있는 경우
            # 금액 범위를 문자열에서 추출하여, 최소값과 최대값을 계산합니다.
            range_str = range_match.group(1)
            range_values = range_str.split(' ')
            min_value = int(range_values[0].replace('억초과', '')) * 100000000
            max_value = int(range_values[1].replace('억이하', '')) * 100000000

            # 최소값과 최대값을 더한 후 2로 나누어 중앙값을 계산합니다.
            median_value = (min_value + max_value) / 2.0
        else:
            median_value = None
    except:
        # 금액 범위가 없는 경우
        # 예외 처리를 하거나 None 값을 반환합니다.
        median_value = None

    # 중앙값을 반환합니다.
    return median_value

# 기온의 이상치를 판별하는 함수
def is_normal_temper(temper):
    if temper < -40 or temper > 50:
        return False
    return True

# 습도의 이상치를 판별하는 함수
def is_normal_humid(humid):
    if humid < 0:
        return False
    return True

## 기상청 데이터 불러오기
import requests
import json

serviceKey = "Fr9wFe/lwpNUNCFDyb4c74NiogVnhbSPOn4VixALepK1XaBViv2tOKOjrbTArthJoToqj0KuLzn4w4TVj/AqJQ=="
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
params ={'serviceKey' : serviceKey, 'pageNo' : '1', 'numOfRows' : '10', 'dataType' : 'JSON', 'dataCd' : 'ASOS', 'dateCd' : 'DAY', 'startDt' : '20100101', 'endDt' : '20100601', 'stnIds' : '108' }

# 해당 날짜의 평균 기온를 반환하는 함수
def get_temper(yyyymmdd):
    params['startDt'] = yyyymmdd 
    params['endDt'] = yyyymmdd+1
    try:
        response = requests.get(url, params=params)
        jsondata = json.loads(response.content)

        for item in jsondata['response']['body']['items']['item']:
            return float(item['avgTa'])
    except ValueError:
        return 0.0
    except KeyError:
        return None

# 해당 날짜의 평균 기온를 반환하는 함수(지역)
def get_temper2(yyyymmdd, loc):
    params['startDt'] = yyyymmdd 
    params['endDt'] = yyyymmdd+1
    params['stnIds'] = loc_code(loc)
    response = requests.get(url, params=params)
    jsondata = json.loads(response.content)

    for item in jsondata['response']['body']['items']['item']:
        return float(item['avgTa'])
    
# 해당 날짜의 평균 습도를 반환하는 함수
def get_humid(yyyymmdd):
    try:
        params['startDt'] = yyyymmdd 
        params['endDt'] = yyyymmdd+1
        response = requests.get(url, params=params)
        jsondata = json.loads(response.content)

        for item in jsondata['response']['body']['items']['item']:
            return float(item['avgRhm'])  
    except ValueError:
        return 0.0
    except KeyError:
        return None

# 해당 날짜의 평균 습도를 반환하는 함수
def get_humid2(yyyymmdd, loc):
    params['startDt'] = yyyymmdd 
    params['endDt'] = yyyymmdd+1
    params['stnIds'] = loc_code(loc)
    response = requests.get(url, params=params)
    jsondata = json.loads(response.content)

    for item in jsondata['response']['body']['items']['item']:
        return float(item['avgRhm']) 

# 지역 코드를 반환하는 함수
def loc_code(loc):
    df = pd.read_csv('../data/loc_data.csv')
    for i, j in iterrows():
        if j == loc:
            return int(i)
    return 108