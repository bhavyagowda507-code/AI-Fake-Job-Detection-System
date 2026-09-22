from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import joblib

from resume_ai import extract_resume_text
from gemini_ai import analyze_career_content

app = Flask(__name__)
app.secret_key = "super_secret_session_key_for_jobguard"


# -----------------------------
# JOB RECOMMENDATION ENGINE
# -----------------------------
def get_job_recommendation(user_input):

    data_path = os.path.join(os.getcwd(), "career_data.json")

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        return "Database file not found."

    user_input_lower = user_input.lower()

    recommendations = []

    for item in data:

        score = (
            sum(
                5
                for edu in item.get("education", [])
                if edu.lower() in user_input_lower
            )
            +
            sum(
                2
                for skill in item.get("skills", [])
                if skill.lower() in user_input_lower
            )
        )

        if score >= 5:
            recommendations.append(item["role"])

    if not recommendations:
        return "No matching roles found."

    return ", ".join(recommendations)


# -----------------------------
# LOAD MODELS
# -----------------------------



# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))


# -----------------------------
# LOAD MODELS
# -----------------------------

try:
    model = joblib.load("job_model.pkl")
    vectorizer = joblib.load("job_vectorizer.pkl")
except Exception:
    model = None
    vectorizer = None

ocr_reader = None


def get_ocr_reader():
    global ocr_reader

    if ocr_reader is None:
        import easyocr
        ocr_reader = easyocr.Reader(["en"], gpu=False)

    return ocr_reader


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":

            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        error = "Invalid credentials."

    return render_template("login.html", error=error)


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    stats = {
        "total_scanned": 148,
        "scams_detected": 42,
        "trusted_postings": 106,
        "accuracy_rate": "94.2%"
    }

    return render_template(
        "dashboard.html",
        stats=stats
    )


# -----------------------------
# JOB ANALYSER
# -----------------------------
@app.route("/job_analyser", methods=["GET", "POST"])
def job_analyser():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    processed = False
    result = None
    score = 0

    title = ""
    company = ""
    description = ""

    if request.method == "POST":

        title = request.form.get("title", "")
        company = request.form.get("company", "")
        description = request.form.get("description", "")

        scam_words = [
            "telegram",
            "whatsapp",
            "fee",
            "deposit",
            "urgent"
        ]

        if any(word in description.lower() for word in scam_words):

            result = "SCAM"
            score = 89

        else:

            result = "SAFE"
            score = 12

        processed = True

    return render_template(
        "job_analyser.html",
        processed=processed,
        result=result,
        score=score,
        title=title,
        company=company,
        description=description
    )


# -----------------------------
# SCAMSNAP
# -----------------------------
@app.route("/scamsnap", methods=["GET", "POST"])
def scamsnap():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    processed = False
    extracted_text = ""
    result = "SAFE"
    score = 0

    if request.method == "POST":

        file = request.files.get("file")

        if file:

            save_path = os.path.join("static", file.filename)
            file.save(save_path)

            if ocr_reader:
                extracted_text = " ".join(
                    ocr_reader.readtext(
                        save_path,
                        detail=0
                    )
                )

            scam_words = [
                "telegram",
                "whatsapp",
                "fee",
                "deposit",
                "urgent"
            ]

            if any(word in extracted_text.lower() for word in scam_words):

                result = "SCAM"
                score = 89

            else:

                result = "SAFE"
                score = 12

            processed = True

    return render_template(
        "scamsnap.html",
        processed=processed,
        extracted_text=extracted_text,
        result=result,
        score=score
    )


# -----------------------------
# RECRUITBOT AI
# -----------------------------
@app.route("/recruitbot", methods=["GET", "POST"])
def recruitbot():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    ai_result = ""
    user_msg = ""

    if request.method == "POST":

        try:

            uploaded_file = request.files.get("resume")
            user_msg = request.form.get("message", "").strip()

            print("USER MESSAGE:", user_msg)

            # Resume Upload Analysis
            if uploaded_file and uploaded_file.filename:

                upload_folder = "uploads"

                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                file_path = os.path.join(
                    upload_folder,
                    uploaded_file.filename
                )

                uploaded_file.save(file_path)

                resume_text = extract_resume_text(file_path)

                print("RESUME TEXT EXTRACTED")

                ai_result = analyze_career_content(
                    resume_text
                )

            # Text Analysis
            elif user_msg:

                ai_result = analyze_career_content(
                    user_msg
                )

            else:

                ai_result = "Please enter some text or upload a resume."

            print("AI RESULT RECEIVED")

        except Exception as e:

            ai_result = f"Error: {str(e)}"
            print("ERROR:", str(e))

    return render_template(
        "recruitbot.html",
        ai_result=ai_result,
        user_msg=user_msg
    )
# -----------------------------
# HISTORY
# -----------------------------
@app.route("/history")
def history():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    recent_history = [
        {
            "date": "05/06/2026",
            "title": "Data Entry Specialist",
            "company": "Apex Global",
            "type": "Text Scan",
            "status": "⚠️ High Risk"
        },
        {
            "date": "04/06/2026",
            "title": "Software Engineer Intern",
            "company": "TechCorp",
            "type": "PDF Document",
            "status": "✅ Verified Trusted"
        }
    ]

    return render_template(
        "history.html",
        history=recent_history
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )