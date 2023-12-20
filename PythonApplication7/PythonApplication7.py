# Τΰιλ main.py
from menu import Menu

menu = Menu()
menu.run()

# Τΰιλ user.py
class User:
    def __init__(self, user_id, name, email, password):
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

# Τΰιλ project.py
class Project:
    def __init__(self, project_id, title, description):
        self.__project_id = project_id
        self.__title = title
        self.__description = description

    def get_project_id(self):
        return self.__project_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

# Τΰιλ task.py
class Task:
    def __init__(self, task_id, project_id, title, description):
        self.__task_id = task_id
        self.__project_id = project_id
        self.__title = title
        self.__description = description

    def get_task_id(self):
        return self.__task_id

    def get_project_id(self):
        return self.__project_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

# Τΰιλ database.py
import sqlite3

class Database:
    def __init__(self, db_name):
        self.__connection = sqlite3.connect(db_name)
        self.__cursor = self.__connection.cursor()

    def create_tables(self):
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)

        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS Projects (
                project_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)

        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                task_id INTEGER PRIMARY KEY,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES Projects (project_id)
            )
        """)

        self.__connection.commit()

    def get_user(self, user_id):
        self.__cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        row = self.__cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2], row[3])
        return None

    def get_projects(self, user_id):
        self.__cursor.execute("SELECT * FROM Projects")
        rows = self.__cursor.fetchall()
        projects = []
        for row in rows:
            projects.append(Project(row[0], row[1], row[2]))
        return projects

    def get_tasks(self, project_id):
        self.__cursor.execute("SELECT * FROM Tasks WHERE project_id = ?", (project_id,))
        rows = self.__cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Task(row[0], row[1], row[2], row[3]))
        return tasks

    def add_user(self, name, email, password):
        self.__cursor.execute("INSERT INTO Users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        self.__connection.commit()

    def add_project(self, title, description):
        self.__cursor.execute("INSERT INTO Projects (title, description) VALUES (?, ?)", (title, description))
        self.__connection.commit()

    def add_task(self, project_id, title, description):
        self.__cursor.execute("INSERT INTO Tasks (project_id, title, description) VALUES (?, ?, ?)", (project_id, title, description))
        self.__connection.commit()

    def delete_project(self, project_id):
        self.__cursor.execute("DELETE FROM Projects WHERE project_id = ?", (project_id,))
        self.__connection.commit()

    def delete_task(self, task_id):
        self.__cursor.execute("DELETE FROM Tasks WHERE task_id = ?", (task_id,))
        self.__connection.commit()

# Τΰιλ validation.py
import re

def validate_email(email):
    email_regex = r'^[\w\.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
    return re.match(email_regex, email)

def validate_password(password):
    return len(password) >= 8

# Τΰιλ menu.py
import sys
from user import User
from project import Project
from task import Task
from database import Database
from validation import validate_email, validate_password

class Menu:
    def __init__(self):
        self.database = Database(":memory:")
        self.database.create_tables()

    def run(self):
        while True:
            print("=== Project Management System ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def register_user(self):
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if not validate_email(email):
            print("Invalid email format.")
            return

        if not validate_password(password):
            print("Password must be at least 8 characters long.")
            return

        self.database.add_user(name, email, password)
        print("User registered successfully!")

    def login_user(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        user = self.database.get_user(email)
        if user and user.get_password() == password:
            self.user_menu(user.get_user_id())
        else:
            print("Invalid email or password. Please try again.")

    def user_menu(self, user_id):
        while True:
            print("=== Projects ===")
            projects = self.database.get_projects(user_id)
            if projects:
                for project in projects:
                    print(f"{project.get_project_id()}. {project.get_title()}")
                print("=====================")
            else:
                print("No projects found.")
                print("=====================")

            print("1. Add Project")
            print("2. View Project Tasks")
            print("3. Add Task")
            print("4. Delete Project")
            print("5. Delete Task")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_project(user_id)
            elif choice == "2":
                project_id = input("Enter project ID: ")
                self.view_project_tasks(project_id)
            elif choice == "3":
                project_id = input("Enter project ID: ")
                self.add_task(project_id)
            elif choice == "4":
                project_id = input("Enter project ID: ")
                self.delete_project(project_id)
            elif choice == "5":
                task_id = input("Enter task ID: ")
                self.delete_task(task_id)
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def add_project(self, user_id):
        title = input("Enter project title: ")
        description = input("Enter project description: ")

        self.database.add_project(title, description)
        print("Project added successfully!")

    def view_project_tasks(self, project_id):
        tasks = self.database.get_tasks(project_id)
        if tasks:
            print("=== Project Tasks ===")
            for task in tasks:
                print(f"Task ID: {task.get_task_id()}")
                print(f"Title: {task.get_title()}")
                print(f"Description: {task.get_description()}")
                print("------------------")
        else:
            print("No tasks found for the project.")

    def add_task(self, project_id):
        title = input("Enter task title: ")
        description = input("Enter task description: ")

        self.database.add_task(project_id, title, description)
        print("Task added successfully!")

    def delete_project(self, project_id):
        self.database.delete_project(project_id)
        print(f"Project {project_id} deleted successfully!")

    def delete_task(self, task_id):
        self.database.delete_task(task_id)
        print(f"Task {task_id} deleted successfully!")
