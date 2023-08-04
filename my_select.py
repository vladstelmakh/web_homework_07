from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group

engine = create_engine('postgresql://postgres:2001@localhost:5433/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    # Найти 5 студентов с наибольшим средним баллом по всем предметам.
    result = session.query(Student.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                    .join(Grade) \
                    .group_by(Student.name) \
                    .order_by(desc('avg_grade')) \
                    .limit(5) \
                    .all()
    print("Студенты с наибольшим средним баллом:")
    for student_name, avg_grade in result:
        print(f"Имя: {student_name}, Средний балл: {avg_grade}")

def select_2():
    # Найти студента с наивысшим средним баллом по определенному предмету.
    subject_id = int(input("Введите ID предмета: "))
    result = session.query(Student.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                    .join(Grade) \
                    .filter(Grade.subject_id == subject_id) \
                    .group_by(Student.name) \
                    .order_by(desc('avg_grade')) \
                    .first()
    if result:
        student_name, avg_grade = result
        print(f"Студент с наивысшим средним баллом по предмету (ID {subject_id}):")
        print(f"Имя: {student_name}, Средний балл: {avg_grade}")
    else:
        print(f"Предмет с ID {subject_id} не существует или у него нет оценок.")

def select_3():
    # Найти средний балл в группах по определенному предмету.
    subject_id = int(input("Введите ID предмета: "))
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                    .join(Student) \
                    .join(Grade) \
                    .filter(Grade.subject_id == subject_id) \
                    .group_by(Group.name) \
                    .all()
    print(f"Средний балл в группах по предмету (ID {subject_id}):")
    for group_name, avg_grade in result:
        print(f"Группа: {group_name}, Средний балл: {avg_grade}")

def select_4():
    # Найти средний балл на потоке (по всей таблице оценок).
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).first()
    if result[0] is not None:
        print(f"Средний балл на потоке: {result[0]}")
    else:
        print("В базе данных нет оценок.")

def select_5():
    # Найти какие курсы читает определенный преподаватель.
    teacher_id = int(input("Введите ID преподавателя: "))
    result = session.query(Subject.name) \
                    .join(Teacher) \
                    .filter(Teacher.id == teacher_id) \
                    .all()
    if result:
        print(f"Преподаватель (ID {teacher_id}) читает следующие курсы:")
        for subject_name in result:
            print(f"Предмет: {subject_name[0]}")
    else:
        print(f"Преподавателя с ID {teacher_id} не существует или он не читает ни одного курса.")

def select_6():
    # Найти список студентов в определенной группе.
    group_id = int(input("Введите ID группы: "))
    result = session.query(Student.name) \
                    .filter(Student.group_id == group_id) \
                    .all()
    if result:
        print(f"Список студентов в группе (ID {group_id}):")
        for student_name in result:
            print(f"Имя: {student_name[0]}")
    else:
        print(f"Группы с ID {group_id} не существует или в ней нет студентов.")

def select_7():
    # Найти оценки студентов в отдельной группе по определенному предмету.
    group_id = int(input("Введите ID группы: "))
    subject_id = int(input("Введите ID предмета: "))
    result = session.query(Student.name, Grade.grade, Grade.date) \
                    .join(Grade) \
                    .filter(Student.group_id == group_id, Grade.subject_id == subject_id) \
                    .all()
    if result:
        print(f"Оценки студентов в группе (ID {group_id}) по предмету (ID {subject_id}):")
        for student_name, grade, date in result:
            print(f"Студент: {student_name}, Оценка: {grade}, Дата: {date}")
    else:
        print(f"Оценок студентов в группе (ID {group_id}) по предмету (ID {subject_id}) не найдено.")

def select_8():
    # Найти средний балл, который ставит определенный преподаватель по своим предметам.
    teacher_id = int(input("Введите ID преподавателя: "))
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                    .join(Subject) \
                    .filter(Subject.teacher_id == teacher_id) \
                    .first()
    if result[0] is not None:
        print(f"Средний балл, который ставит преподаватель (ID {teacher_id}) по своим предметам: {result[0]}")
    else:
        print(f"Преподавателя с ID {teacher_id} не существует или он не читает ни одного предмета.")

def select_9():
    # Найти список курсов, которые посещает определенный студент.
    student_id = int(input("Введите ID студента: "))
    result = session.query(Subject.name) \
                    .join(Grade) \
                    .filter(Grade.student_id == student_id) \
                    .all()
    if result:
        print(f"Студент (ID {student_id}) посещает следующие курсы:")
        for subject_name in result:
            print(f"Предмет: {subject_name[0]}")
    else:
        print(f"Студента с ID {student_id} не существует или он не посещает ни одного курса.")

def select_10():
    # Список курсов, которые определенному студенту читает определенный преподаватель.
    student_id = int(input("Введите ID студента: "))
    teacher_id = int(input("Введите ID преподавателя: "))
    result = session.query(Subject.name) \
                    .join(Grade) \
                    .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id) \
                    .all()
    if result:
        print(f"Студент (ID {student_id}) посещает у преподавателя (ID {teacher_id}) следующие курсы:")
        for subject_name in result:
            print(f"Предмет: {subject_name[0]}")
    else:
        print(f"Студента с ID {student_id} или преподавателя с ID {teacher_id} не существует, либо они не связаны курсами.")

# Выполнение запросов

select_1()
select_2()
select_3()
select_4()
select_5()
select_6()
select_7()
select_8()
select_9()
select_10()

# Закрытие соединения
session.close()
