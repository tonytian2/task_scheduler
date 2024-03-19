from flask import Blueprint,request
import shlex, os, sqlite3, datetime, json, csv
from crontab import CronTab
from pathlib import Path

email_task_blueprint = Blueprint("email_task", __name__)


dir = Path().parent.absolute()
app_db_path = os.path.join(dir, "data", "database","app.db")
csv_folder_path =  os.path.join(dir)
script_folder_path =  os.path.join(dir, "data", "scripts")
email_sender_path = os.path.join(dir,"emailSender.py")


def get_email_reminder_request(data):
    
    content = data["content"]
    email_body = shlex.quote(content["email_body"])
    title = shlex.quote(content["title"])
    receiver = content["receiver"]
    sql_file = content["sql_file"]
    csv_file = content["csv_file"]
    cron_exp = data["cron_exp"]
    task_name = data["task_name"]
    task_type = "email report"
    created_time = datetime.datetime.now().isoformat()
    
    return content, email_body, cron_exp, task_name, task_type, created_time, sql_file, csv_file, title, receiver
    

def record_to_email_tasks(task_name, created_time, task_type, cron_exp, content):
    values = (task_name, created_time, task_type, cron_exp, json.dumps(content) )
    query = ''' INSERT INTO emailtasks(task_name, created_time, task_type, cron_exp, content)
              VALUES(?,?,?,?,?) '''
    with sqlite3.connect(app_db_path) as app_db:
        cur = app_db.cursor()
        cur.execute(query, values)
        app_db.commit()
        
        
@email_task_blueprint.route('/emailReporter', methods=["POST"])
def emailReporter():
    cron = CronTab(user='root') 
    content, email_body, cron_exp, task_name, task_type, created_time, sql_file, csv_file, title, receiver = get_email_reminder_request(request.get_json())
    for job in cron:
        if job.comment == task_name:
            return f"task {task_name} already exists. Please change task name."
    csv_file_path =  os.path.join(csv_folder_path , csv_file+".csv")
    sql_file_path =  os.path.join(script_folder_path, sql_file+".sql")

    job = cron.new(command=f"python3 {email_sender_path} {title} {receiver} {email_body} {sql_file_path} {csv_file_path}", comment= task_name)
    job.setall(cron_exp)
    cron.write()
    
    record_to_email_tasks(task_name, created_time, task_type, cron_exp,content)
    return "OK"


@email_task_blueprint.route('/emailReporter', methods=["DELETE"])
def emailReminderDelete():
    
    task_name = request.get_json["task_name"]
        
    cron = CronTab(user='root')  
    
    for job in cron:
        if job.comment == task_name:
            job.clear
            cron.write()

            query = "DELETE FROM emailtasks WHERE task_name=?;"
            with sqlite3.connect(app_db_path) as app_db:
                cur = app_db.cursor()
                cur.execute(query, task_name)
                app_db.commit()
            return "OK"
            
    return f"task with name {task_name} not found"    


@email_task_blueprint.route('/cronprint') 
def printjob():
    cron = CronTab(user='root')
    r = []
    for job in cron:
        if job.comment:
            item = ( "task name: "+ job.comment, "job: " + str(job))
            print("task name: ", job.comment)
            print("job: ",job)
            r.append(item)
    return r

@email_task_blueprint.route('/runc/') 
def runc():
    data = request.get_json()
    os.system(data["text"])
    return "OK"
   
         
