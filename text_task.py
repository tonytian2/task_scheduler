from flask import Blueprint, jsonify, make_response, request, session
import datetime, os, sqlite3
from pathlib import Path

text_task_blueprint = Blueprint("text_task", __name__)

os.system("crond -b")
dir = Path().parent.absolute()
app_db_path = os.path.join(dir, "data", "database","app.db")

@text_task_blueprint.route("/texttask", methods=["POST"])
def create_task():
    data = request.get_json()
    task_name = data["task_name"]
    task_description = data["task_description"]
    created_time = datetime.datetime.now().isoformat()
    priority =  data["priority"] if "priority" in data else 2
    values = (task_name,  task_description, created_time, priority, None )
    query = ''' INSERT INTO tasks(task_name, task_description, created_time, priority, finished_time)
              VALUES(?,?,?,?,?); '''
    with sqlite3.connect(app_db_path) as app_db:
        cur = app_db.cursor()
        cur.execute(query, values)
        app_db.commit()
    return "OK"
    
    
    
@text_task_blueprint.route("/texttask/update", methods=["POST"])    
def update_task():
    data = request.get_json()
    task_id = data["task_id"]
    updated_items = {}
    updated_items["task_description"] = data["task_description"] if "task_description" in data else None
    updated_items["priority"] = data["task_description"] if "task_description" in data else None
    updated_items["finished_time"] = datetime.datetime.now().isoformat() if "finished" in data else None   
    
    updates = ''.join("{}=?, ".format(k) if updated_items[k] else " " for k in updated_items.keys()).strip()[:-1]
    query = "UPDATE tasks SET " + updates + " WHERE task_id=?;"
    values = []
    for v in updated_items.values():
        if v:
            values.append(v)
    with sqlite3.connect(app_db_path) as app_db:
        cur = app_db.cursor()
        cur.execute(query, values + [task_id])
        app_db.commit()
    return "OK"


@text_task_blueprint.route("/texttask", methods=["DELETE"])    
def delete_task():
    data = request.get_json()
    task_id = (data["task_id"],)
    query = "DELETE FROM tasks WHERE task_id=?;"
    with sqlite3.connect(app_db_path) as app_db:
        cur = app_db.cursor()
        cur.execute(query, task_id)
        app_db.commit()
    return "OK"


@text_task_blueprint.route("/texttask/all", methods=["GET"])    
def get_all_tasks():

    query = "SELECT * FROM tasks order by priority desc, created_time;"
    with sqlite3.connect(app_db_path) as app_db:
        cur = app_db.cursor()
        cur.execute(query)
        header = [r[0] for r in cur.description]
        print(header)
        rows = cur.fetchall()
    r = []
    for row in rows:
        d = {}
        for i in range(len(row)):
            d[header[i]] = row[i]
        r.append(d)
    return r
        
    
    