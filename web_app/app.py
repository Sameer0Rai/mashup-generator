
from flask import Flask, render_template, request
import subprocess
import zipfile
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        videos = request.form["videos"]
        duration = request.form["duration"]
        email = request.form["email"]

        output_file = "mashup.mp3"

        # Run Program 1
        cmd = [
            "python",
            "102303773.py",
            singer,
            videos,
            duration,
            output_file
        ]
        subprocess.run(cmd, cwd=BASE_DIR)

        # Zip the output
        zip_path = os.path.join(OUTPUT_DIR, "mashup.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(os.path.join(OUTPUT_DIR, output_file), output_file)

        # Send email
        send_email(email, zip_path)

        return render_template("index.html", success=True)

    return render_template("index.html", success=False)


def send_email(receiver, zip_path):
    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File 🎵"
    msg["From"] = "samkr2340005@gmail.com"
    msg["To"] = receiver
    msg.set_content(
        "Hi,\n\nYour mashup has been generated successfully.\n"
        "Please find the attached ZIP file.\n\nRegards"
    )

    with open(zip_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename="mashup.zip"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("samkr2340005@gmail.com", "lpnskizyykatuhfr")
        server.send_message(msg)


if __name__ == "__main__":
    app.run(debug=True)
