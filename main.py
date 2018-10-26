from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def signup():
    template = jinja_env.get_template('validate.html')
    return template.render()

@app.route("/", methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    empty_error = ''
    invalid_error = ''
    length_error = ''
    invalid_email_error = ''

    if len(username) or len(password) == 0:
        empty_error = 'Username and password fields are required'
        password = ''

    if username != password:
        invalid_error = 'Passwords must match'
        username = ''

    if 2<= len(username) >= 20 or 2<=len(password)>= 20:
        length_error = 'Username and password must be between 3-20 characters'
        username = ''

    if not empty_error and not invalid_error and not length_error and not invalid_email_error:
        return redirect("/valid-signup")
    else:
        template = jinja_env.get_template('validate.html')
        return template.render(empty_error=empty_error, 
        invalid_error=invalid_error, 
        length_error=length_error,
        invalid_email_error=invalid_email_error,
        username=username,
        password=password,
        verify_password=verify_password,
        email=email)

    #if '.' not in email or '@' not in email:
    #invalid_email_error = 'Email address invalid'

@app.route("/valid-signup")
def valid_signup():
    template = jinja_env.get_template('valid_signup.html')
    return template.render()


app.run()