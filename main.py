import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Teacher, Group

# Подключение к базе данных
engine = create_engine('postgresql://postgres:2001@localhost:5433/postgres')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def create_teacher(name):
    # Создание учителя
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    print(f"Учитель '{name}' успешно создан.")

def create_group(name):
    # Создание группы
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Группа '{name}' успешно создана.")

def list_teachers():
    # Показать всех учителей
    teachers = session.query(Teacher).all()
    if teachers:
        print("Список учителей:")
        for teacher in teachers:
            print(f"ID: {teacher.id}, Имя: {teacher.name}")
    else:
        print("В базе данных нет учителей.")

def list_groups():
    # Показать все группы
    groups = session.query(Group).all()
    if groups:
        print("Список групп:")
        for group in groups:
            print(f"ID: {group.id}, Название: {group.name}")
    else:
        print("В базе данных нет групп.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Управление базой данных университета.")
    parser.add_argument("-a", "--action", choices=["create", "list"], required=True, help="Выберите действие: create (создать) или list (показать список).")
    parser.add_argument("-m", "--model", choices=["Teacher", "Group"], required=True, help="Выберите модель: Teacher (учитель) или Group (группа).")
    parser.add_argument("-n", "--name", help="Имя учителя или название группы (только для create).")
    args = parser.parse_args()

    if args.action == "create":
        if args.model == "Teacher":
            if args.name:
                create_teacher(args.name)
            else:
                print("Ошибка: не указано имя учителя.")
        elif args.model == "Group":
            if args.name:
                create_group(args.name)
            else:
                print("Ошибка: не указано название группы.")
    elif args.action == "list":
        if args.model == "Teacher":
            list_teachers()
        elif args.model == "Group":
            list_groups()
