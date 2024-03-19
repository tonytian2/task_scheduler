import sqlite3

def init(app_db_path):
    try:
        app_db = sqlite3.connect(app_db_path)
    except:
        with open(app_db_path, 'w') as fp:
            pass
        
        app_db = sqlite3.connect(app_db_path)
    cur = app_db.cursor()
    

    query = """CREATE TABLE IF NOT EXISTS emailtasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL UNIQUE,
        task_type TEXT NOT NULL,
        created_time TEXT NOT NULL,
        cron_exp TEXT NOT NULL,
        content TEXT NOT NULL
    ); """
    cur.execute(query)
    
    query = """CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL UNIQUE,
        task_description TEXT NOT NULL,
        created_time TEXT NOT NULL,
        finished_time TEXT,
        priority INTEGER NOT NULL
    ); """
    
    cur.execute(query)
            
    
        
        
    