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

@app.route('/blog', methods=['POST', 'GET'])
def index():

	if request.args.get('id'):
		blog_id = request.args.get('id')
		blog = Blog.query.get(blog_id)
		return render_template('blog_details.html', title="Blog Details", blog=blog)
	
	'''
	owner = User.query.filter_by(email = session['email']).first()
	'''

	blogs = Blog.query.all()
	'''completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()'''
	return render_template('main_blog.html', title="Build A Blog", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

	if request.method == 'POST':
		blog_title = request.form['blog_title']
		blog_text = request.form['blog_text']

		empty_title_error = 'Please fill out the title'
		empty_text_error = 'Please fill out the body'

		if len(blog_title) > 0:
			empty_title_error = ''

		if len(blog_text) > 0:
			empty_text_error = ''

		if not empty_title_error and not empty_text_error:
			new_post = Blog(blog_title, blog_text) 
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