from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Connection to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userName:databasePass@localhost/flaskDB'
db = SQLAlchemy(app)


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        year = request.form['year']

        student = Student(first_name, last_name, year)
        db.session.add(student)
        db.session.commit()
    else:
        return "ERROR"
    return render_template('thanks.html')

@app.route('/view')
def view():
    return render_template('displayStudents.html', students=Student.query.order_by(Student.id).all())


@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    if request.method == 'POST':
        studentInfo = Student.query.filter_by(id=student_id).first()
        studentInfo.first_name = request.form['first_name']
        studentInfo.last_name = request.form['last_name']
        studentInfo.year = request.form['year']
        db.session.commit()
    if request.method == 'GET':
        return render_template('update.html', studentInfo=Student.query.filter_by(id=student_id).first())
    return render_template('thanks.html')



if __name__ == '__main__':
    app.run(debug=True)
