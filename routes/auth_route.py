from flask import Blueprint, render_template, request, redirect, url_for, session, url_for,jsonify
from controllers.auth_controllers import get_teacher_by_username
from controllers.teachers_controllers import verify,add_teacher
auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        teacher = get_teacher_by_username(username, password)
        print(teacher)
        if teacher:
            session['username'] = username
            session['user_id'] = teacher["teacher_id"]
            session['is_admin'] = teacher["is_admin"]
            session.permanent = True
            return redirect(url_for('index'))
        else:
            # Provide an error message for incorrect username or password
            return render_template('login.html', error='Incorrect username or password.')
    return render_template('login.html', error=None)


@auth_bp.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        display_name = request.form['display_name']
        username = request.form['username']
        teacher_password = request.form['password']
        already_in = verify(username)
        if(already_in):
          return render_template('signup.html', error='Username already in use')
        else: 
         new_teacher = add_teacher(display_name,username,teacher_password,is_admin=False)
         session['username'] = username
         session['user_id'] = new_teacher["teacher_id"]
         session['is_admin'] = False
         return redirect(url_for('index'))
        
    is_logged_in = 'username' in session
    if(is_logged_in): 
       return redirect(url_for('index'))
    else: 
       return render_template('signup.html', name="sigUp")





@auth_bp.route('/auth/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('auth.login'))


