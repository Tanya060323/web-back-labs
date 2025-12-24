from flask import Blueprint, render_template, request, session, jsonify, redirect

lab9 = Blueprint('lab9', __name__)

opened_boxes = set()

boxes = [
    {'id': 0, 'text': 'С Новым годом! Пусть этот год принесёт вам счастье и радость!', 'img': '/static/lab9/gift1.png'},
    {'id': 1, 'text': 'Желаю вам крепкого здоровья и благополучия в наступающем году!', 'img': '/static/lab9/gift2.png'},
    {'id': 2, 'text': 'Пусть Новый год подарит вам море позитива и улыбок!', 'img': '/static/lab9/gift3.png'},
    {'id': 3, 'text': 'С наступающим! Пусть все мечты сбываются!', 'img': '/static/lab9/gift4.png'},
    {'id': 4, 'text': 'Желаю вам успехов во всех начинаниях и достижения целей!', 'img': '/static/lab9/gift5.png'},
    {'id': 5, 'text': 'Пусть Новый год принесёт вам удачу и процветание!', 'img': '/static/lab9/gift6.png', 'auth': True},
    {'id': 6, 'text': 'С Новым годом! Пусть в вашей жизни будет много радостных моментов!', 'img': '/static/lab9/gift7.png'},
    {'id': 7, 'text': 'Желаю вам тепла, уюта и семейного счастья!', 'img': '/static/lab9/gift8.png', 'auth': True},
    {'id': 8, 'text': 'Пусть Новый год откроет перед вами новые возможности!', 'img': '/static/lab9/gift9.png'},
    {'id': 9, 'text': 'С наступающим Новым годом! Пусть сбудутся все ваши желания!', 'img': '/static/lab9/gift10.png'},
    {'id': 10, 'text': 'Желаю вам море эмоций и незабываемых впечатлений!', 'img': '/static/lab9/gift11.png'},
    {'id': 11, 'text': 'Пусть Новый год будет полон приятных сюрпризов!', 'img': '/static/lab9/gift12.png', 'auth': True}
]

positions = [
    {'top': 10, 'left': 5}, {'top': 15, 'left': 25}, {'top': 8, 'left': 50},
    {'top': 20, 'left': 70}, {'top': 5, 'left': 85}, {'top': 45, 'left': 10},
    {'top': 50, 'left': 35}, {'top': 48, 'left': 60}, {'top': 42, 'left': 80},
    {'top': 75, 'left': 8}, {'top': 70, 'left': 40}, {'top': 72, 'left': 75}
]


@lab9.route('/lab9/')
def lab():
    if 'opened_count' not in session:
        session['opened_count'] = 0

    unopened = len(boxes) - len(opened_boxes)
    
    login = session.get('login')
    
    return render_template('lab9/lab9.html', unopened=unopened, login=login)


@lab9.route('/lab9/rest-api/boxes', methods=['GET'])
def get_boxes():
    result = []
    for i in range(len(boxes)):
        box = boxes[i]
        result.append({
            'id': box['id'],
            'top': positions[i]['top'],
            'left': positions[i]['left'],
            'opened': box['id'] in opened_boxes,
            'need_auth': box.get('auth', False),
            'img': box['img']
        })
    return jsonify(result)


@lab9.route('/lab9/rest-api/open/<int:box_id>', methods=['POST'])
def open_box(box_id):
    if box_id < 0 or box_id >= len(boxes):
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    if box_id in opened_boxes:
        return jsonify({'error': 'Эта коробка уже пуста!'}), 400
    
    if 'opened_count' not in session:
        session['opened_count'] = 0
    
    if session['opened_count'] >= 3:
        return jsonify({'error': 'Вы уже открыли 3 коробки! Больше открывать нельзя.'}), 400
    
    box = boxes[box_id]
    if box.get('auth', False) and 'login' not in session:
        return jsonify({'error': 'Этот подарок доступен только авторизованным пользователям!'}), 403
    
    opened_boxes.add(box_id)
    session['opened_count'] += 1
    
    unopened = len(boxes) - len(opened_boxes)
    
    return jsonify({
        'text': box['text'],
        'img': box['img'],
        'unopened': unopened
    })


@lab9.route('/lab9/rest-api/reset', methods=['POST'])
def reset():
    if 'login' not in session:
        return jsonify({'error': 'Необходима авторизация!'}), 403
    
    opened_boxes.clear()
    session['opened_count'] = 0
    
    return jsonify({'message': 'Дед Мороз наполнил все коробки подарками!'})


@lab9.route('/lab9/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('opened_count', None)
    return redirect('/lab9/')


