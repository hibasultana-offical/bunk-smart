import sqlite3
def create_database():
    conn=sqlite3.connect("bunksmart.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS subjects
    (id INTEGER PRIMARY KEY AUTOINCREMENT, subject_name TEXT NOT NULL, 
    total_lectures INTEGER DEFAULT 0,attended_lectures INTEGER DEFAULT 0)""")
    conn.commit()
    conn.close()
    print("Bunk Smart Database Created Successfully!")


def add_subject(name):

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM subjects WHERE subject_name = ?",
        (name,)
    )

    existing = cursor.fetchone()

    if existing:
        print(name, "already exists!")
    else:
        cursor.execute(
            "INSERT INTO subjects (subject_name) VALUES (?)",
            (name,)
        )

        conn.commit()
        print(name, "added successfully!")

    conn.close()

def show_subjects():

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    print("\n========== BUNK SMART DASHBOARD ==========")

    for subject in subjects:

        subject_id, name, total, attended = subject

        percentage = (attended / total * 100) if total > 0 else 0

        print("\nSubject ID:", subject_id)
        print("Subject:", name)
        print("Total Lectures:", total)
        print("Attended Lectures:", attended)
        print("Attendance:", round(percentage, 2), "%")

    conn.close()


def mark_attendance(name, status):

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    if status == "Present":
        cursor.execute("""
            UPDATE subjects
            SET total_lectures = total_lectures + 1,
                attended_lectures = attended_lectures + 1
            WHERE subject_name = ?
        """, (name,))

    elif status == "Absent":
        cursor.execute("""
            UPDATE subjects
            SET total_lectures = total_lectures + 1
            WHERE subject_name = ?
        """, (name,))

    conn.commit()
    conn.close()

    print(name, "attendance marked:", status)

def show_attendance(name):

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT total_lectures, attended_lectures
        FROM subjects
        WHERE subject_name = ?
    """, (name,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("Subject not found!")
        return

    total, attended = result

    if total == 0:
        percentage = 0
    else:
        percentage = (attended / total) * 100

    print("\nSubject:", name)
    print("Total Lectures:", total)
    print("Attended Lectures:", attended)
    print("Attendance:", round(percentage, 2), "%")


def get_all_subjects():

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject_name, total_lectures, attended_lectures
        FROM subjects
    """)

    subjects = cursor.fetchall()
    conn.close()

    for subject in subjects:
        name, total, attended = subject

        if total == 0:
            percentage = 0
        else:
            percentage = (attended / total) * 100

        print("\nSubject:", name)
        print("Total Lectures:", total)
        print("Attended Lectures:", attended)
        print("Attendance:", round(percentage, 2), "%")



def calculate_required_lectures(name):

    conn = sqlite3.connect("bunksmart.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT total_lectures, attended_lectures
        FROM subjects
        WHERE subject_name = ?
    """, (name,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        print("Subject not found!")
        return

    total, attended = result

    required = 0

    while total > 0 and (attended + required) / (total + required) < 0.75:
        required += 1

    print("\n--- Smart Attendance Recommendation ---")
    print("Subject:", name)
    print("Current Attendance:", round(attended / total * 100, 2) if total else 0, "%")
    print("Lectures to attend continuously:", required)


def add_multiple_subjects():

    while True:

        name = input("\nEnter subject name (or type 'done'): ")

        if name.lower() == "done":
            break

        add_subject(name)
if __name__ == "__main__":

    create_database()

    add_subject("Mathematics")
    add_subject("Physics")
    add_subject("C++")

    mark_attendance("Mathematics", "Present")
    mark_attendance("Mathematics", "Absent")

    mark_attendance("Physics", "Present")
    mark_attendance("Physics", "Present")

    show_subjects()
    get_all_subjects()