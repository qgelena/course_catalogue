from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Course(db.Model):
    """Таблиця з курсами 

    Курс має мати наступні атрибути:
    * Назва
    * Дата початку
    * Дата закінчення 
    * Кількість лекцій
    """

    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(), nullable =False)
    startdate = db.Column(db.Date())
    finishdate = db.Column(db.Date())
    numberlectures = db.Column(db.Integer(), nullable=False)

    def __init__(self, coursename, startdate, finishdate, numberlectures):
        self.coursename = coursename
        self.startdate = startdate
        self.finishdate = finishdate
        self.numberlectures = numberlectures

if __name__ == '__main__':
    from courseapp import app
    db.create_all(app=app)