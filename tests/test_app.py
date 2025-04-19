import pytest
import json
import os
import sys
from app import app, db, Todo

# Add the parent directory to sys.path to import the main application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Todo List' in response.data

def test_add_task(client):
    response = client.post('/add', data=dict(content='Test task'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Test task' in response.data

def test_delete_task(client):
    # Add a task first
    client.post('/add', data=dict(content='Test delete task'))
    
    # Get the task to find its ID
    with app.app_context():
        task = Todo.query.filter_by(content='Test delete task').first()
        
    # Delete the task
    response = client.get(f'/delete/{task.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Test delete task' not in response.data

def test_complete_task(client):
    # Add a task first
    client.post('/add', data=dict(content='Test complete task'))
    
    # Get the task to find its ID
    with app.app_context():
        task = Todo.query.filter_by(content='Test complete task').first()
        assert not task.completed
        
    # Complete the task
    client.get(f'/complete/{task.id}', follow_redirects=True)
    
    # Check that it's completed
    with app.app_context():
        task = Todo.query.filter_by(content='Test complete task').first()
        assert task.completed

def test_api_get_tasks(client):
    # Add some tasks
    client.post('/add', data=dict(content='API test task 1'))
    client.post('/add', data=dict(content='API test task 2'))
    
    # Get tasks via API
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['content'] == 'API test task 1'
    assert data[1]['content'] == 'API test task 2'

def test_api_create_task(client):
    response = client.post('/api/tasks', 
                          json={'content': 'API created task'},
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['content'] == 'API created task'