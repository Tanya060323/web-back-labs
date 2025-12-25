from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from os import path
import re
import os
import time

rgz = Blueprint('rgz', __name__)

import sqlite3
from os import path


UPLOAD_FOLDER = 'static/rgz/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='tatiana_shegorczova_rgz',
            user='tatiana_shegorczova_rgz',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def validate_login(login):
    if not login:
        return False, "Логин не может быть пустым"
    if not re.match(r'^[a-zA-Z0-9_.-]+$', login):
        return False, "Логин должен содержать только латинские буквы, цифры и знаки препинания"
    if len(login) < 3 or len(login) > 30:
        return False, "Логин должен быть от 3 до 30 символов"
    return True, ""

def validate_password(password):
    if not password:
        return False, "Пароль не может быть пустым"
    if len(password) < 5:
        return False, "Пароль должен быть не менее 5 символов"
    if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+=-]+$', password):
        return False, "Пароль должен содержать только латинские буквы, цифры и знаки препинания"
    return True, ""

@rgz.route('/rgz/')
def main():
    return redirect('/rgz/recipes')

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')
    
    if not (login and password and real_name):
        return render_template('rgz/register.html', error='Заполните все поля')
    
    valid, error_msg = validate_login(login)
    if not valid:
        return render_template('rgz/register.html', error=error_msg)
    
    valid, error_msg = validate_password(password)
    if not valid:
        return render_template('rgz/register.html', error=error_msg)
    
    if len(real_name) > 100:
        return render_template('rgz/register.html', error='Имя слишком длинное')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login = ?;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name, is_admin) VALUES (%s, %s, %s, %s);", 
                    (login, password_hash, real_name, False))
    else:
        cur.execute("INSERT INTO users (login, password, real_name, is_admin) VALUES (?, ?, ?, ?);", 
                    (login, password_hash, real_name, 0))
    
    db_close(conn, cur)
    return redirect('/rgz/recipes')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('rgz/login.html', error="Заполните все поля")
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    session['user_id'] = user['id']
    session['is_admin'] = user['is_admin']
    db_close(conn, cur)
    return redirect('/rgz/recipes')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect('/rgz/recipes')

@rgz.route('/rgz/recipes')
def recipes_list():
    conn, cur = db_connect()
    
    search_title = request.args.get('search_title', '').strip()
    search_ingredients = request.args.get('search_ingredients', '').strip()
    search_mode = request.args.get('search_mode', 'any')
    
    if search_title or search_ingredients:
        if search_title and not search_ingredients:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM recipes WHERE title ILIKE %s ORDER BY id DESC;", 
                            ('%' + search_title + '%',))
            else:
                cur.execute("SELECT * FROM recipes WHERE title LIKE ? ORDER BY id DESC;", 
                            ('%' + search_title + '%',))
                            
        elif search_ingredients and not search_title:
            ingredients_list = [ing.strip().lower() for ing in search_ingredients.split(',') if ing.strip()]
            
            if search_mode == 'all':
                if current_app.config['DB_TYPE'] == 'postgres':
                    conditions = ' AND '.join([f"LOWER(ingredients) LIKE %s" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE {conditions} ORDER BY id DESC;"
                    cur.execute(query, [f'%{ing}%' for ing in ingredients_list])
                else:
                    conditions = ' AND '.join([f"LOWER(ingredients) LIKE ?" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE {conditions} ORDER BY id DESC;"
                    cur.execute(query, [f'%{ing}%' for ing in ingredients_list])
            else:
                if current_app.config['DB_TYPE'] == 'postgres':
                    conditions = ' OR '.join([f"LOWER(ingredients) LIKE %s" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE {conditions} ORDER BY id DESC;"
                    cur.execute(query, [f'%{ing}%' for ing in ingredients_list])
                else:
                    conditions = ' OR '.join([f"LOWER(ingredients) LIKE ?" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE {conditions} ORDER BY id DESC;"
                    cur.execute(query, [f'%{ing}%' for ing in ingredients_list])
                    
        else:
            ingredients_list = [ing.strip().lower() for ing in search_ingredients.split(',') if ing.strip()]
            
            if search_mode == 'all':
                if current_app.config['DB_TYPE'] == 'postgres':
                    ing_conditions = ' AND '.join([f"LOWER(ingredients) LIKE %s" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE title ILIKE %s AND {ing_conditions} ORDER BY id DESC;"
                    cur.execute(query, [f'%{search_title}%'] + [f'%{ing}%' for ing in ingredients_list])
                else:
                    ing_conditions = ' AND '.join([f"LOWER(ingredients) LIKE ?" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE title LIKE ? AND {ing_conditions} ORDER BY id DESC;"
                    cur.execute(query, [f'%{search_title}%'] + [f'%{ing}%' for ing in ingredients_list])
            else:
                if current_app.config['DB_TYPE'] == 'postgres':
                    ing_conditions = ' OR '.join([f"LOWER(ingredients) LIKE %s" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE title ILIKE %s AND ({ing_conditions}) ORDER BY id DESC;"
                    cur.execute(query, [f'%{search_title}%'] + [f'%{ing}%' for ing in ingredients_list])
                else:
                    ing_conditions = ' OR '.join([f"LOWER(ingredients) LIKE ?" for _ in ingredients_list])
                    query = f"SELECT * FROM recipes WHERE title LIKE ? AND ({ing_conditions}) ORDER BY id DESC;"
                    cur.execute(query, [f'%{search_title}%'] + [f'%{ing}%' for ing in ingredients_list])
    else:
        cur.execute("SELECT * FROM recipes ORDER BY id DESC;")
    
    recipes = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('rgz/recipes.html', 
                           recipes=recipes,
                           login=session.get('login'),
                           is_admin=session.get('is_admin'),
                           search_title=search_title,
                           search_ingredients=search_ingredients,
                           search_mode=search_mode)

@rgz.route('/rgz/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    if not session.get('is_admin'):
        return redirect('/rgz/recipes')
    
    if request.method == 'GET':
        return render_template('rgz/create_recipe.html')
    
    title = request.form.get('title', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    instructions = request.form.get('instructions', '').strip()
    
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = f"/static/rgz/uploads/{filename}"
    
    if not title:
        return render_template('rgz/create_recipe.html', error="Название рецепта не может быть пустым")
    
    if len(title) > 200:
        return render_template('rgz/create_recipe.html', error="Название рецепта слишком длинное")
    
    if not ingredients:
        return render_template('rgz/create_recipe.html', error="Необходимо указать ингредиенты")
    
    if not instructions:
        return render_template('rgz/create_recipe.html', error="Необходимо указать шаги приготовления")
    
    conn, cur = db_connect()
    user_id = session.get('user_id')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO recipes (title, ingredients, instructions, image_url, user_id) VALUES (%s, %s, %s, %s, %s);",
                    (title, ingredients, instructions, image_url, user_id))
    else:
        cur.execute("INSERT INTO recipes (title, ingredients, instructions, image_url, user_id) VALUES (?, ?, ?, ?, ?);",
                    (title, ingredients, instructions, image_url, user_id))
    
    db_close(conn, cur)
    return redirect('/rgz/recipes')

@rgz.route('/rgz/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if not session.get('is_admin'):
        return redirect('/rgz/recipes')
    
    conn, cur = db_connect()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM recipes WHERE id = %s;", (recipe_id,))
        else:
            cur.execute("SELECT * FROM recipes WHERE id = ?;", (recipe_id,))
        recipe = cur.fetchone()
        
        image_url = recipe['image_url']
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                if image_url and image_url.startswith('/static/rgz/uploads/'):
                    old_filepath = image_url.replace('/static/', 'static/')
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                filename = secure_filename(file.filename)
                filename = f"{int(time.time())}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                image_url = f"/static/rgz/uploads/{filename}"
        
        if not title:
            db_close(conn, cur)
            return render_template('rgz/edit_recipe.html', recipe=recipe, error="Название не может быть пустым")
        
        if not ingredients:
            db_close(conn, cur)
            return render_template('rgz/edit_recipe.html', recipe=recipe, error="Ингредиенты не могут быть пустыми")
        
        if not instructions:
            db_close(conn, cur)
            return render_template('rgz/edit_recipe.html', recipe=recipe, error="Шаги приготовления не могут быть пустыми")
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE recipes SET title = %s, ingredients = %s, instructions = %s, image_url = %s WHERE id = %s;",
                        (title, ingredients, instructions, image_url, recipe_id))
        else:
            cur.execute("UPDATE recipes SET title = ?, ingredients = ?, instructions = ?, image_url = ? WHERE id = ?;",
                        (title, ingredients, instructions, image_url, recipe_id))
        
        db_close(conn, cur)
        return redirect('/rgz/recipes')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM recipes WHERE id = %s;", (recipe_id,))
    else:
        cur.execute("SELECT * FROM recipes WHERE id = ?;", (recipe_id,))
    
    recipe = cur.fetchone()
    db_close(conn, cur)
    
    if not recipe:
        return "Рецепт не найден", 404
    
    return render_template('rgz/edit_recipe.html', recipe=recipe)

@rgz.route('/rgz/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if not session.get('is_admin'):
        return redirect('/rgz/recipes')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT image_url FROM recipes WHERE id = %s;", (recipe_id,))
    else:
        cur.execute("SELECT image_url FROM recipes WHERE id = ?;", (recipe_id,))
    
    recipe = cur.fetchone()
    
    if recipe and recipe['image_url'] and recipe['image_url'].startswith('/static/rgz/uploads/'):
        filepath = recipe['image_url'].replace('/static/', 'static/')
        if os.path.exists(filepath):
            os.remove(filepath)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM recipes WHERE id = %s;", (recipe_id,))
    else:
        cur.execute("DELETE FROM recipes WHERE id = ?;", (recipe_id,))
    
    db_close(conn, cur)
    return redirect('/rgz/recipes')




