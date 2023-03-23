import requests

serviceKey = "SSViRnA2wdqrMhE6gLVMdjBl6%2FYXNYADYJTlWSvIDLj9hb4RDasyNSx2S250bZRkGhxsG0NT%2FAgLmlQD2ziLeg%3D%3D"

url = 'http://apis.data.go.kr/B552016/FacilAccidentService/getFacilAccidentList'
params ={'serviceKey' : serviceKey, 'numOfRows' : '1', 'pageNo' : '1', 'type' : 'json', 'accdntNm' : '2680번 교', 'facilNm' : '2680번 교', 'facilAddr' : '버지니아주' }

response = requests.get(url, params=params)
print(response.content)