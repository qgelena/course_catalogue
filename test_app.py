from datetime import date

from flask_sqlalchemy import SQLAlchemy
import pytest

import courseapp
import models

COURSE_WEAVING = {
    'coursename': 'underwater basket weaving',
    'startdate': '2021-05-01',
    'finishdate': '2021-11-01',
    'numberlectures': 42
}

SNOW_ZORBING = {
    'coursename': 'snow zorbing',
    'startdate': '2021-01-01',
    'finishdate': '2021-02-15',
    'numberlectures': 15
}

HILL_ZORBING = {
    'coursename': 'hill zorbing',
    'startdate': '2021-03-01',
    'finishdate': '2021-05-01',
    'numberlectures': 12
}

UNDERWATER_EXTREME_IRONING = {
    'coursename': 'underwater extreme ironing',
    'startdate': '2021-06-01',
    'finishdate': '2021-07-17',
    'numberlectures': 20
}

PARACHUTE_EXTREME_IRONING = {
    'coursename': 'parachute extreme ironing',
    'startdate': '2021-06-01',
    'finishdate': '2021-08-31',
    'numberlectures': 34
}

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
    resp = client.post('/api/course', json=COURSE_WEAVING)
    assert resp.status_code == 200

    resp = client.get('/api/course')
    assert resp.status_code == 200
    courses = resp.json['courses']
    assert len(courses) == 1
    assert courses[0]['coursename'] == 'underwater basket weaving'

def test_info(client):
    # test non-existing course id
    resp = client.get('/api/course/1')
    assert resp.status_code == 404

    # create a course and remember its id
    resp = client.post('/api/course', json=COURSE_WEAVING)
    assert resp.status_code == 200
    course_id = resp.json['course_id']
    # get its info back
    resp = client.get('/api/course/' + str(course_id))
    assert resp.status_code == 200
    assert resp.json['coursename'] == COURSE_WEAVING['coursename']
    assert resp.json['numberlectures'] == COURSE_WEAVING['numberlectures']

def test_delete(client):
    resp = client.post('/api/course', json=COURSE_WEAVING)
    assert resp.status_code == 200
    course_id = resp.json['course_id']

    resp = client.delete(f'/api/course/{course_id}')
    assert resp.status_code == 200

    resp = client.delete(f'/api/course/{course_id}')
    assert resp.status_code == 404

def test_search_by_name(client):
    assert client.post('/api/course', json=COURSE_WEAVING).status_code == 200
    assert client.post('/api/course', json=HILL_ZORBING).status_code == 200
    assert client.post('/api/course', json=SNOW_ZORBING).status_code == 200
    assert client.post('/api/course', json=PARACHUTE_EXTREME_IRONING).status_code == 200
    assert client.post('/api/course', json=UNDERWATER_EXTREME_IRONING).status_code == 200

    resp = client.post('/api/course/search', json='zorbing')
    assert resp.status_code == 200
    assert len(resp.json) == 2
    courses = [c['coursename'] for c in resp.json]
    assert sorted(courses) == ['hill zorbing', 'snow zorbing']

def test_search_with_date(client):
    assert client.post('/api/course', json=COURSE_WEAVING).status_code == 200
    assert client.post('/api/course', json=HILL_ZORBING).status_code == 200
    assert client.post('/api/course', json=SNOW_ZORBING).status_code == 200
    assert client.post('/api/course', json=PARACHUTE_EXTREME_IRONING).status_code == 200
    assert client.post('/api/course', json=UNDERWATER_EXTREME_IRONING).status_code == 200

    resp = client.post('/api/course/search', json={
        'coursename':'underwater',
        'startafter': '2021-05-10'
    })
    assert resp.status_code == 200
    assert len(resp.json) == 1
    course = resp.json[0]
    assert course['coursename'] == 'underwater extreme ironing'

def test_change():
    pass

if __name__ == '__main__':
    pass