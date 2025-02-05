from flask import Blueprint, jsonify, make_response, request
from .models.goal import Goal
from .routes_helper_functions import *
from app import db

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=("POST",))
def post_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        error_message(f"Invalid data", 400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.one_goal_to_dict()), 201

@goal_bp.route("", methods=("GET",))
def get_goals():

    goals = Goal.query.all()

    result_list = [goal.to_dict() for goal in goals]

    return jsonify(result_list), 200

@goal_bp.route("/<goal_id>", methods=("GET",))
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return jsonify(goal.one_goal_to_dict()), 200

@goal_bp.route("/<goal_id>", methods=("PUT",))
def put_one_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.replace_details(request_body)

    db.session.commit()

    return jsonify(goal.one_goal_to_dict()), 200

@goal_bp.route("/<goal_id>", methods=("DELETE",))
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'))), 200

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    request_body = request.get_json()

    goal = validate_goal(goal_id)

    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        task.goal = goal

    db.session.commit()

    return make_response(jsonify({"id": goal.goal_id, "task_ids": request_body["task_ids"]})), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks_dict = [task.to_dict() for task in goal.tasks]

    result = goal.to_dict()
    result["tasks"] = tasks_dict

    return jsonify(result), 200
