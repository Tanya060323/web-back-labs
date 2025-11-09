from flask import Flask, url_for, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5


import datetime
app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

error_log = []

@app.errorhandler(404)
def not_found(err):
    img_path = url_for('static', filename='lab1/404.jpg')
    css_url = url_for('static', filename='lab1/404.css')

    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестно')

    # Добавляем запись в журнал
    log_entry = {
        'ip': client_ip,
        'time': access_time,
        'url': requested_url,
        'user_agent': user_agent
    }
    error_log.append(log_entry)
    
    # Ограничиваем журнал последними 20 записями
    if len(error_log) > 20:
        error_log.pop(0)

    # Формируем HTML для журнала
    log_html = ""
    for entry in reversed(error_log):  # Показываем последние записи первыми
        log_html += f"""
        <div class="log-entry">
            <span class="log-time">{entry['time']}</span>
            <span class="log-ip">Пользователь: {entry['ip']}</span>
            <span class="log-url">Адрес: {entry['url']}</span>
        </div>
        """

    return """<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Страница не найдена - 404</title>
        <link rel="stylesheet" href='""" + css_url + """'>
    </head>
    <body>
        <div class="container">
            <img src='""" + img_path + """' alt="404" class="image">
            <h1>404</h1>
            <h2>Ой! Страница потерялась</h2>

            <div class="user-info">
                <p><strong>Ваш IP-адрес:</strong> """ + client_ip + """</p>
                <p><strong>Время доступа:</strong> """ + access_time + """</p>
                <p><strong>Запрошенный URL:</strong> """ + requested_url + """</p>
            </div>
            
            <p>Кажется, мы не можем найти страницу, которую вы ищете.<br>
            Возможно, она переехала или никогда не существовала.</p>
            
            <div class="tips">
                <h3>Что можно сделать?</h3>
                <p>* Проверьте правильность URL-адреса</p>
                <p>* Вернитесь на предыдущую страницу</p>
                <p>* Перейдите на главную страницу</p>
                <p>* Или просто наслаждайтесь красотой этой страницы ошибки</p>
            </div>
            
            <a href="/" class="home-btn">Вернуться на главную</a>

            <div class="journal">
                <h3>Журнал обращений:</h3>
                """ + log_html if error_log else '<p>Журнал пуст</p>' + """
            </div>
        </div>
    </body>
</html>""", 404


@app.route("/")
@app.route("/index")
def index():
    return """<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <div>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2/">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвертая лабораторная</a></li>
                <li><a href="/lab5/">Пятая лабораторная</a></li>
            </ul>
        </div>
        
        <footer>
            <hr>
            <div>
                Щегорцова Татьяна Алексеевна, ФБИ-31, 2 курс, 2025 год
            </div>
        </footer>
    </body>
</html>"""


@app.errorhandler(500)
def server_error(err):
    return '''<!doctype html>
    <html>
        <body>
            <h1>500</h1>
            <p>Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.</p>
            <p><a href="/">Вернуться на главную</a></p>
        </body>
    </html>''', 500