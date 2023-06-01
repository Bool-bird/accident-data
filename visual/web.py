import streamlit as st

st.title("Bool-Bird")

percent = st.slider("공정률")

date = st.date_input(
    "오늘 날짜를 입력하세요.",
    datetime.date(2019, 7, 6))

option = st.selectbox(
    '공종',
    ('Email', 'Home phone', 'Mobile phone'))


#출력
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")