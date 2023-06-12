# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import re
from dateutil import parser


#------------아래는 제목-----------------


#제목
col1,empty2,col2 = st.columns([1, 0.3, 8.7])
with col1 :
    st.image("phoenix.png", width=80)
with col2 :
    st.title("건설 안전사고 위험도 예측 서비스\n")


#------------아래는 입력 (총 13개)---------

list = ["시설물 종류_건축","시설물 종류_산업환경설비","시설물 종류_조경","시설물 종류_토목",
        "공공/민간 구분_공공","공공/민간 구분_민간",
        "날씨_강설","날씨_강우","날씨_강풍","날씨_맑음","날씨_안개","날씨_흐림",
        "공종_가설공사","공종_강구조물공사","공종_건축 토공사","공종_건축물 부대공사","공종_관공사","공종_관공사 부대공사","공종_교량공사","공종_금속공사","공종_기계설비공사","공종_기타","공종_댐 및 제방공사","공종_도로 및 포장공사","공종_도장공사","공종_말뚝공사","공종_목공사","공종_미장공사","공종_방수공사","공종_산업설비공사","공종_수장공사","공종_전기설비공사","공종_조경공사","공종_조적공사","공종_지반개량공사","공종_지반조사","공종_지붕 및 홈통공사","공종_지정공사","공종_창호 및 유리공사","공종_철골공사","공종_철근콘크리트공사","공종_철도 및 궤도공사","공종_타일 및 돌공사","공종_터널공사","공종_토공사","공종_통신설비공사","공종_특수 건축물공사","공종_프리캐스트 콘크리트공사","공종_하천공사","공종_항만공사","공종_해체 및 철거공사",
        "발생일시","공사비","공사기간","공정률","작업자수","설계안전성검토","기온","습도"]

df = pd.DataFrame({"class": list, "boolean": 0.0})
df = df.set_index("class")

#(1) 공사기간 (yy.mm.dd ~ yy.mm.dd)
col1,empty2,col2 = st.columns([1, 0.03, 1])
with col1 :
    start_day = st.date_input('공사 시작일을 선택해주세요.')
with col2 :
    end_day = st.date_input('공사 종료일을 선택해주세요.')

#(2) 공사기간 계산
start_day = parser.parse(str(start_day))
end_day = parser.parse(str(end_day))
dur = (end_day - start_day).days
if (dur <= 0): st.error("공사기간 입력 오류입니다. 입력한 공사 시작일과 종료일을 다시 한 번 확인해주세요.")
df.loc['공사기간'] = dur

#(3) 시설물종류 (건축~)
col1,empty2,col2 = st.columns([1, 0.03, 1])
with col1 :
    facility = ['건축', '산업환경설비', '조경', '토목', '기타']
    selected_facility = st.selectbox('시설물종류를 선택해주세요.',facility)
string = '시설물 종류_'
df.loc[string + selected_facility] = 1.0
    
#(4) 공정률 (~%)
with col2 :
    percent = st.text_input('공정률을 입력해주세요.  (단위 : %)', value="", placeholder="65%라면 '65'라고 입력해주세요")
if percent:
    df.loc['공정률'] = float(percent)
else:
    df.loc['공정률'] = None
    # st.error("공사기간 입력 오류입니다. 입력한 공사 시작일과 종료일을 다시 한 번 확인해주세요.")
    

#(6),(5) 공종 (철근콘크리트~)
with col2:
    category = ['가설공사', '강구조물공사', '건축 토공사', '건축물 부대공사', '관공사', '관공사 부대공사', '교량공사', '금속공사', '기계설비공사', '댐 및 제방공사', '도로 및 포장공사', '도장공사', '말뚝공사', '목공사', '미장공사', '방수공사', '산업설비공사', '수장공사', '전기설비공사', '조경공사', '조적공사', '지반개량공사', '지반조사', '지붕 및 홈통공사', '지정공사', '창호 및 유리공사', '철골공사', '철근콘크리트공사', '철도 및 궤도공사', '타일 및 돌공사', '터널공사', '토공사', '통신설비공사', '특수 건축물공사', '프리캐스트 콘크리트공사', '하천공사', '항만공사', '해체 및 철거공사', '기타']
    search_term = st.text_input('공종 검색어 입력을 통해 빠르게 검색할 수 있습니다.', value="", placeholder="금속공사라면 '금속'을 검색해보세요")
    
    filtered_category = [item for item in category if search_term.lower() in item.lower()]
with col1:
    selected_category = st.selectbox('공종을 선택해주세요.', filtered_category)
string = '공종_'
df.loc[string + selected_category] = 1.0

#(7) 설계안전성검토 (대상,비대상)
with col1 :
    selected_safety = st.radio("설계안전성검토를 선택해주세요.", ("대상", "비대상"))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
if (selected_safety == "대상"):
    df.loc['설계안전성검토'] = 1.0

#(8) 시설관리공사 (공공,민간)
with col2 :
    selected_company = st.radio("시설관리공사를 선택해주세요.", ("공공", "민간"))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
if selected_company == "공공":
    df.loc['공공/민간 구분_공공'] = 1.0
    df.loc['공공/민간 구분_민간'] = 0.0
else:
    df.loc['공공/민간 구분_공공'] = 0.0
    df.loc['공공/민간 구분_민간'] = 1.0

#(9) 공사비 (~원)
with col1 :
    cost = st.text_input('공사비를 입력해주세요. (단위: 억 원)', value="", placeholder="10억 원이라면 '10'이라고 입력해주세요")
#df['공사비'] = float(cost)
if cost:
    df.loc['공사비'] = float(cost)
else:
    df.loc['공정률'] = None

#(10) 작업자수 (~명)
with col2 :
    person = st.text_input('작업자수를 입력해주세요.  (단위 : 명)', value="", placeholder="1,000명이라면 '1000'이라고 입력해주세요")
#df['작업자수'] = float(person)
if person:
    df.loc['작업자수'] = float(person)
else:
    df.loc['작업자수'] = None

#(11, 12, 13) 날씨, 기온, 습도 -> 따로 입력X

# 기상청 데이터 연결 "기상청_단기예보 ((구)_동네예보) 조회서비스"
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
string = '날씨_'
key = '맑음'

# API 요청 URL
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

# 인증키
api_key = 'NminqLTNuSX5OFbyRamiOBFhuUBormib7/IeKYFKpWn1iXnxa1PEQ5IZAfJWebf8nOOb2FplMo5tdutaV6kUxQ=='

# 현재 날짜와 시간 가져오기
now = datetime.now()
date = now.strftime('%Y%m%d')  # 날짜 형식 변환
time = now.strftime('%H')+'00' # 시간 형식 변환  --> 여기서 오류, 10분 미만일 때 API 못불러옴

# # 사용자로부터 날짜와 시간 입력받기
# date = input('날짜를 입력하세요 (예: 20230608): ')
# time = input('시간을 입력하세요 (예: 1400): ')

# 요청 파라미터
params = {
    'serviceKey': api_key,
    'numOfRows': '10',  # 가져올 데이터 개수
    'dataType': 'XML',  # 응답 데이터 형식
    'base_date': date,  # 기준 날짜
    'base_time': time,  # 기준 시간
    'nx': '60',  # 위도
    'ny': '127'  # 경도
}

# API 요청 보내기
response = requests.get(url, params=params)
if (response.status_code != 200):
    params['base_time'] = '0000'
    response = requests.get(url, params=params)
xml_data = response.text

# XML 파싱
tree = ET.ElementTree(ET.fromstring(xml_data))
root = tree.getroot()

# 필요한 데이터 추출
items = root.findall('.//item')

found = False

for item in items:
    category = item.find('category').text
    if category == 'T1H':  # 기온(category=T1H) 데이터 추출
        temp = item.find('obsrValue').text
        found = True
    elif category == 'REH':  # 습도(category=REH) 데이터 추출
        humidity = item.find('obsrValue').text
        found = True
    elif category == "SKY": # 맑음=1, 흐림=4
        sky = item.find('obsrValue').text
        if sky == '4':
            key = '흐림'
        found = True
    elif category == "PTY": # 강설=3, 강우=1
        pty = item.find('obsrValue').text
        if pty == '3': 
            key = '강설'
        elif pty == '1':
            key = '강우'
        found = True
    elif category == "WSD": # 강풍>=9
        wsd = item.find('obsrValue').text 
        wsd = int(float(wsd))
        if wsd >= 9: 
            key = '강풍'
        found = True
      
if not found:
    print('해당 날짜와 시간에 대한 데이터를 찾을 수 없습니다.')
df.loc[string + key] = 1.0
df.loc['기온'] = temp
df.loc['습도'] = humidity

#------------아래는 분석-----------------

# predict/predict.py에 있는 predict(input_data)함수에 input_data 넣으면 class와 상세 위험도 리턴
import sys
sys.path.append('..')
from predict.predict import predict 
from cleansing.data_cleansing import preprocess_data, preprocess_data_classification

import pandas as pd
from dateutil import parser

df['boolean'] = df['boolean'].astype('float64')
df = df.squeeze()

predicted_class, detail_risk  = predict(df)
# return value는 predicted_class={상: 2, 중: 1, 하: 0}, detail_risk = numpy.float64입니당


#import sys
#sys.path.append('..')
#from model.models import LGBMmodel, LGBMmodel_classification

# from models import LGBMmodel, LGBMmodel_classification
# from predict import *
# import numpy as np

# # Model Training
# bst_classification = LGBMmodel_classification()
# bst_regression_high = LGBMmodel('high')
# bst_regression_mid = LGBMmodel('mid')
# bst_regression_low = LGBMmodel('low')

# # Predicting
# def predict(input_data): 
#     # Classification
#     class_proba = bst_classification.predict(input_data)
#     predicted_class = np.argmax(class_proba, axis=1)  # 상: 2, 중: 1, 하: 0
#     detail_risk = 0

#     # Regression
#     if predicted_class == 2:  # 상
#         dmg_scale = bst_regression_high.predict(input_data)
#         detail_risk = (np.expm1(dmg_scale) - 1) * 100
#     elif predicted_class == 1:  # 중
#         dmg_scale = bst_regression_mid.predict(input_data)
#         detail_risk = (np.expm1(dmg_scale) - 0.5) * 100 * 2
#     else:  # 하
#         dmg_scale = bst_regression_low.predict(input_data)
#         detail_risk = (np.expm1(dmg_scale)) * 100 * 2

#     return predicted_class, detail_risk


#------------아래는 출력-----------------

st.write(' ')
button_clicked = st.button('위험도 예측 결과 확인') #통계페이지 이동하는 버튼
if button_clicked:
    predicted_class, detail_risk = predict(df)
    detail_risk = detail_risk / 100
    color = detail_risk  # 색 부분의 비율 (0.0 ~ 1.0 사이의 값)
    if predicted_class==0:
        st.title(f"위험도는 \'하\' 입니다.")
        color_width = int(color * 90)  # 색 부분의 너비 계산
        color_bar_style = f'background-color: #89BF6C; height: 8px; width: {color_width}%; display: inline-block;'
        green_bar_style = f'background-color: #E4F4CF; height: 8px; width: {90-color_width}%; display: inline-block;'
        yellow_bar_style = f'background-color: #FDEDD0; height: 8px; width: 5%; display: inline-block;'
        red_bar_style = f'background-color: #F2D0CD; height: 8px; width: 5%; display: inline-block;'
    
    elif predicted_class==1:
        st.title(f"위험도는 \'중\' 입니다.")
        color_width = int(color * 90)  # 색 부분의 너비 계산
        green_bar_style = f'background-color: #89BF6C; height: 8px; width: 5%; display: inline-block;'
        color_bar_style = f'background-color: #F0BD6A; height: 8px; width: {color_width}%; display: inline-block;'
        yellow_bar_style = f'background-color: #FDEDD0; height: 8px; width: {90-color_width}%; display: inline-block;'
        red_bar_style = f'background-color: #F2D0CD; height: 8px; width: 5%; display: inline-block;'
    
    elif predicted_class==2:
        st.title(f"위험도는 \'상\' 입니다.")
        color = color/2
        color_width = int(color * 90)  # 색 부분의 너비 계산
        green_bar_style = f'background-color: #89BF6C; height: 8px; width: 5%; display: inline-block;'
        yellow_bar_style = f'background-color: #F0BD6A; height: 8px; width: 5%; display: inline-block;'
        color_bar_style = f'background-color: #DD5E65; height: 8px; width: {color_width}%; display: inline-block;'
        red_bar_style = f'background-color: #F2D0CD; height: 8px; width: {90-color_width}%; display: inline-block;'
        color = color*2
        
    st.write(f"상세 위험도는 \' {int(color*100)} % \' 입니다.")
    st.markdown(
        f'<div style="{green_bar_style}"></div><div style="{yellow_bar_style}"></div><div style="{color_bar_style}"></div><div style="{red_bar_style}"></div>',
        unsafe_allow_html=True)
    st.write(df)