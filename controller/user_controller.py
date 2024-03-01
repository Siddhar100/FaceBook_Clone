from flask import Flask,request
from app import app
import time
from model.user_model import user_model

obj = user_model()
@app.route('/')
def home_page():
    return obj.user_home_page()

@app.route('/home_page')
def dash_board():
    return obj.dash_board()

@app.route('/Peoples_page')
def peoples_page():
    return obj.peoples_page()

@app.route('/user_auth',methods=['GET','POST'])
def user_auth():
    if request.method == 'POST':
       return obj.user_auth(request.form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    if request.method == 'POST':
        return obj.log_out()

@app.route('/signUpPage')
def signUpPage():
    return obj.signUpPage()

@app.route('/create_account',methods=['GET','POST'])
def user_create_account():
    if request.method == 'POST':
       return obj.user_create_account(request.form)

@app.route('/upload_dp',methods=['GET','POST'])
def upload_dp():
    if request.method == 'POST':
       file = request.files['dp-input']
       tm = str(time.time())
       tm_decimal = tm.split('.')[0]
       file_name = f"{tm_decimal}_{file.filename}"
       file_location = f"static/{file_name}"
       file.save(file_location)
       print(f"file_location: {file_name}")
       return obj.upload_dp(file_name)


@app.route('/new_post',methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        file = request.files['file-input']
        file_name = f"static/{file.filename}"
        file.save(file_name)
        return obj.new_post(file.filename)


@app.get('/follow_people/<mobile_no>')
def follow_people(mobile_no):
       return obj.follow_people(mobile_no)

@app.route('/Messages/<id>')
def messages(id):
    return obj.messages(id)

@app.route('/new_msg/<mobile>',methods=['GET','POST'])
def send_msg(mobile):
    if request.method == 'POST':
        return obj.send_msg(request.form,mobile)

@app.route('/test')
def test():
    return obj.test()
