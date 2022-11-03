import pymysql
# from tables import Results
from flask_table import Table, Col, LinkCol
# from db_config import MySQL
from flaskext.mysql import MySQL
from flask import flash, render_template, request, redirect
from flask import Flask
from apps import new_db

from apps.home import blueprint
from flask import render_template, request, url_for, session
from flask_login import login_required
from jinja2 import TemplateNotFound
import pandas as pd
import os
from werkzeug.utils import secure_filename
import mysql.connector as mysql
from mysql.connector import Error
 

class Results(Table):
    user_id = Col('Id', show=False)
    user_name = Col('Name')
    user_login = Col('Login')
    user_onboarded = Col('Onboarded')
    user_dept = Col('Department')
    # delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='user_id'))



@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/users.html')
@login_required
def users():
    # print("\n\n in db users \n\n")
    conn = None
    cursor = None
    try:
        conn = new_db.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print(rows)
        # table = Results(rows)
        # table.border = Tru
        print(rows)
        return render_template('home/users.html', segment='users', value=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        print("\n\n segment check \n\n" + segment)

        # Serve the file (if exists) from app/templates/home/FILE.html
        if template != 'users.html': 
            return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

@blueprint.route('/new_user')
@login_required
def add_user_view():
    return render_template('home/add_user.html', segment='add_user')


@blueprint.route('/add', methods=['POST'])
@login_required
def add_user():
    print(" ################ in add user form function")
    conn = None
    cursor = None
    try:
        _name = request.form['inputName']
        _login = request.form['inputLogin']
        _onboarded = request.form['inputOnboarded']
        _department = request.form['inputDepartment']
        # validate the received values
        if _name and _login and _onboarded and _department and request.method == 'POST':
            # save edits
            # print("################before executing sql")

            sql = "INSERT INTO users (user_name, user_login, user_onboarded, user_dept) VALUES(%s, %s, %s, %s)"
            data = (_name, _login, _onboarded, _department)
            conn = new_db.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            # print(' ################ User added successfully!')
            return redirect(url_for('home_blueprint.users'))
        else:
            return 'Error while adding user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@blueprint.route('/delete/<int:id>')
@login_required
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = new_db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
        conn.commit()
        flash('User deleted successfully!')
        return redirect(url_for('home_blueprint.users'))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@blueprint.route('/bulk_add', methods=['POST'])
@login_required
def bulk_add_users():
    print(" ################ in bulk add user form function")
    
    UPLOAD_FOLDER = os.path.join('/root/project/TAP-2022-Team-2-EE-Big-Build-Assessment/prakhar/Storage_Dashboard/Storage_Dashboard/apps/static', 'uploads')
    print(UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = {'csv'}
    try:
        if request.method == 'POST':
            uploaded_df = request.files['uploaded-file']
            # Extracting uploaded data file name
            print(uploaded_df)
            data_filename = secure_filename(uploaded_df.filename)
    
            # flask upload file to database (defined uploaded folder in static path)
            uploaded_df.save(os.path.join(UPLOAD_FOLDER, data_filename))

            loadData(os.path.join(UPLOAD_FOLDER, data_filename))
            return redirect(url_for('home_blueprint.users'))
        else:
            print("Error in uploading Data")

    except Exception as e:
        print(e)
    finally:
        print("END")
        

def loadData(data_file_path):
    conn = None
    cursor = None 
    # read csv file in python flask (reading uploaded csv file from uploaded server location)
    uploaded_df = pd.read_csv(data_file_path)

    # change fromat of date
    uploaded_df['onboarded'] = uploaded_df['onboarded'].apply(lambda x : formatDate(x))

    try:
        conn = mysql.connect(host='localhost', database='USERMGT', user='root', password='Root@123')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            for i,row in uploaded_df.iterrows():
                sql = "INSERT INTO USERMGT.users (user_name, user_login, user_onboarded, user_dept) VALUES (%s,%s,%s,%s);"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                conn.commit()
    except Error as e:
                print("Error while connecting to MySQL", e)
    finally:
        cursor.close()
        conn.close()


def formatDate(date_ddmmyyyy):
    date_dd, date_mm, date_yyyy = date_ddmmyyyy.split("/")
    return date_yyyy+date_mm+date_dd