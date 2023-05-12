## preprocessing2 파일
# data_cleasing과 data_cleansing2에 필요한 추가적인 추출 함수
# 기온, 습도 이상치 판별 함수
# 해당 날짜의 평균 기온, 평균 습도 반환 함수
import pandas as pd

# 년월일을 yyyymmdd형식의 8자리 수로 반환하는 함수
def extract_yyyymmdd(s):
    date = s.split()[0]
    list =  date.split('-')
    return list[0]+list[1]+list[2]

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

# 비사고데이터의 "공사비"를 추출하는 함수
def extract_cost(data_str):

    if '~' in data_str:
        # 범위형 데이터인 경우
        # 문자열을 '~' 기준으로 분리하여 최소값과 최대값을 추출합니다.
        range_list = data_str.split('~')
        min_value = int(range_list[0])
        max_value = int(range_list[1][:-1])

        # 최소값과 최대값을 더한 후 2로 나누어 중앙값을 계산합니다.
        median_value = (min_value + max_value) / (2.0 * 100)

    elif '초과' in data_str:
        value = int(data_str[:2])
        # n% 초과일 경우 n.5%로 가정하여 중앙값을 계산합니다.
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
    params['startDt'] = yymmdd 
    params['endDt'] = yymmdd+1
    response = requests.get(url, params=params)
    jsondata = json.loads(response.content)

    for item in jsondata['response']['body']['items']['item']:
        return(item['avgTa'])

# 해당 날짜의 평균 기온를 반환하는 함수(지역)
def get_temper(yyyymmdd, loc):
    params['startDt'] = yymmdd 
    params['endDt'] = yymmdd+1
    params['stnIds'] = loc_code(loc)
    response = requests.get(url, params=params)
    jsondata = json.loads(response.content)

    for item in jsondata['response']['body']['items']['item']:
        return(item['avgTa'])
    
# 해당 날짜의 평균 습도를 반환하는 함수
def get_humid(yyyymmdd):
    params['startDt'] = yymmdd 
    params['endDt'] = yymmdd+1
    response = requests.get(url, params=params)
    jsondata = json.loads(response.content)

    for item in jsondata['response']['body']['items']['item']:
        return(item['avgRhm'])  

# 해당 날짜의 평균 습도를 반환하는 함수
def get_humid(yyyymmdd, loc):
    params['startDt'] = yymmdd 
    params['endDt'] = yymmdd+1
    params['stnIds'] = loc_code(loc)
    response = requests.get(url, params=params)
    jsondata = json.loads(response.content)

    for item in jsondata['response']['body']['items']['item']:
        return(item['avgRhm']) 

# 지역 코드를 반환하는 함수
def loc_code(loc):
    df = pd.read_csv('../data/loc_data.csv')
    for i, j in iterrows():
        if j == loc:
            return int(i)
    return 108