import requests

url = 'https://www.csi.go.kr/acd/acdCaseList.do'  # 가져올 페이지의 URL
response = requests.get(url)  # GET 요청을 보내서 페이지 내용 가져오기

if response.status_code == 200:  # HTTP 응답 코드가 200인 경우(정상적인 응답)
    html = response.text  # HTML 코드 추출
    print(html)  # 추출한 HTML 코드 출력
else:
    print('Error:', response.status_code)  # 오류 메시지 출력
