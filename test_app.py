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
    assert rv.json['courses'] == []

"""
def test_db(client):
    client.post('/api/course', json={
        'coursename': 'underwater basket weaving',
        'startdate': '2021-05-01',
        'finishdate': '2021-11-01',
        'numberlectures': 42
    })
    resp = client.get('/api/course')
    assert len(resp.json['courses']) == 1
"""
if __name__ == '__main__':
    pass