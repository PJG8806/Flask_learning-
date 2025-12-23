from flask import Flask
from flask_smorest import Api
from api import blp

app = Flask(__name__)

# OpenAPI 관련 설정
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
# 위 항목은 필수 설정
app.config["OPENAPI_URL_PREFIX"] = "/" # 기본 경로 설정
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # http://127.0.0.1:5000/swagger-ui 접속시 swagger 문서를 웹으로 보는 주소 설정
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # swagger ui의 js/css 파일을 어디서 가져올지 지정하는 설정

api = Api(app)
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)