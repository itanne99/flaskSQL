from flask import Flask, render_template, request
from models import db, Student
from readJSON import read_json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Connection to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://userName:databasePass@localhost/flaskDB'
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()
    if Student.query.count() == 0:
        for student in read_json('media/students.json'):
            db.session.add(Student(student['first_name'], student['last_name'], student['year']))
            db.session.commit()


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


@app.route('/delete/<int:student_id>')
def delete(student_id):
    Student.query.filter_by(id=student_id).delete()
    db.session.commit()
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
