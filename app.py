from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    with app.app_context():
        tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_task = Task(content=content)
    with app.app_context():
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    with app.app_context():
        task = Task.query.get(task_id)
        task.completed = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    with app.app_context():
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)