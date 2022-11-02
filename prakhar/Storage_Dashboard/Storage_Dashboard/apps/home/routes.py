import pymysql
# from tables import Results
from flask_table import Table, Col, LinkCol
# from db_config import MySQL
from flaskext.mysql import MySQL
from flask import flash, render_template, request, redirect
from flask import Flask
from apps import new_db

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


class Results(Table):
    user_id = Col('Id', show=False)
    user_name = Col('Name')
    user_login = Col('Login')
    user_onboarded = Col('Onboarded')
    user_dept = Col('Department')
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='user_id'))



@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


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
            sql = "INSERT INTO users (user_name, user_login, user_onboarded, user_dept) VALUES(%s, %s, %s, %s)"
            data = (_name, _login, _onboarded, _department)
            conn = new_db.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User added successfully!')
            return redirect('/users', segment='users')
        else:
            return 'Error while adding user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    conn.close()


@blueprint.route('/db_users')
@login_required
def users():
    print("\n\n in db users \n\n")
    return render_template('home/users.html', segment='users')
    # conn = None
    # cursor = None
    # try:
    #     # conn = new_db.connect()
    #     # cursor = conn.cursor(pymysql.cursors.DictCursor)
    #     # cursor.execute("SELECT * FROM users")
    #     # rows = cursor.fetchall()
    #     # print(rows)
    #     # table = Results(rows)
    #     # table.border = True
    #     return render_template('users.html', segment='users')
    # except Exception as e:
    #     print("exceptio hai####################")
    #     print(e)
    # finally:
    #     print("The END######")
    #     cursor.close()
    #     conn.close()

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
        return redirect('/')
        # TODO :  add segment
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()