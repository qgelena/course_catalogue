from datetime import date

from flask_sqlalchemy import SQLAlchemy
import pytest

import courseapp
import models

@pytest.fixture
def client():
    app = courseapp.create_app()
    app.config['TESTING'] = True

    with app.app_context():
        try:
            models.db.init_app(app)
            models.db.create_all()
            with app.test_client() as client:
                yield client
        finally:
            models.db.drop_all()

def test_empty_db(client):
    rv = client.get('/api/course')
    assert rv.status_code == 200
    assert rv.json['courses'] == []

def test_db(client):
    resp = client.post('/api/course', json={
        'coursename': 'underwater basket weaving',
        'startdate': '2021-05-01',
        'finishdate': '2021-11-01',
        'numberlectures': 42
    })
    assert resp.status_code == 200

    resp = client.get('/api/course')
    assert resp.status_code == 200
    courses = resp.json['courses']
    assert len(courses) == 1
    assert courses[0]['coursename'] == 'underwater basket weaving'


if __name__ == '__main__':
    pass