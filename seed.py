from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade

fake = Faker()

# Создание базы данных и подключение к ней
engine = create_engine('postgresql://postgres:2001@localhost:5433/postgres')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Заполнение таблиц случайными данными
def seed_students(num_students):
    for _ in range(num_students):
        name = fake.name()
        group_id = fake.random_int(1, 3)
        student = Student(name=name, group_id=group_id)
        session.add(student)

def seed_groups():
    groups = ['Group A', 'Group B', 'Group C']
    for group_name in groups:
        group = Group(name=group_name)
        session.add(group)

def seed_teachers(num_teachers):
    for _ in range(num_teachers):
        name = fake.name()
        teacher = Teacher(name=name)
        session.add(teacher)

def seed_subjects(num_subjects):
    for _ in range(num_subjects):
        name = fake.job()
        teacher_id = fake.random_int(1, 3)
        subject = Subject(name=name, teacher_id=teacher_id)
        session.add(subject)

def seed_grades(num_grades):
    for _ in range(num_grades):
        student_id = fake.random_int(1, 30)
        subject_id = fake.random_int(1, 8)
        grade = fake.random_int(1, 10)
        date = fake.date_this_decade()
        grade_entry = Grade(student_id=student_id, subject_id=subject_id, grade=grade, date=date)
        session.add(grade_entry)

def seed_database():
    seed_groups()
    seed_teachers(3)
    seed_subjects(8)
    seed_students(50)
    seed_grades(1000)

    session.commit()

seed_database()
