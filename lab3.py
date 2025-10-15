from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    display_name = name if name else "аноним"

    return render_template('lab3/lab3.html', name=display_name, 
                         name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Tanya', max_age=5)
    resp.set_cookie('age', '19')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user') 

    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    sex = request.args.get('sex')
    
    if age == '':
        errors['age'] = 'Заполните поле!'

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors = errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    
    if color or bg_color or font_size or font_family:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')
    
    resp = make_response(render_template('lab3/settings.html', 
                                         color=color, 
                                         bg_color=bg_color, 
                                         font_size=font_size, 
                                         font_family=font_family))
    return resp


@lab3.route('/lab3/settings/clear')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    if not fio:
        errors['fio'] = 'Заполните поле!'
    if not shelf:
        errors['shelf'] = 'Выберите полку!'
    if not age:
        errors['age'] = 'Заполните поле!'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
    if not departure:
        errors['departure'] = 'Заполните поле!'
    if not destination:
        errors['destination'] = 'Заполните поле!'
    if not date:
        errors['date'] = 'Заполните поле!'
    
    price = 0
    if not errors and fio:
        if age and int(age) < 18:
            price = 700  
            ticket_type = "Детский билет"
        else:
            price = 1000  
            ticket_type = "Взрослый билет"
        
        if shelf in ['lower', 'lower-side']:
            price += 100
        if linen == 'on':
            price += 75
        if luggage == 'on':
            price += 250
        if insurance == 'on':
            price += 150
    
    return render_template('lab3/ticket.html',
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, errors=errors,
                         price=price, ticket_type=ticket_type if not errors and fio else '')


@lab3.route('/lab3/search')
def search():
    products = [
        {'name': 'iPhone 13', 'price': 79999, 'brand': 'Apple', 'color': 'black'},
        {'name': 'Samsung Galaxy S21', 'price': 69999, 'brand': 'Samsung', 'color': 'white'},
        {'name': 'Google Pixel 6', 'price': 46799, 'brand': 'Google', 'color': 'gray'},
        {'name': 'Xiaomi Mi 11', 'price': 34899, 'brand': 'Xiaomi', 'color': 'blue'},
        {'name': 'OnePlus 9', 'price': 27899, 'brand': 'OnePlus', 'color': 'black'},
        {'name': 'iPhone 12', 'price': 49999, 'brand': 'Apple', 'color': 'red'},
        {'name': 'Samsung Galaxy A52', 'price': 29999, 'brand': 'Samsung', 'color': 'blue'},
        {'name': 'Google Pixel 5a', 'price': 32999, 'brand': 'Google', 'color': 'black'},
        {'name': 'Xiaomi Redmi Note 10', 'price': 19999, 'brand': 'Xiaomi', 'color': 'white'},
        {'name': 'OnePlus Nord 2', 'price': 78999, 'brand': 'OnePlus', 'color': 'gray'},
        {'name': 'iPhone SE', 'price': 69999, 'brand': 'Apple', 'color': 'white'},
        {'name': 'Samsung Galaxy Z Flip', 'price': 89999, 'brand': 'Samsung', 'color': 'purple'},
        {'name': 'Google Pixel 4a', 'price': 45766, 'brand': 'Google', 'color': 'black'},
        {'name': 'Xiaomi Poco X3', 'price': 23999, 'brand': 'Xiaomi', 'color': 'blue'},
        {'name': 'OnePlus 8T', 'price': 45799, 'brand': 'OnePlus', 'color': 'green'},
        {'name': 'iPhone 11', 'price': 41999, 'brand': 'Apple', 'color': 'yellow'},
        {'name': 'Samsung Galaxy S20', 'price': 59999, 'brand': 'Samsung', 'color': 'gray'},
        {'name': 'Google Pixel 4', 'price': 23999, 'brand': 'Google', 'color': 'white'},
        {'name': 'Xiaomi Mi 10T', 'price': 56799, 'brand': 'Xiaomi', 'color': 'black'},
        {'name': 'OnePlus 7T', 'price': 45888, 'brand': 'OnePlus', 'color': 'blue'}
    ]
    
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Получаем значения из куки, если они есть
    if not min_price:
        min_price = request.cookies.get('min_price', '')
    if not max_price:
        max_price = request.cookies.get('max_price', '')
    
    filtered_products = products
    search_performed = False
    
    if min_price or max_price:
        search_performed = True
        try:
            min_val = float(min_price) if min_price else 0
            max_val = float(max_price) if max_price else float('inf')
            
            # Если пользователь перепутал min и max
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = max_price, min_price
            
            filtered_products = [
                p for p in products 
                if min_val <= p['price'] <= max_val
            ]
            
            # Сохраняем в куки
            resp = make_response(render_template(
                'lab3/search.html',
                products=filtered_products,
                min_price=min_price,
                max_price=max_price,
                search_performed=search_performed
            ))
            if min_price:
                resp.set_cookie('min_price', min_price)
            if max_price:
                resp.set_cookie('max_price', max_price)
            return resp
            
        except ValueError:
            filtered_products = []
    
    return render_template('lab3/search.html',
                         products=filtered_products,
                         min_price=min_price,
                         max_price=max_price,
                         search_performed=search_performed)

@lab3.route('/lab3/reset_search')
def reset_search():
    resp = make_response(redirect('/lab3/search'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp