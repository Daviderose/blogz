from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys@zP3BQX'


class Blog(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.String(800))

	def __init__(self, title, body):
		self.title = title
		self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
	
	'''
	owner = User.query.filter_by(email = session['email']).first()
	'''
	if request.method == 'POST':
		blog_title = request.form['blog_title']
		blog_text = request.form['blog_text']
		new_blog = Blog(blog_title, blog_text) 
		db.session.add(new_blog)
		db.session.commit() 

	blogs = Blog.query.all()
	'''completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()'''
	return render_template('main_blog.html', title="Main Blog", blogs=blogs)

if __name__ == '__main__':
	app.run()