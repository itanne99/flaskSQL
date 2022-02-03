from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# DB Model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    year = db.Column(db.Integer)

    def __init__(self, first_name, last_name, year):
        self.first_name = first_name
        self.last_name = last_name
        self.year = year

    def __repr__(self):
        return f"{self.first_name}:{self.id}"