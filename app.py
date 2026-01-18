from flask import Flask, render_template, request
import os
import pandas as pd
import re
from topsis import run_topsis
from email_utils import send_email

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    file = request.files["file"]
    weights = request.form["weights"]
    impacts = request.form["impacts"]
    email = request.form["email"]

    # Basic validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid Email ID"

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, "result.csv")

    file.save(input_path)

    run_topsis(input_path, weights, impacts, output_path)

    # Send email
    send_email(email, output_path)

    # Read result and convert to HTML table
    df = pd.read_csv(output_path)
    table_html = df.to_html(index=False, classes="table")

    return render_template(
        "index.html",
        tables=table_html,
        email=email
    )

if __name__ == "__main__":
    app.run()
