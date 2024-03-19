from flask import Flask
from pathlib import Path
from text_task import text_task_blueprint
from email_task import email_task_blueprint
import init_app_db, os

os.system("crond -b")
dir = Path().parent.absolute()
app_db_path = os.path.join(dir, "data", "database","app.db")
init_app_db.init(app_db_path)

app = Flask(__name__)
app.register_blueprint(text_task_blueprint)
app.register_blueprint(email_task_blueprint)



if __name__ == "__main__":
    app.run(debug=True)