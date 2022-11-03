from flask import Flask, render_template, request, session
import pandas as pd
import os
from werkzeug.utils import secure_filename
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
 
#*** Flask configuration
 
# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
 
# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {'csv'}
 
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
def formatDate(date_ddmmyyyy):
    date_dd, date_mm, date_yyyy = date_ddmmyyyy.split("/")
    return date_yyyy+date_mm+date_dd
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['uploaded-file']
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
 
        # Storing uploaded file path in flask session
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
 
        return render_template('index_upload_and_show_data_page2.html')
 
@app.route('/show_data')
def showData():
    # Retrieving uploaded file path from session
    data_file_path = session.get('uploaded_data_file_path', None)
 
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

    # pandas dataframe to html table flask
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html', data_var = uploaded_df_html)
 
if __name__=='__main__':
    app.run(debug = True)