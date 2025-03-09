from flask import Blueprint, request, jsonify
from flaskr.database import db_session
from flaskr.models import TaskPriorityTypes
from sqlalchemy import select

#todo only accessible by admin
bp = Blueprint('task_priority_types',__name__,url_prefix='/task_priority_types')

@bp.route('/', methods = ["GET","POST"])
def get_tasks():
    if request.method == 'GET':
        stmt = select(TaskPriorityTypes)
        with db_session() as session:
            task_priority_types = session.execute(stmt).scalars().all()
            result = [{"id": p.id, "priority": p.priority, "description": p.priority_description} for p in task_priority_types]
        return jsonify(result),200
    
    #else create new request
    data = request.get_json()

    if not data or "priority" not in data or "priority_description" not in data:
        return jsonify({"error": "Priority and priority description are required for creating task"}), 400

    new_priority = TaskPriorityTypes(
        priority = data["priority"],
        priority_description = data["priority_description"],
    )
    db_session.add(new_priority)
    db_session.commit()
    return jsonify({"message":"Priority created successfully", "task_id": str(new_priority.id)}), 200

@bp.route('/<int:priority_id>', methods = ["GET","PUT"])
def get_task(priority_id):

    #find priority type
    stmt = select(TaskPriorityTypes).where(TaskPriorityTypes.id == priority_id)
    with db_session() as session:
        priority_type = session.execute(stmt)
        if not priority_type:
            return jsonify({"error": "Priority type not found"}), 404
        result = [{"id": p.id, "priority": p.priority, "description": p.priority_description} for p in priority_type]
    
    
    if request.method == 'PUT':
        #update the task details
        data = request.get_json()

        if "priority" in data:
            priority_type.priority = data["priority"]
        if "priority_description" in data:
            priority_type.priority_description = data["priority_description"]

        db_session.commit()

        return jsonify({"message" : "Priority type updated successfully"}), 200
    
    #else return task details
    return jsonify(result),200

@bp.route('/initialize', methods = ["POST"])
def init_priority_types():

    #todo truncate the table before hand
    #todo move to DB Migrate initialization

    critical_priority = TaskPriorityTypes(
        id = 1,
        priority = "Critical",
        priority_description = "These are your “drop everything” tasks. They're both urgent and important, often involving crisis management or critical deadlines.",
    )
    high_priority = TaskPriorityTypes(
        id = 2,
        priority = "High",
        priority_description = "Important tasks that are not immediately urgent. These often contribute significantly to long-term goals.",
    )
    medium_priority = TaskPriorityTypes(
        id = 3,
        priority = "Medium",
        priority_description = "Tasks that are urgent but less important. They require attention but don't contribute as much to overall objectives.",
    )
    low_priority = TaskPriorityTypes(
        id =4,
        priority = "Low",
        priority_description = "Neither urgent nor highly important. These tasks should be done but can be scheduled for later.",
    )

    lowest_priority = TaskPriorityTypes(
        id=5,
        priority = "Lowest",
        priority_description = " Tasks with minimal impact that can be eliminated if necessary.",
    )
    
    db_session.add(critical_priority)
    db_session.add(high_priority)
    db_session.add(medium_priority)
    db_session.add(low_priority)
    db_session.add(lowest_priority)
    db_session.commit()

    return jsonify({"message":"Task Priority Types are intialized successfully"}), 200
