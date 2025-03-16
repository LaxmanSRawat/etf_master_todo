from flask import Blueprint, request, jsonify
from flaskr.database import db_session
from flaskr.models import MasterToDoList,TaskStatusTypes,TaskPriorityTypes
from sqlalchemy import select
import datetime
from uuid import uuid4

bp = Blueprint('tasks',__name__, url_prefix='/tasks')

@bp.route('', methods = ["GET","POST"])
def get_tasks():
    # result = MasterToDoList.query.all()
    if request.method == 'GET':
        stmt = select(MasterToDoList,TaskStatusTypes,TaskPriorityTypes).join_from(MasterToDoList,TaskStatusTypes).join_from(MasterToDoList,TaskPriorityTypes)
        with db_session() as session:
            tasks = session.execute(stmt).scalars().all()
            result = [{"id": t.id, "task_title" : t.task_title, "task_description" : t.task_description, "status_id" : t.status_id, "priority_id" : t.priority_id, "planned_start_date" : t.planned_start_date, "planned_end_date" : t.planned_end_date, "completed_on" : t.completed_on, "created_on" : t.created_on, "modified_on": t.modified_on } for t in tasks]
        return jsonify(result),200
    
    #else create new request
    data = request.get_json()

    if not data or "task_title" not in data or "task_description" not in data or "priority_id" not in data:
        return jsonify({"error": "task_title, task_description, status_id and priority_id are required for creating task"}), 400


    with db_session() as session:
        stmt = select(TaskStatusTypes).where(TaskStatusTypes.status == 'Not Started')
        not_started_status = session.execute(stmt).scalars().first()
        if not not_started_status:
            return jsonify({"error": "not started status not initiated"}), 500
        not_started_status_id = not_started_status.id

    #[ ] whitelist allowed priority types
    
    new_task = MasterToDoList(
        task_title = data["task_title"],
        task_description = data["task_description"],
        status_id = not_started_status_id,
        priority_id = data["priority_id"],
        planned_start_date = data.get("planned_start_date"),
        planned_end_date= data.get("planned_end_date"),
        completed_on=data.get("completed_on"),
    )
    db_session.add(new_task)
    db_session.commit()
    return jsonify({"message":"Task created successfully", "task_id": str(new_task.id)}), 200

@bp.route('/<uuid:task_id>', methods = ["GET","PUT"])
def get_task(task_id):
    stmt = select(MasterToDoList).where(MasterToDoList.id == task_id)
    if request.method == 'PUT':
        #update the task details
        data = request.get_json()
        with db_session() as session:
            #find task
            task = session.execute(stmt).scalar_one()
            if not task:
                return jsonify({"error": "task not found"}), 404
            if "task_title" in data:
                task.task_title = data["task_title"]
            if "task_description" in data:
                task.task_description = data["task_description"]
            if "status_id" in data:
                #[ ] whitelist allowed status types
                task.status_id = data["status_id"]
            if "priority_id" in data:
                #[ ] whitelist allowed priority types
                task.priority_id = data["priority_id"]
            if "planned_start_date" in data:
                task.planned_start_date = data["planned_start_date"]
            if "planned_end_date" in data:
                task.planned_end_date = data["planned_end_date"]
            if "completed_on" in data:
                task.completed_on = data["completed_on"]
            
            #[ ] standardize the datetime used everywhere
            task.modified_on = datetime.datetime.now(datetime.timezone.utc)
            db_session.add(task)
            db_session.commit()  
        return jsonify({"message" : "Task updated successfully"}), 200
    
    #else return task details
    #find task
    with db_session() as session:
        task = session.execute(stmt).scalars().all()
        if not task:
            return jsonify({"error": "task not found"}), 404
        result = [{"id": t.id, "task_title" : t.task_title, "task_description" : t.task_description, "status_id" : t.status_id, "priority_id" : t.priority_id, "planned_start_date" : t.planned_start_date, "planned_end_date" : t.planned_end_date, "completed_on" : t.completed_on, "created_on" : t.created_on, "modified_on": t.modified_on } for t in task]

    return jsonify(result),200
    
    


