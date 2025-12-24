from flask import Flask, render_template, request, redirect, session, flash #flash redirect 하기전 안내메시지 뛰어주는거
# session 쿠키에 세션 정보를 가지고 로그인 로그아웃 같은 정보 유지 효과를 가능하다
from datetime import timedelta

app = Flask(__name__)

app.secret_key = 'flask-secret-key' # 실제로 배포시에는 .env or yaml 저장해서 사용
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) #세션 정보가 7일동안 유지됨


users = {
  'john': 'pw123',
  'leo': 'pw123'
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username #유저 이름으로 세션 생성

        return redirect('/secret')
    else:
        flash('Invalid username or password')
        return redirect('/')
    
@app.route('/secret')
def secret():
    if 'username' in session: # 세션에 유저 정보가 들어오면
        return render_template('secret.html')
    else:
        return redirect('/')
    
# 로그아웃
@app.route('/logout')
def logout():
    session.pop('username', None)# 세션 정보를 삭제
    session.clear() # 세션 정보를 더 깔끔하게 삭제
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)