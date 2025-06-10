from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('default.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    return jsonify({
        'success': True,
        'message': '로그인 성공!',
        'user': username,
        'redirect': '/dashboard'
    })

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    return jsonify({
        'success': True,
        'message': '회원가입 성공!',
        'user': username,
        'redirect': '/login'
    })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    return jsonify({
        'success': True,
        'message': '로그아웃 되었습니다.',
        'redirect': '/login'
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
