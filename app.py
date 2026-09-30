from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///students.db"
app.config["UPLOAD_FOLDER"]="static/upload"

db=SQLAlchemy(app)

class Student(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30),nullable=False)
    email= db.Column(db.String(30), nullable=False, unique= True)
    dob= db.Column(db.Date, nullable=False)
    gender= db.Column(db.String(5),nullable=False)
    roll_number =db.Column(db.String(10),nullable=False)
    admission_date= db.Column(db.Date, nullable=False)
    course= db.Column(db.String(30),nullable=False)
    photo =db.Column(db.String(30),nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    students=Student.query.all()
    return render_template("index.html", students=students)

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method=="POST":
        name = request.form.get("name")
        email= request.form.get("email")
        dob= request.form.get("dob")
        dob= datetime.strptime(dob, "%Y-%m-%d").date()
        gender= request.form.get("gender")
        rollnumber= request.form.get("rollnumber")
        admissiondate= request.form.get("admissiondate")
        admissiondate= datetime.strptime(admissiondate, "%Y-%m-%d").date()
        course= request.form.get("course")

        photo= request.files["photo"]
        photo_path=os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        photo.save(photo_path)

        print({"name":name, 'email':email, 'dob':dob, 'gender':gender, 'rollnumber': rollnumber, 'admissiondate':admissiondate, 'course':course, "photo":photo})

        student= Student(name=name, email=email,dob=dob, gender= gender, roll_number=rollnumber, admission_date=admissiondate, course= course, photo=photo.filename)

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("add_student.html")


@app.route("/student_details/<int:student_id>", methods=["GET"])
def student_details(student_id):

    student= Student.query.get(student_id)

    return render_template("student_details.html", student=student)

@app.route("/update_student/<int:student_id>", methods=["GET", "POST"])
def update_student(student_id):

    student= Student.query.get(student_id)

    if request.method=="POST":
        student.name = request.form.get("name")
        student.email= request.form.get("email")
        dob= request.form.get("dob")
        student.dob= datetime.strptime(dob, "%Y-%m-%d").date()
        student.gender= request.form.get("gender")
        student.roll_number= request.form.get("rollnumber")
        admission_date= request.form.get("admissiondate")
        student.admissiondate= datetime.strptime(admission_date, "%Y-%m-%d").date()
        student.course= request.form.get("course")

        photo= request.files["photo"]
        photo_path=os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
        photo.save(photo_path)

        student.photo=photo.filename

        db.session.commit()
        
        return redirect(url_for('home'))

    return render_template("update_student.html", student=student)


@app.route("/delete_student/<int:student_id>", methods=["GET", "POST"])
def delete_student(student_id):
    student= Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('home'))



if __name__=="__main__":
    app.run(debug=True)