import pytest
from flask import url_for
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_existing_user(client):
    user = User(username='hero')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={'username': 'hero'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Welcome back, adventurer' in response.data

def test_login_new_user(client):
    response = client.post('/login', data={'username': 'newbie'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Welcome to QuestLog!' in response.data

    user = User.query.filter_by(username='newbie').first()
    assert user is not None

def test_logout(client):
    # Log in first to access logout
    user = User(username='logout_hero')
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={'username': 'logout_hero'}, follow_redirects=True)

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Goodbye for now' in response.data
