from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    os.system("df -h > filesize")
    
    file1 = open('filesize', 'r')
    s = ""
    while True:   
        # Get next line from file
        line = file1.readline()
        s = s+line
        # if line is empty
        # end of file is reached
        if not line:
            break
  
    file1.close()

    return s


# source venv/bin/activate
# export FLASK_APP=app.py
# flask run