from flaskr.models import TaskStatusTypes
import json
from sqlalchemy import select, text

def test_get_task_status_types_intially(client):
    """ TEST GET /task_status_types returns an empty list initially"""
    response = client.get('/task_status_types')
    assert response.status_code == 200
    assert response.json == []

def test_create_task_status_type(client,session):
    """ TEST POST /task_status_types creates task status type"""
    
    test_task_status_type = {"status": "Not Started", "status_description": "Not Started Test Task Status Type Descrption"}

    response = client.post('/task_status_types', data = json.dumps(test_task_status_type), content_type = 'application/json')


    assert response.status_code == 200
    assert "message" in response.json
    assert "status_id" in response.json

    response = client.get('/task_status_types')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["id"] == 1

def test_create_task_with_missing_fields(client):
    """ TEST POST /task_status_types fails when creating a status without body/missing required fields """
    response = client.post('/task_status_types', data = json.dumps({}), content_type = 'application/json')
    assert response.status_code == 400
    assert "error" in response.json

def test_get_task_status_type_after_creation(client,session):
    """ TEST GET /task_status_types and GET /task_status_types/<status_id> to get details after task status types are created"""
    
    result = session.execute(select(TaskStatusTypes)).scalars().all()
    #insert sample data 
    status_id = 2
    task_status_type = TaskStatusTypes(id = status_id, status="In Progress", status_description="In Progress Test Task Status Type Description")
    session.add(task_status_type)
    session.commit()

    response = client.get('/task_status_types')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[1]["id"] == status_id

    response = client.get(f'/task_status_types/{str(status_id)}')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["id"] == status_id

def test_get_task_status_type_not_found(client):
    """ TEST GET /task_status_types/<status_id> to fail if task status type is not found with 404"""
    #insert sample data 
    status_id = 3
    response = client.get(f'/task_status_types/{str(status_id)}')
    assert response.status_code == 404
    assert "error" in response.json

def test_put_task_status_type(client,session):
    """ TEST PUT /task_status_types/<status_id>  to update task detail after task creation"""
    #insert sample data 
    status_id = 3
    task_status_type = TaskStatusTypes(id = status_id, status="Completed", status_description="Completed Test Task Status Type Description")
    session.add(task_status_type)
    session.commit()

    test_task_status_type = {"status": "Cancelled", "status_description": "Cancelled New Test Task Status Type Description"}
    response = client.put(f'/task_status_types/{str(status_id)}', data = json.dumps(test_task_status_type), content_type = 'application/json')

    assert response.status_code == 200
    assert "message" in response.json
    
    #check updated details
    response = client.get(f'/task_status_types/{str(status_id)}')
    assert response.status_code == 200
    assert response.json[0]["status"] == "Cancelled"
    assert response.json[0]["status_description"] == "Cancelled New Test Task Status Type Description"
    
def test_post_init_status_types(client,session):
    """ TEST PUT /initialize to initialize with default status types"""

    #truncate table
    session.execute(text("DELETE FROM task_status_types"))

    response = client.post('/task_status_types/initialize')
    assert response.status_code == 200
    assert "message" in response.json

    #check initialized rows 
    response = client.get(f'/task_status_types/1')
    assert response.status_code == 200
    assert response.json[0]["status"] == "Not Started"

    response = client.get(f'/task_status_types/2')
    assert response.status_code == 200
    assert response.json[0]["status"] == "In Progress"

    response = client.get(f'/task_status_types/3')
    assert response.status_code == 200
    assert response.json[0]["status"] == "Completed"

    response = client.get(f'/task_status_types/4')
    assert response.status_code == 200
    assert response.json[0]["status"] == "Cancelled"

    response = client.get(f'/task_status_types/5')
    assert response.status_code == 200
    assert response.json[0]["status"] == "Deleted"
    
    




