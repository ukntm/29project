from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# DB 연결
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.dpjbamc.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


@app.route('/')
def home():
    return render_template('login_voyage.html')

# 회원가입 API
@app.route("/voyagegram99/register", methods=["POST"])
def voyagegram99_sign_up():
    # 아이디, 닉네임, 이름, 비밀번호를 request로 받아서 db에 저장
    user_id_receive = request.form['user_id_give']
    nick_name_receive = request.form['nick_name_give']
    name_receive = request.form['name_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    # db에 이미 같은 id가 존재한다 -> result : fail, msg : 같은 아이디가 존재합니다.
    user = db.user_info.find_one({'user_id': user_id_receive})
    nick = db.user_info.find_one({'nick_name': nick_name_receive})
    teugsu_word = ['!' , '#' , '$' , '%' , '^' , '&' , '*' , '(' , ')' , '_' , '+' , '=' , '-' , '`' , '~' , '/' , '|' , "'" , '\\', '"' ]

    msg = ''
    result = 'success'

    # 공통 제약조건
    for t in teugsu_word:  # 특수 문자 입력
        if t in user_id_receive:
            msg = '특수문자는 입력못합니다.'
            result = 'fail'
        if t in nick_name_receive:
            msg = '특수문자는 입력못합니다.'
            result = 'fail'
        if t in name_receive:
            msg = '특수문자는 입력못합니다.'
            result = 'fail'

    # user id 관련 제약조건
    if user_id_receive == '':                       # 입력을 안함
        msg = '이메일을 입력해주세요'
        result = 'fail'
    else:
        if not(user_id_receive.count('@') == 1):    # '@'이 없거나 두개이상일 때
            msg = '이메일 형식이 잘못되었습니다.'
            result = 'fail'
        if user is not None:                        # 이메일 중복체크
            msg = '중복된 이메일이 존재합니다.'
            result = 'fail'


    # nick_name 관련 제약조건
    if nick_name_receive == '':                     # 입력을 안함
        msg = '닉네임을 입력해주세요'
        result = 'fail'
    else:
        if nick is not None:                        # 닉네임 중복체크
            msg = '중복된 닉네임이 존재합니다.'
            result = 'fail'

    # name 관련 제약조건
    if name_receive == '':                          # 입력을 안함
        msg = '이름을 입력해주세요'
        result = 'fail'

    # 비밀번호 관련 제약조건
    if password_receive == '':                      # 입력을 안함
        msg = '비밀번호를 입력해주세요'
        result = 'fail'
    else:
        if len(password_receive) < 8:               # 비밀번호 8자리 이하
            msg = '비밀번호가 너무 짧습니다'
            result = 'fail'


    # casplock 켜져있으면 알람
    # 모두 거친후 실행
    if result == 'success':
        doc = {
            'user_id': user_id_receive,
            'nick_name': nick_name_receive,
            'name': name_receive,
            'password': pw_hash
        }

        db.user_info.insert_one(doc)

    return jsonify({ 'result' : result, 'msg' : msg })

# ## 로그인 작업중
# @app.route("/voyagegram99/login", methods=["POST"])
# def voyagegram99_sign_in():
#     user_id_receive = request.form['user_id_give']
#     password_receive = request.form['password_give']


## render_page
@app.route('/signup')
def move_to_signup():
    return render_template('signUp.html')

@app.route('/login')
def move_to_login():
    return render_template('login_voyage.html')

@app.route('/main')
def move_to_mainPage():
    return render_template('mainpage.html')

# @app.route('/html/<html_name>')
# def html(html_name):
#     return render_template(html_name)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

