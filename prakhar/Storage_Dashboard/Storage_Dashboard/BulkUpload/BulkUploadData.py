import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
# table taken from user
# csv file path taken from user
# db name taken from user
# give better viusalization while uploading

def formatDate(date_ddmmyyyy):
    date_dd, date_mm, date_yyyy = date_ddmmyyyy.split("/")
    return date_yyyy+date_mm+date_dd

userdata = pd.read_csv('/root/TAP-2022-Team-2-EE-Big-Build-Assessment/BulkUpload/SampleData/users_sample.csv', index_col=False, delimiter = ',')

# change fromat of date
userdata['onboarded'] = userdata['onboarded'].apply(lambda x : formatDate(x))


try:
    conn = mysql.connect(host='localhost', database='USERMGT', user='root', password='Root@123')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        for i,row in userdata.iterrows():
            sql = "INSERT INTO USERMGT.users (user_name, user_login, user_onboarded, user_dept) VALUES (%s,%s,%s,%s);"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)
