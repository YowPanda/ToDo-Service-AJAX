from flask import Flask, session, render_template, redirect, request, url_for
from entities import User
from entities import Task
from storage import Storage
import re

# Создаём приложение
app = Flask(__name__)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'_5#y2L"F4Q8ziDec]/'

# Описываем основные маршруты и их обработчики
# Главная страница
@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/index.html', user=user)
    else:
        return redirect('/login')


# Страница с формой входа
@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect('/')
    return render_template('pages/login.html', page_title='Auth Example')


# Обработка формы входа
@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход / Auth Example'

    # Введённые данные получаем из тела запроса
    if not request.form['email']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести email')
    if not request.form['password']:
        return render_template('pages/login.html', page_title=page_title, error='Требуется ввести пароль')

    # Ищем пользователя в БД с таким email паролем
    user = Storage.get_user_by_email_and_password(request.form['email'], request.form['password'])

    # Неверный пароль
    if not user:
        return render_template('pages/login.html', page_title=page_title, error='Неверный пароль')

    # Сохраняем пользователя в сессии
    session['user_id'] = user.id

    # Перенаправляем на главную страницу
    return redirect(url_for('home'))


# Форма регистрации
@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация / Auth Example')


# Обработка формы регистрации
@app.route('/registration', methods=['POST'])
def registration_action():
    page_title = 'Регистрация | Auth Example'
    error = None
    # Проверяем данные
    if not request.form['email']:
        error = 'Требуется ввести Email'
    elif not request.form['password']:
        error = 'Требуется ввести пароль'
    elif not request.form['password2']:
        error = 'Требуется ввести повтор пароля'
    elif request.form['password'] != request.form['password2']:
        error = 'Пароли не совпадают'
    elif not re.search(r'[A-Z]{1}', request.form['password']):
        error = 'В пароле нет заглавной латинской буквы'
    elif not re.search(r'[a-z]{1}',request.form['password']):
        error = 'В пароле нет прописной латинской буквы'
    elif not re.search(r'[0-9]{1}',request.form['password']):
        error = 'В пароле нет цифры'
    elif not re.search(r'[@!/+-=%*]{1}',request.form['password']):
        error = 'В пароле нет спецсимвола'
    elif not re.search(r'[0-9a-zA-Z@!/+-=%*]{8,}', request.form['password']):
        error = 'В пароле меньше восьми символов'
    elif Storage.get_user_by_email(request.form['email']):
        error = 'Пользователь с таким email уже зарегестрирован'

    # В случае ошибки рендерим тот же шаблон, но с текстом ошибки
    if error:
        return render_template('pages/registration.html', page_title=page_title, error=error)

    # Добавляем пользователя
    Storage.add_user(User(None, request.form['email'], request.form['password']))

    # Делаем вид, что добавление всегда без ошибки
    # Перенаправляем на главную
    return redirect(url_for('home'))


# Выход пользователя
@app.route('/logout')
def logout():
    # Просто выкидываем его из сессии
    session.pop('user_id')
    return redirect(url_for('home'))

# Вывод задач 
@app.route('/tasks', methods=['GET'])
def show_tasks():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        tasks = Storage.get_task_by_user(user_id)
        return render_template('pages/task_list.html', page_title = 'Список задач', tasks = tasks, user = user)
    else:
        return redirect('/login')
       
# Добавление задачи       
@app.route('/task', methods=['GET'])
def new_task():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        return render_template('pages/new_task.html', page_title = 'Добавить задачу', user = user)
    else:
        return redirect('/login')

# Создание задачи
@app.route('/task', methods=['POST'])
def create_task():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        status = ('status-input' in request.form) if 1 else 0

        error = None
        if not request.form['title-input']:
            error = 'Необходимо ввести заголовок задачи'
        if error:
            return render_template('pages/new_task.html', page_title = 'Добавить задачу', error = error, user = user)
        Storage.add_task(Task(None, request.form['title-input'], request.form['description-input'], status, user))
        return redirect(url_for('show_tasks'))
    else:
        redirect(url_for('home'))
        
# Получение задачи
@app.route('/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id: int):
    if 'user_id' in session:
        user_id = session['user_id']
        user = Storage.get_user_by_id(user_id)
        task = Storage.get_task_by_id(task_id)
        return render_template('pages/task.html', page_title = "Отредактировать задачу", task = task, user = user)
    else:
        return redirect('/login')
        
# Обновление или удаление задачи
@app.route('/task/<int:task_id>', methods = ['PATCH', 'DELETE'])
def task(task_id: int):
    if request.method == 'PATCH':
        if 'user_id' in session:
            user_id = session['user_id']
            user = Storage.get_user_by_id(user_id)
            dataObj = request.json

            error = None
            if not dataObj['title-input']:
                error = 'Необходимо ввести заголовок задачи'
            if error:
                return render_template('pages/new_task.html', page_title = 'Обновить задачу', error = error, user = user)
            Storage.update_task(Task(dataObj['id'], dataObj['title-input'], dataObj['description-input'], dataObj['status-input'], None))
            return 'ok'
        else:
            redirect(url_for('home'))
    elif (request.method == 'DELETE'):
        if 'user_id' in session:
            user_id = session['user_id']
            Storage.delete_task(Task(int(request.json['id']), None, None, None, None))
            return 'ok'
        else:
            return redirect('/login')

if __name__ == '__main__':
    app.env = 'development'
    app.run(port=8080, host='127.0.0.1', debug=True)
