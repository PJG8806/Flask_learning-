from flask import Flask, render_template
from jwt_utils import configure_jwt  # JWT 설정 함수를 임포트합니다.
from routes.user import user_bp

app = Flask(__name__)
#from flask_jwt_extended import JWTManager jwt_tuils의 configure_jwt(app)에서 정의를 해서 없어도 된다
# app.config['JWT_SECRET_KEY] = 'jwt-secret-key' 요것도
#jwt = JWTManager(app) 요것도
configure_jwt(app)  # JWT 관련 추가 설정을 적용합니다.
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)