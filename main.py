from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys@zP3BQX'

class Task(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	completed = db.Column(db.Boolean)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, name, owner):
		self.name = name
		self.completed = False
		self.owner = owner

@app.route('/', methods=['POST', 'GET'])
def index():

	owner = User.query.filter_by(email = session['email']).first()
	
	if request.method == 'POST':
		task_name = request.form['task']
		new_task = Task(task_name, owner)
		db.session.add(new_task)
		db.session.commit()

	tasks = Task.query.filter_by(completed=False, owner=owner).all()
	completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()
	return render_template('todos.html', title="Get It Done!", 
		tasks=tasks, completed_tasks=completed_tasks)

if __name__ == '__main__':
	app.run()