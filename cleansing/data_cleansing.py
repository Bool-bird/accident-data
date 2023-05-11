import sys
sys.path.append('..')

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from util.preprocessing import *
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import OneSidedSelection, EditedNearestNeighbours
import re
from dateutil import parser


def preprocess_data():
    df = pd.read_csv('../data/output-v2.csv')
    #필요 없는 특성 제거

    allColumns = df.columns
    params = ['발생일시','공공/민간 구분', '기상상태', '시설물 종류', '사망자수(명)', '부상자수(명)', '공사비', '공사기간', '공정률', '작업자수', '설계안전성검토', '공종']

    df = df.drop(allColumns.drop(params), axis=1)

    df = df.dropna()

    df['공종'] = df['공종'].apply(extract_middle_class)

    #범주형 데이터를 수치형 데이터로 인코딩

    df['사망자수(명)'] = df['사망자수(명)'].apply(parse_num_of_people)
    df['부상자수(명)'] = df['부상자수(명)'].apply(parse_num_of_people)
    df['발생일시'] = df['발생일시'].apply(extract_month)
    df['시설물 종류'] = df['시설물 종류'].apply(extract_facility)
    df['공사기간'] = df['공사기간'].apply(count_days)
    df['공정률'] = df['공정률'].apply(str_to_median)
    df['작업자수'] = df['작업자수'].apply(extract_population)
    df['공사비'] = df['공사비'].apply(extract_cost)
    safety_ratio_by_job = calculate_safety_ratios(df)
    safety_ratio_by_job = safety_ratio_by_job.drop(['공종별 안전사고 발생 비율', '공종별 사망자 비율', '공종별 부상자 비율', '공종별 안전사고 발생강도 비율', '공종별 안전사고 발생 건수', '공종별 사망자수', '공종별 부상자수'], axis=1)
    df = pd.merge(df, safety_ratio_by_job, on='공종', how='inner')
    df['피해규모'] = df.apply(calc_damage_scale, axis=1)

    # 기상 상태 컬럼 분리
    df[['날씨', '기온', '습도']] = df['기상상태'].str.extract('날씨 : (\S+)기온 : (\d+)℃습도 : (\d+)%')
    df = df.drop(['기상상태'], axis=1)

    df = df.dropna()

    le = LabelEncoder()
    df['설계안전성검토'] = le.fit_transform(df['설계안전성검토'])

    # 시설물 종류 특성을 원-핫 인코딩

    ct = ColumnTransformer([
    ('onehot', OneHotEncoder(sparse=False), ['시설물 종류', '공공/민간 구분', '날씨', '공종'])], remainder='passthrough'
    )
    ct.fit(df)
    X = ct.transform(df)
    # 컬럼 이름 리스트 생성

    num_cols = df.columns.tolist()
    ohe = ct.named_transformers_['onehot']
    ohe_cols = ohe.get_feature_names_out(['시설물 종류', '공공/민간 구분', '날씨', '공종']).tolist()
    new_cols = ohe_cols + num_cols
    new_cols.remove('시설물 종류')
    new_cols.remove('공공/민간 구분')
    new_cols.remove('날씨')
    new_cols.remove('공종')
    # DataFrame으로 변환

    df = pd.DataFrame(X, columns=new_cols)

    df = df.astype('float64')

    df['습도'] = df['습도'].apply(lambda x: x/100)

    # --------------------정제 완료 ----------------------------

    X = df.drop(['사망자수(명)', '부상자수(명)', '피해규모', '공종별 위험도 평가지수'], axis=1)
    y = df[['공종별 위험도 평가지수']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

preprocess_data()