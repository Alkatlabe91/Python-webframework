from flask import Blueprint, jsonify, send_file, render_template, session, request,redirect ,url_for
from controllers.notes_controllers import get_all_notes, add_note,find_or_add_category,get_all_categories,get_questions_by_note_id,update_question,generate_open_question_and_save,save_question,get_all,delete_note,delete_question,get_note,update_note_by_id,generate_answer
from datetime import datetime
import csv

notes_bp = Blueprint('notes', __name__)




@notes_bp.route('/notes/new', methods=['GET'])
def new_note_page():
    is_logged_in = 'username' in session
    creation_date = datetime.now()
    categories = get_all_categories()
    error = request.args.get('error', None)

    return render_template('notes_edit_new.html',current_time=creation_date, is_logged_in=is_logged_in,categories=categories, error=error)


@notes_bp.route('/notes/edit/<int:note_id>', methods=['GET'])
def edit_note_page(note_id):
    is_logged_in = 'username' in session
    categories = get_all_categories()
    note = get_note(note_id)
    return render_template('notes_edit_new.html',note=note, note_id=note_id, is_logged_in=is_logged_in,categories=categories)


@notes_bp.route('/notes/question/<int:note_id>', methods=['GET'])
def get_Question_page(note_id):
    is_logged_in = 'username' in session
    if is_logged_in: 
        note = get_note(note_id)
        if note is not None: 
          return render_template('note_question.html',note=note)
        else: 
          return redirect(url_for('notFound'))
    else: 
        return redirect(url_for('index'))
    # note = get_note(note_id)
   
    # return render_template('notes_edit_new.html',note=note, note_id=note_id, is_logged_in=is_logged_in,categories=categories)


@notes_bp.route('/notes/submit_form', methods=['POST'])
def submit_form():
    title = request.form.get('title') or None
    source = request.form.get('source') or None
    category = request.form.get('category') or None
    public = 'is_public' in request.form
    text = request.form.get('text') or None
    if not title or not source or not category or not text:
        error = 'Please fill in all required fields.'
        return redirect(url_for('notes.new_note_page', error = error))
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    category_entity = find_or_add_category(category)
    add_note(title,source,public,session['user_id'],category_entity['category_id'],text,date)
    return redirect(url_for('index'))



@notes_bp.route('/notes/edit_form', methods=['POST'])
def edit_form():
    note_id =  request.form.get('note_id') or None
    title = request.form.get('title') or None
    source = request.form.get('source') or None
    category = request.form.get('category') or None
    public = 'is_public' in request.form
    text = request.form.get('text') or None
    if not title or not source or not category or not text:
        error = 'Please fill in all required fields.'

        return redirect(url_for('notes.edit_note_page', error = error))

    category_entity = find_or_add_category(category)
    old_note = get_note(note_id)
    update_note_by_id(note_id,title,source,public,old_note["teacher_id"],category_entity['category_id'],text,old_note["date_created"])
    return redirect(url_for('index'))







    

@notes_bp.route('/notes/update_question', methods=['POST'])
def update_question_by_id():
    if request.form : 
     updated_question = update_question(request.form["questions_id"],request.form["exam_question"])
     return redirect(f"/notes/question/{updated_question['old']['note_id']}")
    elif request.json:     
     updated_question = update_question(request.json["questions_id"],request.json["exam_question"])
     return redirect(f"/notes/question/{updated_question['old']['note_id']}")
    else: 
     return jsonify({ "msg": "no data found in the json or in the form request"})
    


@notes_bp.route('/notes/generate_question/<int:note_id>/<int:question_type>', methods=['GET'])
def generate_open_question_by_note(note_id,question_type=0):
    print(f"question_type {question_type}") 
    question = generate_open_question_and_save(note_id,question_type)
    return redirect(f"/notes/question/{note_id}")


@notes_bp.route('/notes/generate_answer/<int:note_id>/<int:questions_id>', methods=['GET'])
def generate_answer_for_question(note_id,questions_id):
    answer = generate_answer(questions_id)
    return redirect(f"/notes/question/{note_id}")


@notes_bp.route('/notes/delete_note/<int:note_id>', methods=['DELETE', 'GET'])
def delete_note_by_id(note_id):
    delete_note(note_id)
    return redirect(url_for('index'))

@notes_bp.route('/notes/delete_question/<int:question_id>', methods=['DELETE','GET'])
def delete_question_by_id(question_id):
    question = delete_question(question_id)
    return redirect(f"/notes/question/{question['note_id']}")

@notes_bp.route('/notes/export_csv',  methods=['GET', 'POST'])
def export_csv():
   data = get_all()
   csv_file_path = 'new.csv'
   with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Title', 'Note Source', 'Teacher', 'Category', 'Question'])
        csv_writer.writerows(data)

   return send_file(csv_file_path, as_attachment=True)
   

