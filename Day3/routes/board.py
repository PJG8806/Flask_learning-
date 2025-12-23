from flask import request, jsonify
from flask.views import MethodView # http 메서드(GET, POST, PUT, DELETE) 클래스 단위로 묶어주는거
from flask_smorest import Blueprint
from db import db
from models import Board

board_blp = Blueprint('Boards', 'boards', description='Operations on boards', url_prefix='/board')

# /board
@board_blp.route('/')
class BoardList(MethodView):
    # 전체 게이글 불러오기 (GET)
    def get(self):
        # 데이터가 있으면 <Board 1> 데이터가 들어온다
        boards = Board.query.all()
        return jsonify([{"user_id": board.user_id, 
                         "id": board.id,
                         "title": board.title, "content": board.content, "author": board.author.name} for board in boards])

    # 게시글 작성 (POST)
    def post(self):
        data = request.json
        new_board = Board(title=data['title'], content=data['content'], user_id=data['user_id'])
        db.session.add(new_board)
        db.session.commit()
        return jsonify({"message": "Board created"}), 201


# /board<int: board_id>
@board_blp.route('/<int:board_id>')
class BoardResource(MethodView):
    # 하나의 게시글 불러오기 (GET)
    def get(self, board_id):
        board = Board.query.get_or_404(board_id)
        return jsonify({"title": board.title, "content": board.content, "author": board.author.name})

    # 특정 게시글 수정하기 (PUT)
    def put(self, board_id):
        board = Board.query.get_or_404(board_id)
        data = request.json
        board.title = data['title']
        board.content = data['content']
        db.session.commit()
        return jsonify({"message": "Board updated"})

    # 특정 게시글 삭제하기 (DELETE)
    def delete(self, board_id):
        board = Board.query.get_or_404(board_id)
        db.session.delete(board)
        db.session.commit()
        return jsonify({"message": "Board deleted"})