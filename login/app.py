# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- 데이터베이스 설정 ---
# 'site.db' 파일을 Flask 프로젝트의 루트 폴더에 생성하도록 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQL 쿼리를 콘솔에 출력하도록 설정 (디버깅용, 운영 환경에서는 False 권장)
app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)

# --- User 모델 정의 ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- 라우트 정의 ---

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            return jsonify({'success': True, 'message': '로그인 성공!'}), 200
        else:
            return jsonify({'success': False, 'message': '아이디 또는 비밀번호가 올바르지 않습니다.'}), 401
    else:
        return jsonify({'success': False, 'message': '잘못된 요청 형식입니다.'}), 400

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return jsonify({'success': False, 'message': '이미 존재하는 아이디입니다.'}), 409

            new_user = User(username=username)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return jsonify({'success': True, 'message': f'{username}님, 회원가입이 완료되었습니다!'}), 201
        else:
            return jsonify({'success': False, 'message': '잘못된 요청 형식입니다.'}), 400
    else:
        return render_template('signup.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
def logout():
    print("로그아웃 요청 수신됨.")
    return redirect(url_for('index'))

# --- 앱 실행 부분 ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)