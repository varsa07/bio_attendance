from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary Databases
# Structure: { student_id: {'name': name, 'photo': filename} }
students_db = {}
# Structure: [ {'id': student_id, 'name': name, 'time': timestamp} ]
attendance_records = []

TEACHER_PASSWORD = "admin123"

@app.route('/')
def home():
    return render_template('index.html')

# 1. Student Registration Endpoint (Saves Info + Photo reference)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        photo = request.files.get('photo')
        
        if student_id and name:
            photo_filename = photo.filename if photo else "default.jpg"
            students_db[student_id] = {
                'name': name,
                'photo': photo_filename
            }
            return f"""
            <div style="font-family: Arial; padding: 30px; text-align: center;">
                <h2 style="color: green;">Registration Successful!</h2>
                <p><b>Student Name:</b> {name}</p>
                <p><b>Student ID / UID:</b> {student_id}</p>
                <p><b>Reference Image:</b> Uploaded & Linked</p>
                <br><a href="/">← Return to Main Page</a>
            </div>
            """
    return redirect(url_for('home'))

# 2. Student Self Attendance Checker Endpoint
@app.route('/check-student-attendance', methods=['GET', 'POST'])
def check_student_attendance():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        if student_id in students_db:
            student_info = students_db[student_id]
            # Fetch all attendance logs for this student
            user_records = [rec for rec in attendance_records if rec['id'] == student_id]
            total_present = len(user_records)
            
            return f"""
            <div style="font-family: Arial; padding: 30px; text-align: center; max-width: 500px; margin: 0 auto;">
                <h2>Student Attendance Details</h2>
                <hr>
                <p><b>Student Name:</b> {student_info['name']}</p>
                <p><b>UID / Roll No:</b> {student_id}</p>
                <p><b>Total Days Present:</b> <span style="color: #28a745; font-size: 20px; font-weight: bold;">{total_present} Days</span></p>
                <h3>Recent Mark Timestamps:</h3>
                <ul style="text-align: left;">
                    {''.join([f"<li>{r['time']}</li>" for r in user_records]) if user_records else "<li>No records logged yet.</li>"}
                </ul>
                <br><a href="/">← Go Back</a>
            </div>
            """
        else:
            return "<h3>Student Roll Number / UID Not Found! Please register first.</h3><br><a href='/'>Go Back</a>"
            
    return redirect(url_for('home'))

# 3. Secure Teacher Dashboard Route
@app.route('/teacher-dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == TEACHER_PASSWORD:
            return render_template('dashboard.html', students=students_db, attendance=attendance_records)
        else:
            return "<h3>Access Denied: Incorrect Teacher Password!</h3><br><a href='/'>Try Again</a>"
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
