from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary Databases
students_db = {}
attendance_records = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    if student_id and name:
        students_db[student_id] = name
        return f"<h3>Success! {name} (ID: {student_id}) Registered.</h3><br><a href='/'>Go Back</a>"
    return redirect(url_for('home'))

@app.route('/teacher-dashboard')
def teacher_dashboard():
    return render_template('dashboard.html', students=students_db, attendance=attendance_records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
