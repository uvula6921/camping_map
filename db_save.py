from pymongo import MongoClient # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import requests # requests 라이브러리 설치 필요
import json # json 라이브러리 설치 필요


client = MongoClient('localhost', 27017)
# mongoDB는 27017 포트로 돌아갑니다.
db = client.camping_map
# 'camping_map'라는 이름의 db를 사용합니다. 'camping_map' db가 없다면 새로 만듭니다.

url_items = 'http://api.visitkorea.or.kr/openapi/service/rest/GoCamping/basedList?ServiceKey=zx%2F1%2FYPkTrW7rdL4k3RAYq7sJf2GrX4HqZrA7gAQwwOC%2BwkCgrlEtrnXEFFsqO9QV3GLgkWGn6Ac0cIxvRmo8w%3D%3D&numOfRows=2611&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json'
# 요청 URL을 url_items라는 변수에 넣습니다.

response = requests.get(url_items)
# requests 를 사용해 URL_item get요청(Request)하기

# GET을 사용할 때는 requests.get()을 사용하고, POST를 사용할때는 requests.post()를 사용합니다.

dict = json.loads(response.text)
# 파이썬 형식에 맞게 디코딩을 해줘야 함

camp_info =dict['response']['body']['items']['item']
# dict값은 파이썬 형식에 맞게 디코딩한 값
# camp_info라는 변수에 item까지 접근한 값을 넣어줍니다.

for camp_item in camp_info:
# 반복문을 돌려 각각의 딕셔너리를 나열후,
    address = camp_item['addr1']
    camp_name = camp_item['facltNm']
    mapX = camp_item['mapY']
    mapY = camp_item['mapX']
    contentId = camp_item['contentId']
    phone = camp_item.get('tel','번호X')
    # 해당 key가 없을 경우 번호X로 대체할 수 있음 (get을 사용)
    feature = camp_item.get('featureNm','정보없음')
    homepage = camp_item.get('homepage','홈페이지X')
    story = camp_item.get('lineIntro','정보없음')
    intro = camp_item.get('intro','정보없음')
    image_url = camp_item.get('firstImageUrl', '사진없음')
    # 각각의 변수를 만들고 그안에 Value 값들을 넣어줍니다.

    doc = {
      'address': address,
      'camp_name': camp_name,
      'mapX': mapX,
      'mapY': mapY,
      'camp_id': contentId,
      'phone' : phone,
      'feature' : feature,
      'homepage' : homepage,
      'onelinestory' : story,
      'intro' : intro,
      'image_url': image_url
   }
	# 도큐먼트를 만들어 딕셔너리 형태로 Key에 넣습니다.

    db.camping_site.insert_one(doc)
    # db에 저장하는 코드