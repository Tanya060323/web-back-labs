from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)


@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404


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


@app.route("/lab1")
def lab1():
    return """<!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Лабораторная 1</title>
        </head>
        <body>
            <h1>Лабораторная работа 1</h1>
            
            <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.
            </p>
            
            <a href="/">На главную</a>

            <h2>Список роутов:</h2>
                <ul>
                    <li><a href="/lab1/web">/lab1/web</a></li>
                    <li><a href="/lab1/author">/lab1/author</a></li>
                    <li><a href="/lab1/image">/lab1/image</a></li>
                    <li><a href="/lab1/counter">/lab1/counter</a></li>
                    <li><a href="/lab1/counter/clear">/lab1/counter/clear</a></li>
                    <li><a href="/lab1/info">/lab1/info</a></li>
                    <li><a href="/lab1/created">/lab1/created</a></li>
                    <li><a href="/lab1/error/400">/lab1/error/400</a></li>
                    <li><a href="/lab1/error/401">/lab1/error/401</a></li>
                    <li><a href="/lab1/error/402">/lab1/error/402</a></li>
                    <li><a href="/lab1/error/403">/lab1/error/403</a></li>
                    <li><a href="/lab1/error/405">/lab1/error/405</a></li>
                    <li><a href="/lab1/error/418">/lab1/error/418</a></li>
                    <li><a href="/lab1/trigger500">/lab1/trigger500</a></li>
                </ul>
        </body>
    </html>"""


@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
            <body> 
                <h1>web-сервер на flask</h1> 
                <a href="/author">author</a>
            </body> 
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/plain; charset=utf-8"
        }



@app.route("/lab1/author")
def author():
    name = "Щегорцова Татьяна Алексеевна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html> 
            <body> 
                <p> Студент: """ + name + """</p>
                <p> Группа: """ + group + """</p>
                <p> Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body> 
        </html>"""


@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css_url = url_for("static", filename="lab1.css")

    return '''
<!doctype html>
<html> 
    <head>
        <link rel="stylesheet" href="''' + css_url + '''">
        <title>Дуб</title>
    </head>
    <body> 
        <div class="container">
            <h1>Дуб</h1>
            <img src="''' + path + '''" alt="Дуб" class="oak-image">
            <p class="description">Величественное дерево с мощным стволом</p>
        </div>
    </body> 
</html>
'''


count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html> 
    <body> 
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + str(url) + '''<br>
        Ваш IP-адрес: ''' + str(client_ip) + '''<br>
        <a href="/lab1/counter/reset">Сбросить счетчик</a>
    </body> 
</html>
'''

@app.route("/lab1/counter/reset")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body> 
</html>
''',201



        