from flask import Blueprint, request, jsonify
from flaskr.database import db_session
from flaskr.models import TaskStatusTypes
from sqlalchemy import select

#[ ] only accessible by admin
bp = Blueprint('task_status_types',__name__,url_prefix='/task_status_types')

@bp.route('', methods = ["GET","POST"])
def get_tasks():
    if request.method == 'GET':
        stmt = select(TaskStatusTypes)
        with db_session() as session:
            task_status_types = session.execute(stmt).scalars().all()
            result = [{"id": t.id, "status": t.status, "description": t.status_description} for t in task_status_types]
        return jsonify(result),200
    
    #else create new request
    data = request.get_json()

    if not data or "status" not in data or "status_description" not in data:
        return jsonify({"error": "Status and status description are required for creating task"}), 400

    new_status = TaskStatusTypes(
        status = data["status"],
        status_description = data["status_description"],
    )
    db_session.add(new_status)
    db_session.commit()
    return jsonify({"message":"Status created successfully", "status_id": str(new_status.id)}), 200

@bp.route('/<int:status_id>', methods = ["GET","PUT"])
def get_task(status_id):

    #find status type
    stmt = select(TaskStatusTypes).where(TaskStatusTypes.id == status_id)

    if request.method == 'PUT':
        #update the task details
        data = request.get_json()

        with db_session() as session:
            status_type = session.execute(stmt).scalar_one()
            if not status_type:
                return jsonify({"error": "Status type not found"}), 404
            if "status" in data:
                status_type.status = data["status"]
            if "status_description" in data:
                status_type.status_description = data["status_description"]
            db_session.add(status_type)
            db_session.commit()

        return jsonify({"message" : "Status type updated successfully"}), 200
    
    #else return task details
    with db_session() as session:
        status_type = session.execute(stmt).scalars().all()
        if not status_type:
            return jsonify({"error": "Status type not found"}), 404
        result = [{"id": t.id, "status": t.status, "status_description": t.status_description} for t in status_type]
    return jsonify(result),200


@bp.route('/initialize', methods = ["POST"])
def init_status_types():

    #[ ] truncate the table before hand
    #[ ] move to DB Migrate initialization

    not_started_status = TaskStatusTypes(
        id = 1,
        status = "Not Started",
        status_description = "This status means that the task's planned start date hasn\'t begin yet.",
    )
    in_progress_status = TaskStatusTypes(
        id = 2,
        status = "In Progress",
        status_description = "This status means that the task is currently active i.e. the planned start has passed and the task is not marked completed yet",
    )
    completed_status = TaskStatusTypes(
        id = 3,
        status = "Completed",
        status_description = "This status means that the task is completed",
    )
    cancelled_status = TaskStatusTypes(
        id =4,
        status = "Cancelled",
        status_description = "This status means that the task and corresponding child tasks have been cancelled",
    )

    deleted_status = TaskStatusTypes(
        id=5,
        status = "Deleted",
        status_description = "This status means that the task and corresponding child tasks have been deleted i.e. hidden for user",
    )
    
    db_session.add_all([not_started_status,in_progress_status,completed_status,cancelled_status,deleted_status])
    db_session.commit()

    return jsonify({"message":"Task Status Types are intialized successfully"}), 200
