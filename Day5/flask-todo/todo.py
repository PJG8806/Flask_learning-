from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Todo, User, db

todo_blp = Blueprint('todo', 'todo', user_prefix='/todo', description='Operations on todos')

@todo_blp.route('/', methods=['POST'])
@jwt_required()# 인증된 사용자만 접근
def create_todo():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    title = request.json.get('title', None)
    if not title:
        return jsonify({"msg": "Missing title"}), 400
    
    username = get_jwt_identity() #값을 불러오는 부분
    user = User.query.filter_by(username=username).first()

    new_todo = Todo(title=title, user_id=user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"msg": "Todo created", "id": new_todo.id}), 201

@todo_blp.route('/', methods=['GET'])
@jwt_required()
def get_todos():
    username = get_jwt_identity() # 문서의 전체 정보를 가져온다
    user = User.query.filter_by(username=username).first()
    todos = Todo.query.filter_by(user_id=user.id).all()
    return jsonify([{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos])

@todo_blp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if 'title' in request.json:
        todo.title = request.json['title']
    db.session.commit()
    return jsonify({"msg": "Todo updated", "id": todo.id})

@todo_blp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"msg": "Todo delete", "id": todo_id})
