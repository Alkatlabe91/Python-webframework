from flask import Blueprint, jsonify, send_file, render_template, session, request,redirect ,url_for
from controllers.teachers_controllers import get_all_teachers,get_teacher,update_teacher_by_id,delete_user_by_id,add_teacher,verify,update_profile_by_id
from datetime import datetime
from flask import g

teachers_bp = Blueprint('teachers', __name__)


@teachers_bp.before_request
def before_teachers_request():
    g.user = get_teacher(session['user_id'] )

@teachers_bp.route('/teachers/edit_profile', methods=['GET' , 'POST'])
def edit_profile():
  # if g.user and g.user.get('is_admin', 0) == 1:

    if request.method == 'GET': 
     if 'username' in session:
      teacher = get_teacher(session['user_id'] )
      print(teacher)
      return render_template('edit_profile.html',teacher=teacher)
     else: 
      return redirect(url_for('index'))
    elif request.method == 'POST':
      if request.is_json:
        # If the request is identified as JSON, use request.json
          displayname = request.json.get('display_name')
          username = request.json.get('username')
      else:
        # If not JSON, assume form data
          displayname = request.form.get('display_name')
          username = request.form.get('username')
      if username is not None and displayname  is not None:
       update_profile_by_id(session['user_id'],displayname,username)
       return redirect(url_for('teachers.edit_profile'))
      else: 
        return jsonify({"msg": "no data found in your request"})
    else : 
      return redirect(url_for('notFound'))
  # else:
  #     return render_template('404.html')




    
@teachers_bp.route('/teachers', methods=['GET'])
def get_teachers():
    if g.user and g.user.get('is_admin', 0) == 1:

     teachers = get_all_teachers()
     return render_template('teachers.html',teachers=teachers)
    else:
        
        return render_template('404.html')


@teachers_bp.route('/teachers/new', methods=['POST', 'GET'])
def create_teacher():
  if g.user and g.user.get('is_admin', 0) == 1:

    if request.method == 'POST':
          # Logica voor het maken van een nieuwe leraar
          display_name = request.form['display_name']
          username = request.form['username']
          teacher_password = request.form['teacher_password']
          is_admin = request.form.get('is_admin', 0)  # Ophaal de waarde van is_admin checkbox

          already_in = verify(username)
        
          if not display_name or not username or not teacher_password:
              # Geef een foutmelding weer als display_name, username of password ontbreekt
              return render_template('new_teacher.html', error='Display name, username, and password are required.')
          else:
              if(already_in):
                return render_template('new_teacher.html', error='Username already in use')
              else:
                add_teacher(display_name, username, teacher_password, is_admin)
                return redirect(url_for('teachers.get_teachers'))

    # Als de methode GET is, toon dan het formulier
    return render_template('new_teacher.html')
  else:
      return render_template('404.html')
    
@teachers_bp.route('/teachers/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def update_teacher(teacher_id):
    if g.user and g.user.get('is_admin', 0) == 1:

      if request.method == 'GET':
            teacher = get_teacher(teacher_id)
            if teacher:
                return render_template('edit_teacher.html', teacher=teacher, error=None)
            else:
                return redirect(url_for('teachers.get_teachers'))

      elif request.method == 'POST':
            display_name = request.form['display_name']
            username = request.form['username']

            if not display_name or not username:
                 # Return an error message if display_name or username is empty
                teacher = get_teacher(teacher_id)
                return render_template('edit_teacher.html', teacher=teacher, error='Display name and username are required.')

            is_admin = int(request.form['is_admin'])  # Convert the value to an integer

            update_teacher_by_id(teacher_id, display_name=display_name, username=username, is_admin=is_admin)
            return redirect(url_for('teachers.get_teachers'))

      return render_template('edit_teacher.html', error=None)
    else:
      return render_template('404.html')



@teachers_bp.route('/teachers/delete_user/<int:teacher_id>', methods=['DELETE', 'GET'])
def delete_teacher(teacher_id):
    if g.user and g.user.get('is_admin', 0) == 1:

      delete_user_by_id(teacher_id)
      return redirect(url_for('teachers.get_teachers'))
    else:
      return render_template('404.html')
