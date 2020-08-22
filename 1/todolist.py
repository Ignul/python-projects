from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# Global Variables
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='nothing')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def start_db():
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def text_for_db():
    # Maybe add a check for formatting, date should be YYYY-MM-DD
    text = input('Enter task\n')
    date = input('Enter deadline\n')
    return Table(task=text, deadline=datetime.strptime(date, '%Y-%m-%d'))


def get_today_date():
    today = datetime.today()
    return str(today.day) + ' ' + today.strftime('%b')


def main():
    session = start_db()
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

        # Ugh this is ugly, need to think about rewriting this.
        while True:
            try:
                user_input = int(input())
                if user_input not in [0, 1, 2, 3, 4, 5, 6]:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("That's not a valid number.")
                continue

        if user_input == 0:
            print("Bye!")
            break

        elif user_input == 1:
            rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
            print("Today " + get_today_date() + ":")
            if not rows:
                print("Nothing to do!")
            else:
                for counter, item in enumerate(rows, 1):
                    print(str(counter) + '. ' + str(item.task))

        elif user_input == 2:
            # We need to start at today and look for tasks for all week.
            day_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday",
                        6: "Sunday"}
            for date in range(0, 7):
                start_date = datetime.today() + timedelta(days=date)
                print(
                    day_dict[start_date.weekday()] + ' ' + str(start_date.day) + ' ' + start_date.strftime('%b').lstrip(
                        '0') + ':')
                rows = session.query(Table).filter(Table.deadline == start_date.date()).all()
                if not rows:
                    print("Nothing to do!\n")
                else:
                    for counter, item in enumerate(rows, 1):
                        print(str(counter) + '. ' + str(item.task))
                    print('\n')

        elif user_input == 3:
            rows = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
            if not rows:
                print("Nothing to do!")
            else:
                for counter, item in enumerate(rows, 1):
                    print(str(counter) + '. ' + str(item.task) + '. ' + str(
                        datetime.strftime(item.deadline, '%d %b').lstrip('0')))
                print('\n')

        elif user_input == 4:
            rows = session.query(Table.task, Table.deadline).order_by(Table.deadline).filter(
                Table.deadline < datetime.today().date()).all()
            if not rows:
                print("Missed tasks:")
                print("Nothing is missed!\n")
            else:
                print("Missed tasks:")
                for counter, item in enumerate(rows, 1):
                    print(str(counter) + '. ' + str(item.task) + '. ' + str(
                        datetime.strftime(item.deadline, '%d %b').lstrip('0')))
                print('\n')

        elif user_input == 5:
            new_row = text_for_db()
            session.add(new_row)
            session.commit()
            print("The task has been added!\n")

        elif user_input == 6:
            rows = session.query(Table.task, Table.deadline).order_by(Table.deadline).all()
            if not rows:
                print("Nothing to delete\n")
            else:
                for counter, item in enumerate(rows, 1):
                    print(str(counter) + '. ' + str(item.task) + '. ' + str(
                        datetime.strftime(item.deadline, '%d %b').lstrip('0')))
                numb = int(input('Choose the number of the task you want to delete: '))
                # Need to query the whole table in order to successfully delete, a smart workaround ;)
                rows = session.query(Table).order_by(Table.deadline).all()
                # Also I'm skipping error checking here.
                session.delete(rows[numb - 1])
                session.commit()
                print("The task has been deleted!\n")


if __name__ == '__main__':
    main()
