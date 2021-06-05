# 지도 응답 코드

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.camping_map


@app.route('/')
def home():
    return render_template('index.html')


######################사전준비#########################

@app.route('/list', methods=['POST'])
def camping_info():
    sido_receive = request.form['sido_give']
    # 클라이언트에서 받은 시,도를 sido_receive라는 변수에 넣습니다.

    if sido_receive == '서울':
        regex = '^' + sido_receive
    elif sido_receive == '충청':
        regex = '^충청|충남|충북'
    elif sido_receive == '경상':
        regex = '^경상|경남|경북'
    elif sido_receive == '전라':
        regex = '^전라|전남|전북'
    elif sido_receive == '경기':
        regex = '^' + sido_receive
    elif sido_receive == '강원':
        regex = '^' + sido_receive
    elif sido_receive == '제주':
        regex = '^' + sido_receive
    # 파이썬 정규표현식을 사용하여, regex라는 변수에 '지역명'을 넣습니다.

    real_address = list(db.camping_site.find({'address': {'$regex': regex, '$options': 'i'}}, {'_id': 0}))
    # db에서 address가 regex인 데이터들을 찾아가져오고, real_address에 넣습니다.

    return jsonify({'result': 'success', 'list': real_address})
    #  성공 여부 & 캠핑장 목록 반환하기


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)