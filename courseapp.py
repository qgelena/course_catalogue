#!/usr/bin/env python3
'''
Створити ряд endpoint'ів для наступних функцій:
* Додавання курсу в каталог (create)
* Відображення списку курсів (read)
* Відображення деталей курсу по id (детальна сторінка)
 курсу повинна відображати повну інформацію про курс) (read)
* Пошук курсу за назвою і фільтр по датах (search)
* Зміна атрибутів курсу (update)
* Видалення курсу (delete)
'''

from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    request,
    jsonify
)
import models
from models import db, Course
import sqlalchemy as sa
from sqlalchemy import and_

def create_app(sqlitepath='sqlite://'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlitepath
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
    # Відображення списку курсів (read)
    @app.route('/api/course', methods=['GET'])
    def course_list():
        """App route function for the homepage with a list of courses"""
        Course = models.Course
        data = Course.query.all()
        return jsonify({'status': 'ok', 'courses': data})

    # Додавання курсу в каталог (create)
    @app.route('/api/course', methods=['POST'])
    def course_new():
        try:
            coursename = request.json['coursename']
            startdate = request.json['startdate']
            finishdate = request.json['finishdate']
            numberlectures = request.json['numberlectures']

            startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
            finishdate = datetime.strptime(finishdate, '%Y-%m-%d').date()
        except (KeyError, ValueError) as e:
            return jsonify({
                "status":"error", 
                "error": str(e),
            }), 400
        
        course = models.Course(coursename, startdate, finishdate, numberlectures)
        db.session.add(course)
        db.session.commit()

        return jsonify({
            "status":"ok",
            "course_id": course.id
        })

    # Відображення деталей курсу по id (детальна сторінка)
    # курсу повинна відображати повну інформацію про курс) (read)
    @app.route('/api/course/<int:id>', methods=['GET'])
    def course_info(id):
        course = models.Course.query.get(id)
        if course is None:
            return jsonify({'error':'not found', 'course': id}), 404
        return jsonify(course) 

    # Видалення курсу (delete)
    @app.route('/api/course/<int:id>', methods=['DELETE'])
    def course_delete(id):
        
        course = Course.query.get(id)
        if course is None:
            return jsonify({'error':'not found', 'course':id}), 404
        db.session.delete(course)
        db.session.commit()

        return jsonify({'status':'ok'})

    # Пошук курсу за назвою і фільтр по датах (search)
    @app.route('/api/course/search', methods=['POST'])
    def searchcourse():
        if type(request.json) == str:
            search = '%' + request.json + '%'
            search_filter = Course.coursename.like(search)
        elif type(request.json) == dict:
            search_filter = sa.true() # '1=1'
            if 'coursename' in request.json:
                # TODO: AND in SQLAlchemy
                search = '%' + request.json['coursename'] +'%'
                search_filter = Course.coursename.like(search)
            if 'startafter' in request.json:
                try:
                    startafter = request.json['startafter']
                    startafter = datetime.strptime(startafter, '%Y-%m-%d').date()
                    search_filter = and_(search_filter, Course.startdate >= startafter)
                except ValueError as e:
                    return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'invalid search format'}), 400

        q = Course.query.filter(search_filter)
        #print('SQL:', str(q))
        results = q.all()
        return jsonify(results)

    # Зміна атрибутів курсу (update)
    @app.route('/api/course/<id>', methods=['PATCH'])
    def coursechange():
        pass


    db.init_app(app)

    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    basedir = Path(__file__).absolute().parent
    sqlitepath = basedir/'db.sqlite'
    sqlitepath = 'sqlite:///' + sqlitepath.as_posix()

    print(sqlitepath)
    app = create_app(sqlitepath)
    app.debug = True
    app.run()