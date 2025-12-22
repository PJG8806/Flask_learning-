from flask_smorest import Blueprint, abort
from schemas import BookSchema
from flask.views import MethodView
from flask import Flask, request, jsonify

# 블루프린트 생성 books라는 이름으로 url 정보는 /books
blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# 데이터 저장소
books = []
id = 0

# id 증가후 반환
def next_id():
    global id
    id += 1
    return id

# 엔드포인트 구현...
@blp.route("/")
class Book_list(MethodView):    
    @blp.response(200)
    def get(self):
        return books
    
    # BookSchema로 요청 받은 json 값을 검증후 함수 인자로(딕셔너리) 넘겨준다
    @blp.arguments(BookSchema)
    # 함수 먼저 실행후 상태코드 201로 설정후 json 값으로 반환
    @blp.response(201, description="Book added")
    def post(self, new_data):
        new_data["id"] = next_id()
        if any(new_data["title"] == book["title"] for book in books):
            abort(400, message="title already exists")
        books.append(new_data)
        return new_data
    

@blp.route("/<int:book_id>")
class Book(MethodView):
    @blp.response(200)
    def get(self, book_id):
        # 조건을 만족하는 첫번째 값을 가져오는 제너레이터 컴프리헨션
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message = "Book not found")
        return book

    @blp.arguments(BookSchema)
    @blp.response(200, description="Book updated")
    def put(self, new_data, book_id):
        book = next((book for book in books if book["id"] == book_id), None)
        if book is None:
            abort(404, message = "Book not found")
        book.update(new_data)
        return book
    
    @blp.response(204, description="Book deleted")
    def delete(self, book_id):
        global books
        if not any(book for book in books if book["id"] == book_id):
            abort(404, message = "Book not found")
        books = [book for book in books if book["id"] != book_id]
        return