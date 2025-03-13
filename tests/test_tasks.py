from flaskr.models import TaskStatusTypes, TaskPriorityTypes
import json
from sqlalchemy import select

def test_get_tasks(client):
    """ TEST GET /tasks returns an empty list initially"""
    response = client.get('/tasks')
    print(response.json)
    assert response.status_code == 200
    assert response.json == []

def test_create_task(client,session):
    """ TEST POST /tasks creates task"""
    #Insert required status and priority data first
    not_started_status = TaskStatusTypes(
        id = 1,
        status = "Not Started",
        status_description = "This status means that the task's planned start date hasn\'t begin yet.",
    )
    critical_priority = TaskPriorityTypes(
        id = 1,
        priority = "Critical",
        priority_description = "These are your “drop everything” tasks. They're both urgent and important, often involving crisis management or critical deadlines.",
    )
    session.add_all([not_started_status, critical_priority])
    session.commit()

    print(session.execute(select(TaskPriorityTypes)))
    print(session.execute(select(TaskStatusTypes)))

    test_task = {"task_title": "Test Task", "task_description": "My first test task", "priority_id": 1}

    response = client.post('/tasks', data = json.dumps(test_task), content_type = 'application/json')

    assert response.status_code == 200
    assert "message" in response.json
    assert "task_id" in response.json
