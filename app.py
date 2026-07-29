from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary Databases
students_db = {}
attendance_records = []

# Teacher Password
TEACHER_PASSWORD = "admin123"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        if student_id and name:
            students_db[student_id] = name
            return f"<h3>Success! {name} (ID: {student_id}) Registered.</h3><br><a href='/'>Go Back</a>"
    return redirect(url_for('home'))

@app.route('/teacher-dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == TEACHER_PASSWORD:
            return render_template('dashboard.html', students=students_db, attendance=attendance_records)
        else:
            return "<h3>Incorrect Password! Access Denied.</h3><br><a href='/'>Try Again</a>"
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
