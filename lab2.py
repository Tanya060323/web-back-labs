from flask import Blueprint, url_for, request, redirect, abort, render_template
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "Роза", "price": 132},
    {"name": "Тюльпан", "price": 70},
    {"name": "Незабудка", "price": 173},
    {"name": "Ромашка", "price": 22}
]


@lab2.route('/lab2/flowers')
def flowers_all():
    return render_template('flowers.html', flowers=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower.html', flower=flower, id=flower_id)


@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower_with_price(name, price):
    flower_list.append({"name": name, "price": price})
    return render_template('flowers.html', name=name, price=price, flowers=flower_list)


@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '').strip()

    flower_list.append({"name": name, "price": price})
    return redirect(url_for('flowers_all'))


@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    global flower_list
    flower_list = []
    return render_template('flowers_cleared.html')


@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('flowers_all'))


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc_ab', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def calc_a(a):
    return redirect(url_for('lab2.calc_ab', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>/')
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


@lab2.route('/lab2/books/')
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


@lab2.route('/lab2/object/')
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