import pymysql
from app import app
from tables import Results
from db_config import MySQL
from flask import flash, render_template, request, redirect

mysql = MySQL(app)


@app.route('/new_user')
def add_user_view():
    return render_template('add_user.html')


@app.route('/add', methods=['POST'])
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
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User added successfully!')
            return redirect('/')
        else:
            return 'Error while adding user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    conn.close()


@app.route('/')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print(rows)
        table = Results(rows)
        table.border = True
        return render_template('users.html', table=table)
    except Exception as e:
        print("exceptio hai####################")
        print(e)
    finally:
        print("The END######")
        cursor.close()
        conn.close()


@app.route('/delete/<int:id>')
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=%s", (id,))
        conn.commit()
        flash('User deleted successfully!')
        return redirect('/')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
