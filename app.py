import os
import csv
from flask import send_file

from flask import Flask, render_template, request
from datetime import date
import csv
import os

app = Flask(__name__)

CSV_FILE = "registrations.csv"

# Create CSV file if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Event", "Name", "Course", "Year", "Phone", "Category"])


# ================= HOME =================
@app.route("/")
def home():
    today = date.today()

    events = [
        {
            "id": 1,
            "name": "Annual Cultural Fest 2026",
            "image": "annual.jpg",
            "date": "March 18, 2026",
            "is_annual": True
        },
        {
            "id": 2,
            "name": "Mahatma Phule Jayanti",
            "image": "phule.jpg",
            "days_left": (date(2026, 4, 11) - today).days,
            "is_annual": False
        },
        {
            "id": 3,
            "name": "Dr. Babasaheb Ambedkar Jayanti",
            "image": "ambedkar.jpg",
            "days_left": (date(2026, 4, 14) - today).days,
            "is_annual": False
        },
        {
            "id": 4,
            "name": "Maharashtra Day",
            "image": "maharashtra.jpg",
            "days_left": (date(2026, 5, 1) - today).days,
            "is_annual": False
        },
        {
            "id": 5,
            "name": "Independence Day",
            "image": "independence.jpg",
            "days_left": (date(2026, 8, 15) - today).days,
            "is_annual": False
        },
        {
            "id": 6,
            "name": "Gandhi Jayanti",
            "image": "gandhi.jpg",
            "days_left": (date(2026, 10, 2) - today).days,
            "is_annual": False
        }
    ]

    return render_template("index.html", events=events)


# ================= REGISTER =================
@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):

    events = [
        {"id": 1, "name": "Annual Cultural Fest 2026", "is_annual": True},
        {"id": 2, "name": "Mahatma Phule Jayanti", "is_annual": False},
        {"id": 3, "name": "Dr. Babasaheb Ambedkar Jayanti", "is_annual": False},
        {"id": 4, "name": "Maharashtra Day", "is_annual": False},
        {"id": 5, "name": "Independence Day", "is_annual": False},
        {"id": 6, "name": "Gandhi Jayanti", "is_annual": False}
    ]

    event = next((e for e in events if e["id"] == event_id), None)

    # ===== FORM SUBMIT =====
    if request.method == "POST":
        name = request.form.get("name")
        course = request.form.get("course")
        year = request.form.get("year")
        phone = request.form.get("phone")
        category = request.form.get("category")

        # ✅ SAVE TO EXCEL (CSV)
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([event["name"], name, course, year, phone, category])

        return render_template("success.html", name=name, event=event["name"])

    return render_template("register.html", event=event)

# ================= ADMIN PANEL =================
@app.route("/admin")
def admin():

    registrations = []

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                registrations.append(row)

    return render_template("admin.html", registrations=registrations)

# ================= DOWNLOAD EXCEL =================
@app.route("/download")
def download():
    return send_file("registrations.csv", as_attachment=True)


# ================= DELETE ENTRY =================
@app.route("/delete/<int:index>")
def delete(index):
    rows = []

    with open(CSV_FILE, "r") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        data = reader[1:]

    if 0 <= index < len(data):
        data.pop(index)

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    return redirect(url_for("admin"))

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)