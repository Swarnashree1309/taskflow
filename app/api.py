from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task

api_bp = Blueprint("api", __name__)


@api_bp.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@api_bp.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    due_date = None
    if data.get("due_date"):
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        category=data.get("category", "General"),
        priority=data.get("priority", "Medium"),
        status=data.get("status", "Pending"),
        due_date=due_date,
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.category = data.get("category", task.category)
    task.priority = data.get("priority", task.priority)
    task.status = data.get("status", task.status)
    if data.get("due_date"):
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    db.session.commit()
    return jsonify(task.to_dict())


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return "", 204


@api_bp.route("/stats", methods=["GET"])
@login_required
def get_stats():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    stats = {
        "total": len(tasks),
        "pending": len([t for t in tasks if t.status == "Pending"]),
        "in_progress": len([t for t in tasks if t.status == "In Progress"]),
        "done": len([t for t in tasks if t.status == "Done"]),
        "high_priority": len([t for t in tasks if t.priority == "High"]),
    }
    return jsonify(stats)
