from flask import Flask,request
from app import app
from model.user_model import user_model

obj = user_model()
@app.route('/')
def home_page():
    return obj.user_home_page()

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

@app.route('/new_post',methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        file = request.files['file-input']
        file_name = f"static/{file.filename}"
        file.save(file_name)
        return obj.new_post(file_name)





@app.route('/test')
def test():
    return obj.test()
