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

def is_blank(variable):
    try:
        len(variable) != 0
        return True
    except:
        return False

@app.route("/", methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    email_error = ''

    if not is_blank(username):
        username_error = 'Username field is required'
        password = ''
    else:
        if 3 <= len(username) >= 20:
            username_error = 'Username and password must be between 3-20 characters'  
            password = ''

    if not is_blank(password):
        password_error = 'Password field is required'
        password = ''
    else:
        if 3 <= len(password) >= 20:
            password_error = 'Username and password must be between 3-20 characters'
            password = ''
        
    if password != verify_password:
        password_error = 'Passwords must match'
        password = ''
        verify_password = ''

    if len(email) > 0:
        if email.count(' ') > 0 or 2 <= len(email) >=20:
            email_error = 'Email address is invalidA'
        else:
            if 0 <= email.count('.') >= 2 or 0 <= email.count('@') >=2:
                email_error ='Email address invalidB'

    #if '.' not in email or '@' not in email:
    #    email_error = 'Email address invalid'
    #else:
    #    if email.count('.') > 1 or email.count('@') > 1:
    #        email_error = 'Email address invalid'

    #if 2<= len(username) >= 20 or 2<=len(password)>= 20:
    #    length_error = 'Username and password must be between 3-20 characters'
    #    password = ''
 
    if not username_error and not password_error and not email_error:
        return redirect('/valid-signup?username={0}'.format(username))
    else:
        template = jinja_env.get_template('validate.html')
        return template.render(username_error=username_error, 
        password_error=password_error, 
        email_error=email_error,
        username=username,
        password=password,
        verify_password=verify_password,
        email=email)

    if len(email) == 0:
        invalid_email_error = 'Email address invalid'
        password = ''
        verify_password = ''

@app.route("/valid-signup")
def valid_signup():
    username = request.args.get('username')
    return '<h1>Welcome {0}!</h1>'.format(username)
    
    #username = request.form['username']
    #template = jinja_env.get_template('valid_signup.html')
    #return template.render(name = username)

app.run()