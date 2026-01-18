import smtplib
from email.message import EmailMessage

def send_email(to_email, attachment_path):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = "vishwasskhattarr@gmail.com"
    msg["To"] = to_email
    msg.set_content("Please find the TOPSIS result attached.")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("vishwasskhattarr@gmail.com", "xkmrczworilviujk")
        smtp.send_message(msg)
