from flask import Flask , render_template, request # type: ignore
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
#cred = credentials.Certificate("firestore_database.py")
#firebase_admin.initialize_app(cred)
#db = firestore.client()
@app.route('/')

def home():
    return render_template("index.html")

def submit_task():
    # retrieve from data
    task = request.form.get('task')
    hours = request.form.get('hours')
    # for now just pass data to the rendered page
    return render_template("submit_task.html", task=task, hours=hours)


if __name__ == '__main__':
    app.run(debug=True)

