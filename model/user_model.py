import mysql.connector
from flask import Flask,render_template,session


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
    

    def log_out(self):
        session["mobile_no"] = None
        return render_template('LoginPage.html')

    def user_auth(self,data):
        form_mobile = data['mobile_no']
        form_password = data['password']
        self.cur.execute(f"SELECT * FROM user_data where mobile_no = '{form_mobile}';")
        result = self.cur.fetchall()
        user_password = result[0]['password']
        user_dp = result[0]['dp_url']
        print(user_password)
        if form_password == user_password:
            session["mobile_no"] = form_mobile
            session["user_dp"] = user_dp
            self.cur.execute(f"SELECT * FROM user_post;")
            posts = self.cur.fetchall()
            return render_template('HomePage.html',posts=posts)
        else:
            return "Sorry!"

    
    def signUpPage(self):
        return render_template('SignUpPage.html')
    
    def user_home_page(self):
        return render_template('LoginPage.html')
    
    def user_create_account(self,data):
        query = f"INSERT INTO user_data (mobile_no,first_name,last_name,password,dp_url) values('{data['mobile_no']}','{data['first_name']}','{data['last_name']}','{data['password']}','blank');"
        self.cur.execute(query)
        return render_template('DpPage.html')
        
    def new_post(self,file_name):
        self.cur.execute(f"SELECT first_name,last_name from user_data where mobile_no = '{session.get('mobile_no')} ';")
        user_info = self.cur.fetchall()
        first_name = user_info[0]['first_name']
        last_name = user_info[0]['last_name']
        dp = session.get('user_dp')
        query = f"INSERT INTO user_post (dp_url,first_name,last_name,post_url) values('{dp}','{first_name}','{last_name}','{file_name}');"
        self.cur.execute(query)
        self.cur.execute(f"SELECT * FROM user_post;")
        posts = self.cur.fetchall()
        return render_template('HomePage.html',posts=posts)

    def upload_dp(self,file_location):
        self.cur.execute(f"UPDATE user_data set dp_url = '{file_location}' where dp_url = 'blank' ;")
        return render_template('LoginPage.html')