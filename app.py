from datetime import datetime
import os
import sqlite3
import cv2
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

DATASET_DIR = "dataset"
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", records=records)


@app.route("/save_student", methods=["POST"])
def save_student():
    import base64

    data = request.get_json()
    name = data["name"]
    roll_no = data["roll_no"]
    image_data = data["image"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?)", (roll_no, name)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

    img_bytes = base64.b64decode(image_data.split(",")[1])
    file_path = os.path.join(DATASET_DIR, f"{roll_no}_{name}.jpg")

    with open(file_path, "wb") as f:
        f.write(img_bytes)

    return jsonify(
        {"status": "success", "message": "Student Registered Successfully!"}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)