from bottle import run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

conn = pymysql.connect(host='0.0.0.0',
                       user='root',
                       password='uncledr3w',
                       db='store',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
	return template("pages/admin.html")


@get("/categories")
def list_categories():
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM categories'
            cursor.execute(sql)
            categories = cursor.fetchall()
            status = 'SUCCESS'
            msg = ''
            code = 200
    except Exception as e:
        status = 'ERROR'
        msg = 'Internal Error'
        code = 500
    result = {'CATEGORIES': categories, 'STATUS': status, 'MSG': msg, 'CODE': code}
    return json.dumps(result)


@post("/category")
def add_category():
    new_category = request.POST.get('name')
    if new_category == '':
        status = 'ERROR'
        msg = 'Name parameter is missing'
        code = 400
        result = {'STATUS': status, 'MSG': msg, 'CODE': code}
        return json.dumps(result)
    try:
        with conn.cursor() as cursor:
            sql_query = "SELECT count(*) as count FROM categories where name='{}'".format(new_category)
            cursor.execute(sql_query)
            result = cursor.fetchone()
            if result['count'] > 0:
                status = 'ERROR'
                msg = 'Category already exists'
                code = 200
            else:
                sql_insert = "INSERT INTO categories (name) VALUES ('{}')".format(new_category)
                cursor.execute(sql_insert)
                conn.commit()
                status = 'SUCCESS'
                msg = ''
                code = 201
        result = {'STATUS': status, 'MSG': msg, 'CODE': code}
        return json.dumps(result)
    except Exception as e:
        status = 'ERROR'
        msg = 'Internal Error'
        code = 500
    result = {'STATUS': status, 'MSG': msg, 'CODE': code}
    return json.dumps(result)


@delete("/category/<id>")
def delete_category(id):
    try:
        with conn.cursor() as cursor:
            sql_query = "SELECT count(*) as count FROM categories WHERE id={}".format(id)
            cursor.execute(sql_query)
            result = cursor.fetchone()
            if result['count'] == 0:
                status = 'ERROR'
                msg = 'Category not found'
                code = 404
            else:
                sql_insert = "DELETE FROM categories WHERE id={}".format(id)
                cursor.execute(sql_insert)
                status = 'SUCCESS'
                msg = 'category deleted successfully'
                code = 201
        result = {'STATUS': status, 'MSG': msg, 'CODE': code}
        return json.dumps(result)
    except Exception as e:
        status = 'ERROR'
        msg = 'Internal Error'
        code = 500
    result = {'STATUS': status, 'MSG': msg, 'CODE': code}
    return json.dumps(result)


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='0.0.0.0', port=argv[1])
