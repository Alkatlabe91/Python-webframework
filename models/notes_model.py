import sqlite3


class NotesDatabase:
    def __init__(self, db_path='database/database.db'):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_all(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
           SELECT notes.*, 
                   categories.omschrijving AS category,
                   teachers.display_name AS teacher_name,
                   questions.exam_question
            FROM notes
            JOIN categories ON notes.category_id = categories.category_id
            JOIN teachers ON notes.teacher_id = teachers.teacher_id
            LEFT JOIN questions ON notes.note_id = questions.note_id
        """)

        notes_with_category = cursor.fetchall()
        conn.close()

        notes_with_category_as_dicts = [dict(row) for row in notes_with_category]

        return notes_with_category_as_dicts

    def get_note_by_id(self, id):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE note_id = ?", (id,))
        note = cursor.fetchone()
        cursor.execute("SELECT * from questions WHERE note_Id = ?", (id,))
        questions = cursor.fetchall()
        _questions = [dict(row) for row in questions]
        conn.close()
        new_note = dict(note) if note is not None else None
        new_note["all_questions"] = _questions
        for questions in new_note["all_questions"]:
            questions["my_answers"] = self.get_answers_by_question_id(questions["questions_id"])
        return new_note

    def get_all_categories(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        conn.close()
        categories_as_dicts = [dict(row) for row in categories]
        return categories_as_dicts

    def get_category_by_name(self, omschrijving):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE omschrijving = ?", (omschrijving,))
        existing_category = cursor.fetchone()

        conn.close()
        return dict(zip(('category_id', 'omschrijving', 'date_created'),
                        existing_category)) if existing_category is not None else {}

    def find_or_add_category(self, omschrijving):
        existing_category = self.get_category_by_name(omschrijving)

        if existing_category:
            # Category already exists, return the existing category
            return existing_category
        else:
            # Category does not exist, add the new category
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO categories (omschrijving) VALUES (?)", (omschrijving,))
            new_category_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return {'category_id': new_category_id, 'omschrijving': omschrijving}

    def update_note(self, note_id, title, note_source, is_public, teacher_id, category_id, note, date_created):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE notes
        SET title=?, note_source=?, is_public=?, teacher_id=?, category_id=?, note=?, date_created=?
        WHERE note_id=?
    """, (title, note_source, is_public, teacher_id, category_id, note, date_created, note_id))

        cursor.execute("SELECT * FROM notes WHERE note_id = ?", (note_id,))
        updated_note = cursor.fetchone()
        conn.commit()
        conn.close()
        return updated_note

    def create_note(self, title, note_source, is_public, teacher_id, category_id, note, date_created):
        conn = self._connect()

        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO notes (title, note_source, is_public, teacher_id, category_id, note, date_created)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, note_source, is_public, teacher_id, category_id, note, date_created))

        cursor.execute("SELECT * FROM notes WHERE note_id = last_insert_rowid()")
        added_note = cursor.fetchone()
        conn.commit()
        conn.close()
        return True

    def delete_note_by_id(self, note_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE note_id = ?", (note_id,))
        conn.commit()
        conn.close()
        return True

    def get_questions_by_note_id(self, note_id):
     conn = self._connect()
     conn.row_factory = sqlite3.Row
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM questions WHERE note_id = ?", (note_id,))
     questions = cursor.fetchall()
     conn.close()
     questions_as_dicts = [dict(row) for row in questions]
     return questions_as_dicts
 
 
    def create_question(self, note_id, exam_question):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (note_id, exam_question ) VALUES (?, ?)", (note_id,exam_question,))
        new_question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {'questions_id': new_question_id, 'note_id' : note_id, 'exam_question': exam_question}
    
    
    def get_all_data(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
         SELECT notes.title, notes.note_source, teachers.display_name, categories.omschrijving, questions.exam_question
    FROM notes
    JOIN teachers ON notes.teacher_id = teachers.teacher_id
    JOIN categories ON notes.category_id = categories.category_id
    LEFT JOIN questions ON notes.note_id = questions.note_id
    """
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    
    
    def get_question_by_id(self,questions_id):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE questions_id = ?", (questions_id,))
        question = cursor.fetchone()
        conn.close()
        
        return dict(question) if not None else {}
    
    
    
    def delete_question_by_id(self,questions_id):
        saved = self.get_question_by_id(questions_id)
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE questions_id = ?", (questions_id,))
        conn.commit()
        conn.close()
        return saved
    
    
    def update_question(self, question_id, updated_exam_question):
     old_question = self.get_question_by_id(question_id)
     conn = self._connect()
     cursor = conn.cursor()
     cursor.execute("UPDATE questions SET exam_question = ? WHERE questions_id = ?", (updated_exam_question, question_id))
     conn.commit()
     conn.close()
     new_question = self.get_question_by_id(question_id)
     return {"old" : old_question , "new" : new_question}
 
 
    def get_answers_by_question_id(self,questions_id): 
      conn = self._connect()
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM answers WHERE questions_id = ?", (questions_id,))
      answers = cursor.fetchall()
      conn.close()
      return  [dict(answer) for answer in answers] if answers else []
    
    def get_answer_by_id(self,answer_id): 
      conn = self._connect()
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM answers WHERE answer_id = ?", (answer_id,))
      answer = cursor.fetchone()
      conn.close()
      return  dict(answer)

    
    def create_answers(self,answer, questions_id): 
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO answers (questions_id, answer ) VALUES (?, ?)", (questions_id,answer,))
        conn.commit()
        conn.close()
        added_answer = self.get_answer_by_id(cursor.lastrowid)
        return added_answer