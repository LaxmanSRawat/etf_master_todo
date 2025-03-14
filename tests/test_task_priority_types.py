from flaskr.models import TaskPriorityTypes
import json
from sqlalchemy import select, text

def test_get_task_priority_types_intially(client):
    """ TEST GET /task_priority_types returns an empty list initially"""
    response = client.get('/task_priority_types')
    assert response.status_code == 200
    assert response.json == []

def test_create_task_priority_type(client,session):
    """ TEST POST /task_priority_types creates task priority type"""
    
    test_task_priority_type = {"priority": "Critical", "priority_description": "Critical Test Task Priority Type Descrption"}

    response = client.post('/task_priority_types', data = json.dumps(test_task_priority_type), content_type = 'application/json')


    assert response.status_code == 200
    assert "message" in response.json
    assert "priority_id" in response.json

    response = client.get('/task_priority_types')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["id"] == 1

def test_create_task_with_missing_fields(client):
    """ TEST POST /task_priority_types fails when creating a priority without body/missing required fields """
    response = client.post('/task_priority_types', data = json.dumps({}), content_type = 'application/json')
    assert response.status_code == 400
    assert "error" in response.json

def test_get_task_priority_type_after_creation(client,session):
    """ TEST GET /task_priority_types and GET /task_priority_types/<priority_id> to get details after task priority types are created"""
    
    result = session.execute(select(TaskPriorityTypes)).scalars().all()
    #insert sample data 
    priority_id = 2
    task_priority_type = TaskPriorityTypes(id = priority_id, priority="High", priority_description="High Test Task Priority Type Description")
    session.add(task_priority_type)
    session.commit()

    response = client.get('/task_priority_types')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[1]["id"] == priority_id

    response = client.get(f'/task_priority_types/{str(priority_id)}')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["id"] == priority_id

def test_get_task_priority_type_not_found(client):
    """ TEST GET /task_priority_types/<priority_id> to fail if task priority type is not found with 404"""
    #insert sample data 
    priority_id = 3
    response = client.get(f'/task_priority_types/{str(priority_id)}')
    assert response.status_code == 404
    assert "error" in response.json

def test_put_task_priority_type(client,session):
    """ TEST PUT /task/<task_id> to update task detail after task creation"""
    #insert sample data 
    priority_id = 3
    task_priority_type = TaskPriorityTypes(id = priority_id, priority="Medium", priority_description="Medium Test Task Priority Type Description")
    session.add(task_priority_type)
    session.commit()

    test_task_priority_type = {"priority": "Low", "priority_description": "Low New Test Task Priority Type Description"}
    response = client.put(f'/task_priority_types/{str(priority_id)}', data = json.dumps(test_task_priority_type), content_type = 'application/json')

    assert response.status_code == 200
    assert "message" in response.json
    
    #check updated details
    response = client.get(f'/task_priority_types/{str(priority_id)}')
    assert response.status_code == 200
    assert response.json[0]["priority"] == "Low"
    assert response.json[0]["priority_description"] == "Low New Test Task Priority Type Description"


def test_post_init_priority_types(client,session):
    """ TEST PUT /task_priority_types/initialize to initialize with default priority types"""

    #truncate table
    session.execute(text("DELETE FROM task_priority_types"))

    response = client.post('/task_priority_types/initialize')
    assert response.status_code == 200
    assert "message" in response.json

    #check initialized rows 
    response = client.get(f'/task_priority_types/1')
    assert response.status_code == 200
    assert response.json[0]["priority"] == "Critical"

    response = client.get(f'/task_priority_types/2')
    assert response.status_code == 200
    assert response.json[0]["priority"] == "High"

    response = client.get(f'/task_priority_types/3')
    assert response.status_code == 200
    assert response.json[0]["priority"] == "Medium"

    response = client.get(f'/task_priority_types/4')
    assert response.status_code == 200
    assert response.json[0]["priority"] == "Low"

    response = client.get(f'/task_priority_types/5')
    assert response.status_code == 200
    assert response.json[0]["priority"] == "Lowest"




