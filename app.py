from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

error_log = []

@app.errorhandler(404)
def not_found(err):
    img_path = url_for('static', filename='404.jpg')
    css_url = url_for('static', filename='404.css')

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
                    <li><a href="/lab1/counter/reset">/lab1/counter/reset</a></li>
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
                <a href="/lab1/author">author</a>
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
                <a href="/lab1/web">web</a>
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
</html>''', 200, {'Content-Type': 'text/html; charset=utf-8',
        'Content-Language': 'ru',
        'X-Developer': 'Shchegorcova Tanya',  
        'X-Project': 'Flask-Labs',
}

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


@app.route("/lab1/error/400")
def error400():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
    </body> 
</html>
''', 400, {'Content-Type': 'text/html; charset=utf-8'}


@app.route("/lab1/error/401")
def error401():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>401 Unauthorized</h1>
        <p>Требуются учетные данные для доступа к ресурсу.</p>
    </body> 
</html>
''', 401, {'Content-Type': 'text/html; charset=utf-8','WWW-Authenticate': 'Basic realm="Login Required"'}


@app.route("/lab1/error/402")
def error402():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>402 Payment Required</h1>
        <p>Для доступа к ресурсу требуется оплата.</p>
    </body> 
</html>
''', 402, {'Content-Type': 'text/html; charset=utf-8'}


@app.route("/lab1/error/403")
def error403():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
    </body> 
</html>
''', 403, {'Content-Type': 'text/html; charset=utf-8'}


@app.route("/lab1/error/405")
def error405():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>405 Method Not Allowed</h1>
        <p>Метод, указанный в запросе, не разрешен для данного ресурса.</p>
    </body> 
</html>
''', 405, {'Content-Type': 'text/html; charset=utf-8','Allow': 'GET'}


@app.route("/lab1/error/418")
def error418():
    return '''
<!doctype html>
<html> 
    <body> 
        <h1>I'm a teapot</h1>
        <p>Я чайник</p>
    </body> 
</html>
''', 418, {'Content-Type': 'text/html; charset=utf-8'}


@app.route('/lab1/trigger500')
def trigger_500():
    return 1 / 0

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


# ЛАБОРАТОРНАЯ РАБОТА 2

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "Роза", "price": 132},
    {"name": "Тюльпан", "price": 70},
    {"name": "Незабудка", "price": 173},
    {"name": "Ромашка", "price": 22}
]

@app.route('/lab2/flowers')
def flowers_all():
    return render_template('flowers.html', flowers=flower_list)

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower.html', flower=flower, id=flower_id)

@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower_with_price(name, price):
    flower_list.append({"name": name, "price": price})
    return render_template('flowers.html', name=name, price=price, flowers=flower_list)

@app.route('/lab2/add_flower/')
def add_flower():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()

    flower_list.append({"name": name, "price": price})
    return redirect(url_for('flowers_all'))

@app.route('/lab2/flowers/clear')
def clear_flowers():
    global flower_list
    flower_list = []
    return render_template('flowers_cleared.html')

@app.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('flowers_all'))


@app.route('/lab2/example')
def example():
    name = 'Татьяна Щегорцова'
    number = '2'
    group = 'ФБИ-31'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, number=number, group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc_ab', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(url_for('calc_ab', a=a, b=1))

@app.route('/lab2/calc/<int:a>/<int:b>/')
def calc_ab(a, b):
    add = a + b
    sub = a - b
    mul = a * b

    if b == 0:
        div = "На 0 делить нельзя"
    else:
        if a % b == 0:
            div = str(a // b)
        else:
            div = f"{a / b:.2f}"

    power = a ** b

    return render_template(
        'calc.html',
        a=a, b=b,
        add=add, sub=sub, mul=mul, div=div, power=power
    )

@app.route('/lab2/books/')
def show_books():
    books = [
        {"author": "Джоан Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 432},
        {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
        {"author": "Рей Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Научная фантастика", "pages": 256},
        {"author": "Джон Р. Р. Толкин", "title": "Властелин колец: Братство кольца", "genre": "Фэнтези", "pages": 576},
        {"author": "Агата Кристи", "title": "Убийство в Восточном экспрессе", "genre": "Детектив", "pages": 320},
        {"author": "Стивен Кинг", "title": "Оно", "genre": "Ужасы", "pages": 1248},
        {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 384},
        {"author": "Пауло Коэльо", "title": "Алхимик", "genre": "Притча", "pages": 208},
        {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Роман", "pages": 416},
        {"author": "Маргарет Митчелл", "title": "Унесённые ветром", "genre": "Исторический роман", "pages": 1024},
        {"author": "Артур Конан Дойл", "title": "Приключения Шерлока Холмса", "genre": "Детектив", "pages": 352},
        {"author": "Дэн Браун", "title": "Код да Винчи", "genre": "Триллер", "pages": 480},
        {"author": "Сергей Лукьяненко", "title": "Ночной дозор", "genre": "Городское фэнтези", "pages": 448},
        {"author": "Борис Акунин", "title": "Азазель", "genre": "Исторический детектив", "pages": 304},
        {"author": "Виктор Пелевин", "title": "Generation П", "genre": "Постмодернизм", "pages": 320}
    ]
    return render_template('books.html', books=books)

@app.route('/lab2/object/')
def object():
    frut = [
        {"name": "Авокадо", "image": "авакадо.jpg", "desc": "Вечнозелёное плодовое растение"},
        {"name": "Ананас", "image": "ананас.webp", "desc": "Травянистое растение с колючим стеблем и плодом"},
        {"name": "Апельсин", "image": "апельсин.jpg", "desc": "Дерево рода цитрус"},
        {"name": "Арбуз", "image": "арбуз.webp", "desc": "Однолетняя бахчевая культура с ползучими стеблями"},
        {"name": "Банан", "image": "банан.webp", "desc": "Крупное травянистое растение со съедобными плодами"},
        {"name": "Гранат", "image": "гранат.jpg", "desc": "Листопадное дерево или кустарник с шарообразными плодами"},
        {"name": "Грейпфрут", "image": "грейпфрут.jpg", "desc": "Субтропическое вечнозелёное дерево"},
        {"name": "Груша", "image": "груша.webp", "desc": "Листопадное дерево подсемейства яблоневых"},
        {"name": "Дыня", "image": "дыня.jpg", "desc": "Теплолюбивое растение семейства тыквенных"},
        {"name": "Киви", "image": "киви.jpg", "desc": "Древовидная лиана с опушёнными плодами"},
        {"name": "Кокос", "image": "кокос.jpg", "desc": "Высокое растение семейства пальмовых"},
        {"name": "Лайм", "image": "лайм.webp", "desc": "Колючий кустарник или дерево рода цитрус"},
        {"name": "Лимон", "image": "лимон.jpg", "desc": "Небольшое вечнозелёное плодовое дерево"},
        {"name": "Личи", "image": "личи.jpg", "desc": "Тропическое плодовое дерево с пупырчатой кожурой"},
        {"name": "Манго", "image": "манго.png", "desc": "Тропическое дерево с крупными косточковыми плодами"},
        {"name": "Мандарин", "image": "мандарин.jpg", "desc": "Невысокое вечнозелёное дерево"},
        {"name": "Персик", "image": "персик.webp", "desc": "Листопадное дерево с бархатистыми плодами"},
        {"name": "Слива", "image": "слива.jpeg", "desc": "Плодовое растение подсемейства сливовые"},
        {"name": "Яблоко", "image": "яблоко.jpg", "desc": "Широко распространённое плодовое дерево"},
        {"name": "Виноград", "image": "виноград.jpg", "desc": "Многолетняя лиана с древесным стеблем"}
    ]
    return render_template('object.html', frut=frut)