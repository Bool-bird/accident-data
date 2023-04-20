from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import logging

# 로그 설정
logging.basicConfig(filename='log.txt', level=logging.INFO)

#건설공사 안전관리 종합정보망 사이트 크롤링 코드

url = 'https://www.csi.go.kr/acd/acdCaseList.do'  # 가져올 페이지의 URL

# Chrome 웹 드라이버 실행
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome('./chromedriver_mac_arm64/chromedriver', options=options)
driver.get(url)

# 크롤링할 데이터 저장을 위한 리스트 선언
data_list = []

# 현재 페이지 번호를 가져오기
current_page_num = int(driver.find_element('css selector', '.pagination .active a').text)

logging.info("크롤링 시작.")

# 페이지 수 만큼 반복하면서 크롤링 수행
for i in range(1, 1781):  # 1번 페이지부터 1781번 페이지까지 크롤링 수행
    try:
        current_page_num = int(driver.find_element('css selector', '.pagination .active a').text)
        # 다음 페이지로 이동하기
        driver.execute_script(f"goPage('{i}');")

        # 페이지 내 모든 a 태그 선택하기
        links = driver.find_elements('xpath', '//tbody/tr/td[1]/a')

        # href 속성값 추출하여 리스트에 저장하기
        href_list = [link.get_attribute('href') for link in links]

        # 각 하위 페이지를 크롤링하며 데이터 추출 작업 수행
        for link_index in range(len(links)):
            # 매번 새로운 a 태그 리스트를 가져옴
            links = driver.find_elements('xpath', '//tbody/tr/td[1]/a')

            # a 태그 href 속성값 가져오기
            link_href = links[link_index].get_attribute('href')

            # JavaScript 함수 호출하여 하위 페이지 열기
            driver.execute_script(link_href)

            # 하위 페이지 HTML 코드 가져오기
            sub_html = driver.page_source
            sub_soup = BeautifulSoup(sub_html, 'html.parser')

            # 필요한 데이터 추출 작업 수행
            data_dict = {}
            td_heads = sub_soup.find_all('td', class_='td-head')
            t_lefts = sub_soup.find_all('td', class_='t-left')
            td_head_index = 0

            for t_left_index, t_left in enumerate(t_lefts):
                td_head = td_heads[td_head_index]
                key = td_head.text.strip()
                value = t_left.text.strip()

                # td-head 클래스 태그가 rowspan 속성을 가지고 있다면, 크롤링하지 않는다.
                if 'rowspan' in td_head.attrs:
                    rowspan = int(td_head.attrs['rowspan'])
                    if t_left_index < rowspan:
                        continue
                    else:
                        td_head_index += 1
                        td_head = td_heads[td_head_index]
                        key = td_head.text.strip()

                # td-head 클래스 태그가 연속으로 2번 나오는 경우, 두 번째 태그의 내용을 키 값으로 사용
                if t_left_index == 0 and td_head_index == 0:
                    data_dict[key] = t_lefts[t_left_index+1].text.strip()
                    td_head_index += 1
                elif t_left_index == 0 and td_head_index > 0:
                    td_head_index -= 1
                    continue
                else:
                    # t-left 클래스 하위 태그(label)가 있는 경우, label의 내용을 밸류 값으로 사용
                    if t_left.find('label'):
                        sub_values = []
                        for label in t_left.find_all(['div']):
                            sub_values.append(label.text.strip())
                        value = ' '.join(sub_values).strip()

                    data_dict[key] = value
                    td_head_index += 1

            # 추출한 데이터를 리스트에 저장
            data_list.append(data_dict)

            # 이전 페이지로 돌아가기
            driver.execute_script("javascript:history.back()")
            # driver.back()
        # 로그 출력
        logging.info(f"{i} 번 페이지 완료.")
    except Exception as e:
        print("{} 에러 발생, {} 페이지에서 발생".format(e, current_page_num))
        logging.error("{} 에러 발생, {} 페이지에서 발생".format(e, current_page_num))

# 브라우저 닫기
driver.quit()

for data_dict in data_list:
    for key, value in data_dict.items():
        data_dict[key] = value.replace('\t', '').replace('\n', '')

# 크롤링한 데이터 dataframe으로 변환
df = pd.DataFrame(data_list)

df = df.drop(columns=["검색범위", "검색방법", "검색기간"], axis=1)

# csv 파일로 저장
df.to_csv('output.csv', encoding='utf-8-sig')

