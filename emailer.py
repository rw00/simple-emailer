import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_CONFIG = {
    "host": "smtp.company.com",
    "port": 465,
    "username": "---@company.com",
    "password": "---",
}


def load_recipients(file_path):
    recipients_list = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                recipients_list.append({"name": parts[0], "email": parts[2]})
    return recipients_list


def send_email(server, recipient_email, email_content):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_CONFIG["username"]
        msg["To"] = recipient_email
        msg["Subject"] = "---"

        msg.attach(MIMEText(email_content, "html"))

        server.sendmail(SMTP_CONFIG["username"], recipient_email, msg.as_string())
        print(f"Email sent to <{recipient_email}>")

    except Exception as e:
        print(f"Failed to send email to <{recipient_email}>: {e}")


server = smtplib.SMTP_SSL(SMTP_CONFIG["host"], SMTP_CONFIG["port"])
server.login(SMTP_CONFIG["username"], SMTP_CONFIG["password"])

with open("email_template.html", "r") as email_template_file:
    email_template = email_template_file.read()

recipients = load_recipients("recipients.txt")

for recipient in recipients:
    name = recipient.get("name")
    email = recipient.get("email")
    if name and email:
        email_content = email_template.replace(r"${name}", name)
        send_email(server, email, email_content)
    else:
        print(f"Invalid recipient entry: {recipient}")

server.quit()
