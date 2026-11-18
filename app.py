
from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("bunk.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/subjects")
def subjects():

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, subject_name, total_lectures, attended_lectures
        FROM subjects
    """)

    data = cursor.fetchall()
    conn.close()

    result = []

    for subject in data:
        subject_id, name, total, attended = subject
        percentage = (attended / total * 100) if total > 0 else 0

        result.append({
            "id": subject_id,
            "name": name,
            "total": total,
            "attended": attended,
            "percentage": round(percentage, 2)
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
