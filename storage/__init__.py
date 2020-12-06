import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from entities import User
from entities import Task

# Подключаемся к БД
db_path = '/'.join([str(Path(__file__).parent), '..', 'db', 'database.sqlite'])
db = sqlite3.connect(db_path, check_same_thread=False)

class Storage:
    @staticmethod
    def add_user(user: User):
        """обавление пользователя
        :param user:    новый пользователь
        :type user:     User"""
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                   (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email: str, passwordHash: str) -> User:
        """Найти пользователя по email и паролю
        :param email:       электронная почта
        :type email:        str
        :param passwordHash:    хэш пароля
        :type passwordHash:     str
        :return: пользователь
        :rtype: User
        """
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data and check_password_hash(user_data[2], passwordHash):
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_user_by_email(email: str) -> User:
        """Найти пользователя по email
        :param email:  имейл пользователя
        :type email:   str
        :return:    пользователь
        :rtype:     User"""
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data:
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_user_by_id(id: int) -> User:
        """Найти пользователя по id
        :param id:  идентификатор пользователя
        :type id:   int
        :return:    пользователь
        :rtype:     User"""
        user_data = db.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
        if user_data:
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None
            
    @staticmethod
    def get_task_by_id(task_id: int) -> Task:
        """Найти задачу по id
        :param task_id:  идентификатор задачи
        :type task_id:   int
        :return:    задача
        :rtype:     Task"""
        task_data = db.execute('SELECT * FROM tasks WHERE tasks.id=?', (task_id,)).fetchone()
        if task_data:
            user = Storage.get_user_by_id(task_data[4])
            return Task(id=task_data[0], title=task_data[1], description=task_data[2], status=task_data[3], user=user)
        else:
            return None
            
    @staticmethod
    def get_task_by_user(user_id: int):
        """Найти задачу по пользователю
        :param user_id:  идентификатор пользователя
        :type user_id:  int
        :return:    список задач
        :rtype:     Tasks[]"""
        tasks = db.execute('SELECT tasks.id, tasks.title, tasks.description, tasks.status, tasks.user_id FROM tasks INNER JOIN users ON tasks.user_id = users.id WHERE tasks.user_id=?', (user_id,)).fetchall()
        tasks_list = []
        for task in tasks:
            tasks_list.append(Task(id=task[0],
                                   title=task[1],
                                   description=task[2],
                                   status=task[3],
                                   user=Storage.get_user_by_id(task[4])))
        return tasks_list
    
    @staticmethod
    def add_task(task: Task):
        """Добавление задачи
        :param task:  задача
        :type task:  Task"""
        db.execute('INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)',
                   (task.title, task.description, task.status, task.user.id))
        db.commit() 

    @staticmethod
    def update_task(task: Task):
        """Добавление задачи
        :param task:  задача
        :type task:  Task"""
        db.execute('UPDATE tasks set title=?, description=?, status=? where id=?;',
                   (task.title, task.description, task.status, task.id))
        db.commit()
        
    @staticmethod
    def delete_task(task: Task):
        """Удаление задачи
        :param task:  задача
        :type task:  Task"""
        db.execute('DELETE FROM tasks where tasks.id=?', (task.id,))
        db.commit()
