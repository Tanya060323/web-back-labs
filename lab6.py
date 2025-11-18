from flask import Blueprint, render_template, request, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from os import path

lab6 = Blueprint('lab6', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='tatiana_shegorczova_knowledge_base',
            user='tatiana_shegorczova_knowledge_base',
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

def init_offices_table():
    with current_app.app_context():
        conn, cur = db_connect()
        
        if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
            cur.execute('''
                CREATE TABLE IF NOT EXISTS offices (
                    number INTEGER PRIMARY KEY,
                    tenant TEXT,
                    price INTEGER
                )
            ''')
        else:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS offices (
                    number INTEGER PRIMARY KEY,
                    tenant TEXT,
                    price INTEGER
                )
            ''')
        
        if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
            cur.execute('SELECT COUNT(*) FROM offices')
        else:
            cur.execute('SELECT COUNT(*) FROM offices')
            
        result = cur.fetchone()
        if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
            count = result['count'] if 'count' in result else result[0] if isinstance(result, (tuple, list)) else 0
        else:
            count = result[0] if result else 0
        
        if count == 0 or count < 10:
            if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
                cur.execute('DELETE FROM offices')
            else:
                cur.execute('DELETE FROM offices')
            
            for i in range(1, 11):
                if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
                    cur.execute(
                        'INSERT INTO offices (number, tenant, price) VALUES (%s, %s, %s)',
                        (i, '', 900 + i * 10)
                    )
                else:
                    cur.execute(
                        'INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)',
                        (i, '', 900 + i * 10)
                    )
        
        db_close(conn, cur)

def get_offices():
    conn, cur = db_connect()
    
    if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
        cur.execute('SELECT number, tenant, price FROM offices ORDER BY number')
    else:
        cur.execute('SELECT number, tenant, price FROM offices ORDER BY number')
    
    offices = []
    for row in cur.fetchall():
        if isinstance(row, dict):  
            offices.append({
                'number': row['number'],
                'tenant': row['tenant'],
                'price': row['price']
            })
        else:  
            offices.append({
                'number': row[0],
                'tenant': row[1],
                'price': row[2]
            })
    db_close(conn, cur)
    return offices

def update_office_tenant(office_number, tenant):
    conn, cur = db_connect()
    
    if current_app.config.get('DB_TYPE', 'sqlite') == 'postgres':
        cur.execute(
            'UPDATE offices SET tenant = %s WHERE number = %s',
            (tenant, office_number)
        )
    else:
        cur.execute(
            'UPDATE offices SET tenant = ? WHERE number = ?',
            (tenant, office_number)
        )
    
    db_close(conn, cur)

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html', current_user=session.get('login'))

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        offices = get_offices()
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id 
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        offices = get_offices()
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                update_office_tenant(office_number, login)
                return {
                    'jsonrpc': '2.0',
                    'result': 'Booking successful',
                    'id': id
                }
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        }
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        offices = get_offices()
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel another user\'s booking'
                        },
                        'id': id
                    }
                update_office_tenant(office_number, '')
                return {
                    'jsonrpc': '2.0',
                    'result': 'Cancellation successful',
                    'id': id
                }
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }