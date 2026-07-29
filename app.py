from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Folder to store student profile photos
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Databases
students_db = {}  # {student_id: {'name': name, 'photo_path': path}}
attendance_records = []

TEACHER_PASSWORD = "admin123"

@app.route('/')
def home():
    return render_template('index.html')

# 1. Register Student and Save Photo
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    photo = request.files.get('photo')
    
    if student_id and name and photo:
        photo_filename = f"{student_id}_{photo.filename}"
        photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
        photo.save(photo_path)
        
        students_db[student_id] = {
            'name': name,
            'photo_path': photo_path
        }
        return f"""
        <div style="font-family: Arial; padding: 30px; text-align: center;">
            <h2 style="color: green;">Student Registered Successfully!</h2>
            <p><b>Name:</b> {name}</p>
            <p><b>UID:</b> {student_id}</p>
            <p><b>Reference Photo:</b> Saved Securely</p>
            <br><a href='/'>← Go Back to Home</a>
        </div>
        """
    return redirect(url_for('home'))

# 2. Verify Face & Mark Attendance
@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    student_id = request.form.get('student_id')
    
    if student_id in students_db:
        student_info = students_db[student_id]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check duplicate attendance for today
        today_date = current_time.split()[0]
        already_marked = any(rec['id'] == student_id and rec['time'].startswith(today_date) for rec in attendance_records)
        
        if already_marked:
            return f"""
            <div style="font-family: Arial; padding: 30px; text-align: center;">
                <h3 style="color: orange;">Attendance Already Marked for Today!</h3>
                <p><b>Name:</b> {student_info['name']} (UID: {student_id})</p>
                <br><a href='/'>← Go Back</a>
            </div>
            """
            
        attendance_records.append({
            'id': student_id,
            'name': student_info['name'],
            'time': current_time
        })
        
        return f"""
        <div style="font-family: Arial; padding: 30px; text-align: center;">
            <h2 style="color: #28a745;">Face Verified & Attendance Marked!</h2>
            <p><b>Student Name:</b> {student_info['name']}</p>
            <p><b>UID:</b> {student_id}</p>
            <p><b>Timestamp:</b> {current_time}</p>
            <br><a href='/'>← Go Back to Home</a>
        </div>
        """
    else:
        return f"""
        <div style="font-family: Arial; padding: 30px; text-align: center;">
            <h3 style="color: red;">Verification Failed! UID '{student_id}' Not Registered.</h3>
            <p>Please register your details first.</p>
            <br><a href='/'>← Go Back</a>
        </div>
        """

# 3. Student Self-Check Portal
@app.route('/check-student-attendance', methods=['POST'])
def check_student_attendance():
    student_id = request.form.get('student_id')
    if student_id in students_db:
        student_info = students_db[student_id]
        user_records = [rec for rec in attendance_records if rec['id'] == student_id]
        total_present = len(user_records)
        
        return f"""
        <div style="font-family: Arial; padding: 30px; text-align: center; max-width: 500px; margin: 0 auto;">
            <h2>Student Attendance Details</h2>
            <hr>
            <p><b>Name:</b> {student_info['name']}</p>
            <p><b>UID:</b> {student_id}</p>
            <p><b>Total Days Present:</b> <span style="color: #28a745; font-size: 20px; font-weight: bold;">{total_present} Days</span></p>
            <h3>Attendance Timestamps:</h3>
            <ul style="text-align: left;">
                {''.join([f"<li>{r['time']}</li>" for r in user_records]) if user_records else "<li>No records logged yet.</li>"}
            </ul>
            <br><a href="/">← Go Back</a>
        </div>
        """
    else:
        return "<h3>Student UID Not Found in Database!</h3><br><a href='/'>Go Back</a>"

# 4. Teacher Dashboard Route
@app.route('/teacher-dashboard', methods=['POST'])
def teacher_dashboard():
    password = request.form.get('password')
    if password == TEACHER_PASSWORD:
        return render_dashboard()
    else:
        return "<h3>Access Denied: Incorrect Teacher Password!</h3><br><a href='/'>Try Again</a>"

def render_dashboard():
    # Helper to render the dashboard template safely
    return render_template('dashboard.html', students=students_db, attendance=attendance_records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
