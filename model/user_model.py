import mysql.connector
from flask import Flask,render_template


class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host='localhost',user='root',password='',database='facebook')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('connection established!')
        except:
            print('error!')

    def test(self):
        self.cur.execute("SELECT * FROM user_data;")
        result = self.cur.fetchall()
        return result
    
    def signUpPage(self):
        return render_template('SignUpPage.html')
    
    def user_home_page(self):
        return render_template('LoginPage.html')
    
    def user_create_account(self,data):
        query = f"INSERT INTO user_data (mobile_no,first_name,last_name,password) values('{data['mobile_no']}','{data['first_name']}','{data['last_name']}','{data['password']}');"
        self.cur.execute(query)
        return render_template('LoginPage.html')
        