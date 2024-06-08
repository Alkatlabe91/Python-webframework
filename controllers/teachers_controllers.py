from models.teachers_model import TeacherDatabase


def verify(username): 
    teacher_db = TeacherDatabase()
    return teacher_db.verify_teacher_by_username(username)

def add_teacher(display,username,password, is_admin):
    teacher_db = TeacherDatabase()
    return teacher_db.create_teacher(display,username,password, is_admin)

def get_all_teachers():
    teacher_db = TeacherDatabase()
    return teacher_db.get_all()

def get_teacher(teacher_id):
     teacher_db = TeacherDatabase()
     return teacher_db.get_teacher_by_id(teacher_id)
 
 
def update_teacher_by_id(teacher_id, display_name, username, is_admin):
    teacher_db = TeacherDatabase()
    return teacher_db.update_teacher(teacher_id, display_name, username, is_admin)

def update_profile_by_id(teacher_id, display_name, username):
    teacher_db = TeacherDatabase()
    return teacher_db.update_profile(teacher_id, display_name, username)

def delete_user_by_id(teacher_id): 
    teacher_db = TeacherDatabase()
    teachers = teacher_db.delete_user(teacher_id)
    return teachers







