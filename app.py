from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.dpjbamc.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('signUp.html')

@app.route("/voyagegram99", methods=["POST"])
def voyagegram99_sign_up():
    user_id_receive = request.form['user_id_give']
    nick_name_receive = request.form['nick_name_give']
    name_receive = request.form['name_give']
    password_receive = request.form['password_give']

    doc = {
        'user_id': user_id_receive,
        'nick_name': nick_name_receive,
        'name': name_receive,
        'password': password_receive
    }
    db.user_info.insert_one(doc)
    return jsonify({'msg': '회원 가입 완료!'})

@app.route('/signup')
def move_to_signup():
    return render_template('signUp.html')

@app.route('/login')
def move_to_login():
    return render_template('login_voyage.html')

# @app.route('/html/<html_name>')
# def html(html_name):
#     return render_template(html_name)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)