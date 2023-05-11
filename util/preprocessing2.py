import pandas as pd


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

def is_normal_temper(temper):
    if temper < -40 or temper > 50:
        return False
    return True
    
def is_normal_humid(humid):
    if humid < 0:
        return False
    return True

def get_temper(date):
    # 기온 데이터셋을 읽어옵니다.
    weather_data = pd.read_csv('../data/weather.csv')
    
    # 주어진 날짜에 해당하는 기온을 찾습니다.
    temper = weather_data[weather_data['시간'] == date]['평균기온(°C)'].values

    if len(temper) > 0:
        return temper[0]
    else:
        return None
    
def get_humid(date):
    # 습도 데이터셋을 읽어옵니다.
    weather_data = pd.read_csv('../data/weather.csv')

    # 주어진 날짜에 해당하는 습도을 찾습니다.
    humid = weather_data[weather_data['시간'] == date]['평균 상대습도(%)'].values

    if len(humid) > 0:
        return humid[0]
    else:
        return None    
