# app.py

from flask import Flask, render_template, request, jsonify, redirect, url_for, session # session 추가 확인
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps # login_required 데코레이터 사용을 위해 필요

app = Flask(__name__)

# --- 데이터베이스 설정 (이전과 동일) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False # 실제 SQL 쿼리를 콘솔에 볼지 말지 (디버깅 시 True, 운영 시 False)

# --- 세션 설정을 위한 SECRET_KEY (매우 중요! 반드시 복잡하게 설정) ---
app.config['SECRET_KEY'] = 'your_secret_key_very_secret_and_random' # 실제 운영에서는 더 복잡한 값으로!

db = SQLAlchemy(app)

# --- User 모델 정의 (이전과 동일) ---
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

# --- 데이터베이스 초기화 (이전과 동일) ---
with app.app_context():
    db.create_all()

# --- 로그인 필요 데코레이터 (이전과 동일) ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# --- 라우트 정의 (기존 라우트들) ---

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
            session['logged_in'] = True
            session['username'] = username # 로그인한 사용자 이름 세션에 저장
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
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None) # 사용자 이름도 세션에서 제거
    print("로그아웃 요청 수신됨.")
    return redirect(url_for('index'))

# --- ★ 새로 추가된 회원 탈퇴 관련 라우트 ★ ---

@app.route('/exit') # 회원 탈퇴 페이지 보여주기
@login_required # 로그인한 사용자만 접근 가능
def exit_page():
    return render_template('exit.html')

@app.route('/delete_account', methods=['POST']) # 회원 탈퇴 처리 요청 받기
@login_required # 로그인한 사용자만 처리 가능
def delete_account():
    if request.is_json:
        data = request.get_json()
        password = data.get('password') # 사용자가 입력한 비밀번호

        # 현재 로그인된 사용자의 아이디를 세션에서 가져옴
        username = session.get('username')
        if not username: # 세션에 사용자 이름이 없으면 오류 (로그인 상태 이상)
            return jsonify({'success': False, 'message': '로그인 정보가 유효하지 않습니다.'}), 401

        user = User.query.filter_by(username=username).first()

        # 사용자 존재 여부 및 비밀번호 일치 여부 확인
        if user and user.check_password(password):
            db.session.delete(user) # 데이터베이스에서 사용자 삭제
            db.session.commit()     # 변경사항 저장

            # 세션 정보 삭제 (로그아웃 처리)
            session.pop('logged_in', None)
            session.pop('username', None)

            return jsonify({'success': True, 'message': '회원 탈퇴가 완료되었습니다. 안녕히 계세요!'}), 200
        else:
            return jsonify({'success': False, 'message': '비밀번호가 올바르지 않습니다.'}), 401
    else:
        return jsonify({'success': False, 'message': '잘못된 요청 형식입니다.'}), 400

# --- 앱 실행 부분 (이전과 동일) ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)