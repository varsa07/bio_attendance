from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary database
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

@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form.get('student_id')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if student_id in students_db:
        student_name = students_db[student_id]
        attendance_records.append({'id': student_id, 'name': student_name, 'time': now})
        return f"<h3>Welcome {student_name}! Attendance Marked at {now}</h3><br><a href='/'>Go Back</a>"
    else:
        return f"<h3>Error: Student ID not found! Register first.</h3><br><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
