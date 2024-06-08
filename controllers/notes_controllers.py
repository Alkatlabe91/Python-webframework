from models.notes_model import NotesDatabase
from helpers.testgpt import TestGPT

def get_all_notes():
    notes_db = NotesDatabase()
    return notes_db.get_all()

def get_note(note_id):
     notes_db = NotesDatabase()
     return notes_db.get_note_by_id(note_id)

def update_note_by_id(note_id,title,note_source,is_public,teacher_id,category_id,note,date_created):
    notes_db = NotesDatabase()
    notes = notes_db.update_note(note_id,title,note_source,is_public,teacher_id,category_id,note,date_created)
    return notes


def get_all_categories():
    notes_db = NotesDatabase()
    return notes_db.get_all_categories()

def find_or_add_category(omschrijving):
    notes_db = NotesDatabase()
    return notes_db.find_or_add_category(omschrijving)

def add_note(title,note_source,is_public,teacher_id,category_id,note,date_created):
    notes_db = NotesDatabase()
    return notes_db.create_note(title,note_source,is_public,teacher_id,category_id,note,date_created)

def delete_note(note_id):
    notes_db = NotesDatabase()
    notes = notes_db.delete_note_by_id(note_id)
    return notes

def get_questions_by_note_id(note_id): 
    notes_db = NotesDatabase()
    return notes_db.get_questions_by_note_id(note_id)


def update_question(question_id, updated_exam_question): 
    notes_db = NotesDatabase()
    return notes_db.update_question(question_id, updated_exam_question)


def generate_open_question_and_save(note_id,type=0):
    notes_db = NotesDatabase()
    note = notes_db.get_note_by_id(note_id)
    if note is not None: 
        tesGPT = TestGPT()
        question = tesGPT.generate_open_question(note["note"]) if type is 0 else tesGPT.generate_multiple_choice_question(note["note"])
        notes_db.create_question(note_id,question)
        return question
    else:
        return 'no note found with this id'
    
    

def generate_answer(questions_id):
    notes_db = NotesDatabase()
    question = notes_db.get_question_by_id(questions_id)
    if question is not None: 
        tesGPT = TestGPT()
        answer = tesGPT.generate_answer(question['exam_question'])
        notes_db.create_answers(answer,questions_id)
        return answer
    else:
        return 'no question found with this id'

def save_question(note_id, exam_question):
    notes_db = NotesDatabase()
    question = notes_db.create_question(note_id, exam_question)
    return question


def delete_question(questions_id): 
    notes_db = NotesDatabase()
    question = notes_db.delete_question_by_id(questions_id)
    return question
    
def get_all(): 
    notes_db = NotesDatabase()
    notes = notes_db.get_all_data()
    return notes