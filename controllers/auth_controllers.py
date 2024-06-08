from models.teachers_model import TeacherDatabase



def get_teacher_by_username(username,password):
    teacher_db = TeacherDatabase()
    print(username,password)
    return teacher_db.get_teacher_by_username(username,password)