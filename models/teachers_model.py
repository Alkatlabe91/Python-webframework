import sqlite3

class TeacherDatabase:
    def __init__(self, db_path='database/database.db'):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)


    def get_teacher_by_username(self, username, password):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE Username = ? AND teacher_password = ?", (username, password))
        teacher = cursor.fetchone()
        conn.close()
        return  dict(teacher) if teacher is not None  else None
    
    def verify_teacher_by_username(self, username):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE Username = ? ", (username,))
        teacher = cursor.fetchone()
        conn.close()
        return  True if teacher is not None  else False
    

    def create_teacher(self,display_name,username,teacher_password, is_admin): 
      conn = self._connect()
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      cursor.execute("""
        INSERT INTO teachers (display_name, username, teacher_password, is_admin)
        VALUES (?, ?, ?, ?)
    """, (display_name,username,teacher_password, is_admin))

      cursor.execute("SELECT * FROM teachers WHERE teacher_id = last_insert_rowid()")
      added_teacher = cursor.fetchone()
      conn.commit()
      conn.close()
      return dict(added_teacher) if added_teacher is not None else None
  
  
    def get_all(self):
        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers")
        teachers = cursor.fetchall()
        conn.close()
        return teachers
    
    
    
    def get_teacher_by_id(self, id):
        conn = self._connect()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = ? ", (id,))
        teacher = cursor.fetchone()
        conn.close()
        new_teacher = dict(teacher) if teacher is not None  else None
        return new_teacher
    
    
    def update_teacher(self, teacher_id, display_name, username, is_admin):
     conn = self._connect()
     cursor = conn.cursor()
     cursor.execute("""
        UPDATE teachers
        SET display_name = ?, username = ?, is_admin = ?
        WHERE teacher_id = ?
    """, (display_name, username, is_admin, teacher_id))
    #  cursor.execute("SELECT * FROM teachers WHERE teacher_id = ?", (teacher_id,))
    #  updated_teacher = cursor.fetchone()
     conn.commit()
     conn.close()
     updated_teacher = self.get_teacher_by_id(teacher_id)
     return updated_teacher
 
    def update_profile(self, teacher_id, display_name, username):
     conn = self._connect()
     cursor = conn.cursor()
     cursor.execute("""
        UPDATE teachers
        SET display_name = ?, username = ?
        WHERE teacher_id = ?
    """, (display_name, username,teacher_id))
    #  cursor.execute("SELECT * FROM teachers WHERE teacher_id = ?", (teacher_id,))
    #  updated_teacher = cursor.fetchone()
     conn.commit()
     conn.close()
     updated_teacher = self.get_teacher_by_id(teacher_id)
     return updated_teacher
 
 
 
    def delete_user(self,teacher_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE teacher_id = ?", (teacher_id,))
        conn.commit()
        conn.close()
        return True
  
  









