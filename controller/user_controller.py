from flask import Flask,request
from app import app
from model.user_model import user_model

obj = user_model()
@app.route('/')
def home_page():
    return obj.user_home_page()

@app.route('/signUpPage')
def signUpPage():
    return obj.signUpPage()

@app.route('/create_account',methods=['GET','POST'])
def user_create_account():
    if request.method == 'POST':
       return obj.user_create_account(request.form)

@app.route('/test')
def test():
    return obj.test()
