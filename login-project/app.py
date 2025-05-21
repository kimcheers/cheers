from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_id = request.form.get('id')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

        print(f"아이디: {user_id}")
        print(f"비밀번호: {password}")
        print(f"비밀번호 확인: {password_check}")

        if password == password_check:
            print("비밀번호가 일치합니다.")
            
            try:
                with open('users.txt', 'a') as f:
                    f.write(f"USER={user_id}\n PW={password}\n----------------")
                return jsonify({'message': '회원가입 성공!'}), 200
            except Exception as e:
                print(f"파일 저장 오류: {e}")
                return jsonify({'error': '회원 정보 저장에 실패했습니다.'}), 500
        else:
            print("비밀번호가 일치하지 않습니다.")
            return jsonify({'error': '비밀번호가 일치하지 않습니다.'}), 400


@app.route('/')
def index():
    return render_template('login.html')# url 실행시 index.html실행

@app.route('/login')
def show_index():
    return render_template('login.html')

@app.route('/signup')
def show_signup():
    return render_template('signup.html')

@app.route('/findid')
def show_find_id():
    return render_template('findid.html')

@app.route('/Resetpw')
def show_reset_pw():
    return render_template('resetpw.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)