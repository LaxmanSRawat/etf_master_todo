from flaskr.models import TaskStatusTypes, TaskPriorityTypes, MasterToDoList
import json
from uuid import uuid4
from sqlalchemy import text

def test_get_tasks_intially(client):
    """ TEST GET /tasks returns an empty list initially"""
    response = client.get('/tasks')
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

    test_task = {"task_title": "Test Task", "task_description": "My first test task", "priority_id": 1}

    response = client.post('/tasks', data = json.dumps(test_task), content_type = 'application/json')


    assert response.status_code == 200
    assert "message" in response.json
    assert "task_id" in response.json

def test_create_task_with_missing_fields(client):
    """ TEST POST /tasks fails when creating a task without body/missing required fields """
    response = client.post('/tasks', data = json.dumps({}), content_type = 'application/json')
    assert response.status_code == 400
    assert "error" in response.json

def test_get_tasks_after_creation(client,session):
    """ TEST GET /tasks and GET /task/<task_id> to get details after tasks are created"""
    
    #insert sample data - referencing status_id and priority_id from previous tests
    task_id = uuid4()
    task = MasterToDoList(id = task_id, task_title="Test Task", task_description="Test Task Description", status_id = 1, priority_id = 1)
    session.add(task)
    session.commit()

    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[1]["id"] == str(task_id)

    response = client.get(f'/tasks/{str(task_id)}')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["id"] == str(task_id)

def test_get_tasks_not_found(client):
    """ TEST GET /task/<task_id> to fail if task is not found with 404"""
    #insert sample data - referencing status_id and priority_id from previous tests
    task_id = uuid4()
    response = client.get(f'/tasks/{str(task_id)}')
    assert response.status_code == 404
    assert "error" in response.json

def test_put_tasks(client,session):
    """ TEST PUT /task/<task_id> to update task detail after task creation"""
    #insert sample data - referencing status_id and priority_id from previous tests
    task_id = uuid4()
    task = MasterToDoList(id = task_id, task_title="Test Task", task_description="Test Task Description", status_id = 1, priority_id = 1)
    session.add(task)
    session.commit()

    test_task = {"task_title": "New Task", "task_description": "New Test Task Description"}
    response = client.put(f'/tasks/{str(task_id)}', data = json.dumps(test_task), content_type = 'application/json')

    assert response.status_code == 200
    assert "message" in response.json
    
    #check updated details
    response = client.get(f'/tasks/{str(task_id)}')
    assert response.status_code == 200
    assert response.json[0]["task_title"] == "New Task"
    assert response.json[0]["task_description"] == "New Test Task Description"
    





