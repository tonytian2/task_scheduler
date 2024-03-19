import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys,os,csv,sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_APP_PASSWORD')

dir = Path().parent.absolute()
app_db_path = os.path.join(dir, "data", "database","app.db")

subject = sys.argv[1]
body = sys.argv[3]
recipients = sys.argv[2] if sys.argv[2] != "self" else sender
attachment_location = None
sql_location = None
if len(sys.argv) > 5:
    sql_location = sys.argv[4]
    attachment_location = sys.argv[5]
def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_string = file.read()
    return sql_string


def sqlToCSV(csv_file, sql_file):
    with open(csv_file, "w", newline='') as f:
        query = read_sql_file(sql_file)
        c = csv.writer(f)
        with sqlite3.connect(app_db_path) as app_db:
            cur = app_db.cursor()
            cur.execute(query)
            data = cur.fetchall()
            header = tuple([i[0] for i in cur.description])
            c.writerow(header)
            for item in data:
                c.writerow(item)

             
def send_email(subject, body, sender, recipients, password):
    msg = MIMEMultipart()
    txt_msg = MIMEText(body)
    txt_msg['Subject'] = subject
    txt_msg['From'] = sender
    txt_msg['To'] = recipients
    msg.attach(txt_msg)
    
    if attachment_location:
        part = MIMEBase('application', "octet-stream")
        with open(attachment_location, 'rb') as file:
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename={}'.format(Path(attachment_location).name))
            msg.attach(part)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

sqlToCSV(attachment_location, sql_location)
send_email(subject, body, sender, recipients, password)