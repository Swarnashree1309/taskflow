from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)


@main_bp.route("/tasks")
@login_required
def tasks_page():
    return render_template("tasks.html", username=current_user.username)
