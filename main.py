from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzarecool@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys@zP3BQX'


class Blog(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.String(800))
	pub_date = db.Column(db.DateTime)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, title, body, pub_date, owner):
		self.title = title
		self.body = body
		self.pub_date = pub_date
		self.owner = owner

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120))
	password = db.Column(db.String(120))
	blogs = db.relationship('Blog', backref = 'owner')

	def __init__(self, username, password):
		self.username = username
		self.password = password
		

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog_list', 'index', 'static']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['GET'])
def index():
	users = User.query.order_by("username")
	return render_template('index.html', users=users)

@app.route('/blog', methods=['POST', 'GET'])
def blog_list():

	if request.args.get('id'):
		blog_id = request.args.get('id')
		blog = Blog.query.get(blog_id)
		return render_template('blog_details.html', title="Blog Details", blog=blog)

	if request.args.get('user'):
		user = request.args.get('user')
		username = User.query.get(user)
		blogs = Blog.query.filter_by(owner_id=user)
		return render_template('user_details.html', title="User Details", username=username, blogs=blogs)
	
	'''
	owner = User.query.filter_by(email = session['email']).first()
	'''

	blogs = Blog.query.order_by("pub_date desc")
	'''completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()'''
	return render_template('main_blog.html', title="Blogz", blogs=blogs,)

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user and user.password == password:
			session['username'] = username
			flash('Logged in', 'success')
			return redirect('/newpost')
		elif user and user.password != password:
			flash('Your password is incorrect', 'error')
		else:
			flash('Username does not exist', 'error')

	return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		verify = request.form['verify']
		is_verified = False

		# check required fields are not empty, contain no spaces and of allotted length
		while not is_verified:
			error_count = 0
			if username == '' or password == ''  or verify == '':
				flash('One or more required fields are empty', 'error')
				error_count += 1

			if len(username) > 2 and len(username) < 21:
				if re.search(' ', username):
					flash('Username cannot contain spaces', 'error')
					error_count += 1	
			else:
				flash('Username must be between 3 and 20 characters', 'error')
				error_count += 1

			if len(password) > 2 and len(password) < 21:
				if re.search(' ', password):
					flash('Password cannot contain spaces', 'error')
					error_count += 1		
			else:
				flash('Password must be between 3 and 20 characters', 'error')
				error_count += 1

			# check if passwords match
			if password != verify:
				flash('Password and Verify Password do not match', 'error')
				error_count += 1

			if error_count > 0:
				return redirect('/signup')

			is_verified = True
			
				

		# check for existing user, if not then create one
		existing_user = User.query.filter_by(username=username).first()
		if not existing_user:
			new_user = User(username, password)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = username
			flash('Logged in', 'success')
			return redirect('/newpost')
		else:
			flash('Username already exists', 'error')
			return redirect('/signup')

	return render_template('signup.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

	if request.method == 'POST':
		blog_title = request.form['blog_title']
		blog_text = request.form['blog_text']
		pub_date = datetime.utcnow()
		owner = User.query.filter_by(username = session['username']).first()

		empty_title_error = 'Please fill out the title'
		empty_text_error = 'Please fill out the body'

		if len(blog_title) > 0:
			empty_title_error = ''

		if len(blog_text) > 0:
			empty_text_error = ''

		if not empty_title_error and not empty_text_error:
			new_post = Blog(blog_title, blog_text, pub_date, owner) 
			db.session.add(new_post)
			db.session.commit()
			blog_id = str(new_post.id)
			return redirect('/blog?id=' + blog_id)
		else:
			return render_template('new_post.html', empty_title_error=empty_title_error, empty_text_error=empty_text_error, 
				blog_title=blog_title, blog_text=blog_text )

	return render_template('new_post.html', title="Add A Blog Entry")

'''@app.route('/blog?id={{blog.id}}', methods=['GET'])
def check_post():
	
	return render_template('blog_details.html', title="Blog Details",)'''

if __name__ == '__main__':
	app.run()