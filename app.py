from flask import Flask
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

def sendMail():
    # list of email_id to send the mail
    li = ["geniusadarsh4@gmail.com", "geniusadarsh3@gmail.com"]
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    
    # storing the senders email address  
    fromaddr = "sdashadm@gmail.com"
    msg['From'] = fromaddr
    
    # Iterating through list of recievers
    for toaddr in li:

        msg['To'] = toaddr
        
        # storing the subject 
        msg['Subject'] = "Checking storage status"
        
        # string to store the body of the mail
        username = "testuser1"
        body = "Reminder to check the storage status of the system for the user : " + username +"."
        body = body + "The current storage is exceeding the assigned storage allocated to user : " + username +"."
        
        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
        
        # open the file to be sent 
        filename = "Storage.pdf"
        attachment = open("./Storage.pdf", "rb")
        
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
        
        # To change the payload into encoded form
        p.set_payload((attachment).read())
        
        # encode into base64
        encoders.encode_base64(p)
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
        
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        
        # start TLS for security
        s.starttls()
        
        # Authentication
        s.login(fromaddr, "mvfkqncnorepjfjp")
        
        # Converts the Multipart msg into a string
        text = msg.as_string()
        
        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
        
        # terminating the session
        s.quit()

    


def downloadPDF():
    from fpdf import FPDF
    
    # save FPDF() class into a variable pdf
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font that you want in the pdf
    pdf.set_font("Arial", size = 15)

    # create a cell
    pdf.cell(200, 10, txt = "Testing pdf", ln = 1, align = 'C')
    
    
    file1 = open('filesize', 'r')
    s = ""
    linenumber=2
    while True:   
        # Get next line from file
        line = file1.readline()

        # add another cell
        pdf.cell(200, 10, txt = line, ln = linenumber, align = 'C')
        linenumber = linenumber + 1

        # if line is empty
        # end of file is reached
        if not line:
            break
    file1.close()
    
    # save the pdf with name .pdf
    pdf.output("Storage.pdf")

@app.route('/')
def hello_world():
    os.system("df -h > filesize")
    
  
    
    downloadPDF()
    sendMail()

    return "Hello"


# source venv/bin/activate
# export FLASK_APP=app.py
# flask run