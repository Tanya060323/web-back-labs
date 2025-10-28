from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    
    x1 = float(x1) if x1.strip() != '' else 0.0
    x2 = float(x2) if x2.strip() != '' else 0.0
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    
    x1 = float(x1) if x1.strip() != '' else 1.0
    x2 = float(x2) if x2.strip() != '' else 1.0
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    if x1.strip() == '' or x2.strip() == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    
    x1 = float(x1)
    x2 = float(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    if x1.strip() == '' or x2.strip() == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')
    
    x1 = float(x1)
    x2 = float(x2)
    if x1 == 0.0 and x2 == 0.0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'plant' and tree_count < 10:
            tree_count += 1
    elif operation == 'cut' and tree_count > 0:
            tree_count -= 1
        
    return redirect ('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Сидоров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Алексеев', 'gender': 'male'},
    {'login': 'tanya', 'password': '2323', 'name': 'Татьяна Щегорцова', 'gender': 'female'},
    {'login': 'sacha', 'password': '666', 'name': 'Александра Попова', 'gender': 'female'},
    {'login': 'max', 'password': '777', 'name': 'Максим Титов', 'gender': 'male'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user = next((u for u in users if u['login'] == session['login']), None)
            if user:
                name = user['name']
                gender = user['gender']
                gender_text = 'мужской' if gender == 'male' else 'женский'
        else:
            authorized = False
            login = ''
            name = ''
            gender_text = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name, gender_text=gender_text)
    
    login_input = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    
    errors = []
    if not login_input:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    
    if errors:
        return render_template('lab4/login.html', errors=errors, authorized=False, login=login_input)  
    
    user_found = None
    for user in users:
        if login_input == user['login'] and password == user['password']:
            user_found = user
            break
    
    if user_found:
        session['login'] = login_input
        session['name'] = user_found['name']
        session['gender'] = user_found['gender']
        return redirect('/lab4/login')
    else:
        error = 'Неверные логин и/или пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login_input)  
    

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    session.pop('gender', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    temperature = None
    snowflakes = None
    
    if request.method == 'POST':
        temp_str = request.form.get('temperature', '').strip()
        
        if not temp_str:
            error = "Ошибка: не задана температура"
        else:
            try:
                temperature = int(temp_str)
                
                if temperature < -12:
                    error = "Не удалось установить температуру — слишком низкое значение"
                elif temperature > -1:
                    error = "Не удалось установить температуру — слишком высокое значение"
                elif -12 <= temperature <= -9:
                    snowflakes = '❄️❄️❄️'
                elif -8 <= temperature <= -5:
                    snowflakes = '❄️❄️'
                elif -4 <= temperature <= -1:
                    snowflakes = '❄️'
                    
            except ValueError:
                error = "Ошибка: температура должна быть числом"
    
    return render_template('lab4/fridge.html', temperature=temperature, snowflakes=snowflakes, error=error)