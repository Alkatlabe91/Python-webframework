from flask import Flask,render_template, url_for, session,jsonify
from routes.teachers_routes import teachers_bp
from routes.notes_route import notes_bp
from routes.auth_route import auth_bp
from controllers.notes_controllers import get_all_notes,get_all_categories
from database_generator import WP2DatabaseGenerator
from pathlib import Path
from datetime import timedelta


# database_folder = Path(__file__).parent / 'database'
# database_path = database_folder / 'database.db'

# if not database_folder.exists():
#     database_folder.mkdir()

# database_generator = WP2DatabaseGenerator(database_path, overwrite=True, initial_data=True)
# database_generator.generate_database()
 
app = Flask(__name__ , static_url_path='/static')
app.secret_key = 'secret_key_used_for_hash'
app.permanent_session_lifetime =  timedelta(minutes=60)


app.register_blueprint(teachers_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)



@app.route('/')
def index():
    # login_url = url_for('auth.login')

    print('login_url')
    is_logged_in = 'username' in session
    notes =  get_all_notes()  if  is_logged_in else  []
    categories= get_all_categories()
    category_names = [category['omschrijving'] for category in categories]
    is_admin = session["is_admin"] if is_logged_in else False
    user_id = session["user_id"] if  is_logged_in  else None
    return render_template('index.html',newData=['name1','name2'],user_id=user_id if not None else None,is_admin=is_admin , is_logged_in=is_logged_in,data=notes,categories=category_names)


@app.route('/notFound')
def notFound():
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
