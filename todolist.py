from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy_utils.functions import database_exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    deadline = Column(Date, default=datetime.now())

    def __repr__(self):
        return self.task


def date_format(date):
    return date.strftime('%A %#d %b:')


def print_all_tasks(tasks, my_format=None):
    if tasks:
        for index, task in enumerate(tasks):
            print('{}. {}{}'.format(index + 1, task.task, task.deadline.strftime('. %#d %b') if my_format else ""))
        print()
    else:
        print('Nothing to do!\n')


def display():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


def add_task_to_db(new_task):
    session.add(new_task)
    session.commit()


def delete_tasks(number):
    todos = session.query(Task).order_by(Task.deadline).all()
    if todos:
        session.delete(todos[0])
        session.commit()


def create_new_task():
    print('Enter task')
    task_title = str(input())
    print('Enter deadline')
    date_string = str(input())
    deadline = datetime.strptime(date_string, "%Y-%m-%d")
    new_task = Task(task=task_title, deadline=deadline)
    add_task_to_db(new_task)
    print('The task has been added!\n')


def query_tasks_by_date(date):
    todos = session.query(Task).filter(Task.deadline == date.date()).all()
    return todos


def query_all_tasks():
    todos = session.query(Task).order_by(Task.deadline).all()
    return todos


def query_missed_tasks():
    todos = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
    return todos


def query_tasks_by_week():
    today = datetime.today()
    for i in range(0, 7):
        nextday = today + timedelta(days=i)
        todos = query_tasks_by_date(nextday)
        print(date_format(nextday))
        print_all_tasks(todos)




def main():
    while 1:
        if not database_exists('sqlite:///todo.db'):
            Base.metadata.create_all(engine)
        display()
        command = 0
        try:
            command = int(input())
        except ValueError:
            print('Not a number!')
            exit(0)
        print()
        if command == 1:
            today = datetime.today()
            print(today.strftime('Today %#d %b:'))
            print_all_tasks(query_tasks_by_date(today))
        elif command == 2:
            query_tasks_by_week()
        elif command == 3:
            print('All tasks:')
            print_all_tasks(query_all_tasks(), my_format=True)
        elif command == 4:
            print('Missed tasks:')
            print_all_tasks(query_missed_tasks())
        elif command == 5:
            create_new_task()
        elif command == 6:
            print('Choose the number of the task you want to delete:')
            print_all_tasks(query_all_tasks(), my_format=True)
            try:
                delete_number = int(input())
            except ValueError:
                print('Not a number!')
                exit(0)
            delete_tasks(delete_number)
            print('The task has been deleted!')
        elif command == 0:
            print('\nBye!')
            exit(0)


if __name__ == '__main__':
    main()
