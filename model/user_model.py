import mysql.connector
from flask import Flask,render_template,session,redirect


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
        errors = []
        form_mobile = data['mobile_no']
        form_password = data['password']
        if not form_mobile:
            errors.append("Enter Mobile no!")
        if not form_password:
            errors.append("Enter Password!")
        if errors:
            return render_template('LoginPage.html',errors=errors)
        self.cur.execute(f"SELECT * FROM user_data where mobile_no = '{form_mobile}';")
        result = self.cur.fetchall()
        user_password = result[0]['password']
        user_dp = result[0]['dp_url']
        print(user_dp)
        print(user_password)
        if form_password == user_password:
            session["mobile_no"] = form_mobile
            session["user_dp"] =  user_dp 
            dp =  user_dp 
            self.cur.execute(f"select followee from followers where follower = {form_mobile} ;")
            followees = self.cur.fetchall()
            if len(followees) == 0:
                return render_template('HomePage.html',followees=followees,dp=dp)
            else:
                include = ""
                for followee in followees:
                    include = include + "'" + str(followee['followee']) + "',"
                peoples = include[:len(include)-1]
                print(peoples)
                self.cur.execute(f"SELECT * FROM user_post where mobile_no  in ({peoples},'{session.get('mobile_no')}');")
                print(f"SELECT * FROM user_post where mobile_no  in ({peoples},'{session.get('mobile_no')}');")
                posts = self.cur.fetchall()
                return render_template('HomePage.html',posts=posts,dp=dp,followees=followees)
        else:
            errors.append("Password mismatch!")
            return render_template('LoginPage.html',errors=errors)

    def dash_board(self):
        self.cur.execute(f"SELECT * FROM user_data where mobile_no = {session.get('mobile_no')};")
        result = self.cur.fetchall()
        dp = result[0]['dp_url']
        self.cur.execute(f"select followee from followers where follower = {session.get('mobile_no')} ;")
        followees = self.cur.fetchall()
        if len(followees) == 0:
            return render_template('HomePage.html',followees=followees,dp=dp)
        else:
            include = ""
            for followee in followees:
                include = include + "'" + str(followee['followee']) + "',"
            peoples = include[:len(include)-1]
            print(peoples)
            self.cur.execute(f"SELECT * FROM user_post where mobile_no  in ({peoples},'{session.get('mobile_no')}');")
            print(f"SELECT * FROM user_post where mobile_no  in ({peoples},'{session.get('mobile_no')}');")
            posts = self.cur.fetchall()
            return render_template('HomePage.html',posts=posts,dp=dp,followees=followees)
    
    def peoples_page(self):
        self.cur.execute(f"select followee from followers where follower = '{session.get('mobile_no')}' ;")
        user_info = self.cur.fetchall()
        if len(user_info) == 0:
            self.cur.execute(f"select mobile_no,dp_url,first_name,last_name from user_data where mobile_no  not  in ({session.get('mobile_no')});")
            users_data = self.cur.fetchall()
            return render_template('FriendsPage.html',users_data=users_data)
        else:
            not_include = ""
            for user in user_info:
               not_include = not_include + "'" + str(user['followee']) + "',"
            peoples = not_include[:len(not_include)-1]
            print(peoples)
            self.cur.execute(f"select mobile_no,dp_url,first_name,last_name from user_data where mobile_no not in ({peoples},{session.get('mobile_no')}) ;")
            users_data = self.cur.fetchall()
            return render_template('FriendsPage.html',users_data=users_data)
      

    def signUpPage(self):
        return render_template('SignUpPage.html')
    
    def user_home_page(self):
        return render_template('LoginPage.html')
    
    def user_create_account(self,data):
        errors = []
        if not data['first_name']:
            errors.append("Enter First Name!")
        if not data['last_name']:
            errors.append("Enter Last Name!")
        if not data['mobile_no']:
            errors.append("Enter mobile no!")
        if not data['password']:
            errors.append('Set Password!')
        if not data['confirm_password']:
            errors.append("Please confirm Password!")
        elif data['password'] != data['confirm_password']:
            errors.append("Type Password correctly!")
        if errors:
            return render_template('SignUpPage.html',errors=errors)
        else:
            query = f"INSERT INTO user_data (mobile_no,first_name,last_name,password,dp_url) values('{data['mobile_no']}','{data['first_name']}','{data['last_name']}','{data['password']}','blank');"
            self.cur.execute(query)
            return render_template('DpPage.html')
        
    def new_post(self,file_name):
        self.cur.execute(f"SELECT first_name,last_name,mobile_no from user_data where mobile_no = '{session.get('mobile_no')} ';")
        user_info = self.cur.fetchall()
        first_name = user_info[0]['first_name']
        last_name = user_info[0]['last_name']
        mobile = user_info[0]['mobile_no']
        dp = session.get('user_dp')
        query = f"INSERT INTO user_post (dp_url,first_name,last_name,post_url,mobile_no) values('{dp}','{first_name}','{last_name}','{file_name}','{mobile}');"
        self.cur.execute(query)
        self.cur.execute(f"SELECT * FROM user_post order by si_no asc;")
        posts = self.cur.fetchall()
        return redirect('/home_page')

    def upload_dp(self,file_location):
        self.cur.execute(f"UPDATE user_data set dp_url = '{file_location}' where dp_url = 'blank' ;")
        return render_template('LoginPage.html')
    
    def follow_people(self,mobile_no):
        self.cur.execute(f"insert into followers (follower,followee) values({session.get('mobile_no')},'{mobile_no}');")
        self.cur.execute(f"select followee from followers where follower = {session.get('mobile_no')} ;")
        user_info = self.cur.fetchall()
        if len(user_info) == 0:
            self.cur.execute(f"select mobile_no,dp_url,first_name,last_name from user_data where mobile_no  not in ({session.get('mobile_no')});")
            users_data = self.cur.fetchall()
            return render_template('FriendsPage.html',users_data=users_data)
        else:
            not_include = ""
            for user in user_info:
               not_include = not_include + "'" + str(user['followee']) + "',"
            peoples = not_include[:len(not_include)-1]
            print(peoples)
            self.cur.execute(f"select mobile_no,dp_url,first_name,last_name from user_data where mobile_no not in ({peoples},{session.get('mobile_no')}) ;")
            users_data = self.cur.fetchall()
            print(users_data)
            return render_template('FriendsPage.html',users_data=users_data)
        

    def messages(self,id):
        visiblity = True
        if id == '202':
            visiblity = False
            self.cur.execute("select * from user_data;")
            user_info = self.cur.fetchall()
            recciver_info = None
            return render_template('Message.html',visiblity=visiblity,user_info=user_info,recciver_info=recciver_info)

        else:
            self.cur.execute("select * from user_data;")
            user_info = self.cur.fetchall()
            self.cur.execute(f"select * from user_data where mobile_no = '{id}';")
            recciver_info = self.cur.fetchall()
            print(recciver_info)
            recciver_mobile = recciver_info[0]['mobile_no']
            dp_image = recciver_info[0]['dp_url']
            full_name = recciver_info[0]['first_name'] + " " + recciver_info[0]['last_name']
            self.cur.execute(f"select * from messages where ( sender= {session.get('mobile_no')} && recciver = '{id}') || ( sender= '{id}' && recciver = {session.get('mobile_no')});")
            all_messages = self.cur.fetchall()
            return render_template('Message.html',visiblity=visiblity,user_info=user_info,dp_image=dp_image,full_name=full_name,all_messages=all_messages,recciver_mobile=recciver_mobile)

    def send_msg(self,data,mobile):
        msg = data['msg']
        visiblity=True
        self.cur.execute(f"insert into messages (sender,recciver,message) values({session.get('mobile_no')},'{mobile}','{msg}');")
        print(f"insert into messages (sender,recciver,message) values({session.get('mobile_no')},'{mobile}','{msg}');")
        self.cur.execute("select * from user_data;")
        user_info = self.cur.fetchall()
        self.cur.execute(f"select * from user_data where mobile_no = '{mobile}';")
        recciver_info = self.cur.fetchall()
        print(recciver_info)
        recciver_mobile = recciver_info[0]['mobile_no']
        dp_image = recciver_info[0]['dp_url']
        full_name = recciver_info[0]['first_name'] + " " + recciver_info[0]['last_name']
        self.cur.execute(f"select * from messages where ( sender= {session.get('mobile_no')} && recciver = '{mobile}') || ( sender= '{mobile}' && recciver = {session.get('mobile_no')});")
        all_messages = self.cur.fetchall()
        return render_template('Message.html',visiblity=visiblity,user_info=user_info,dp_image=dp_image,full_name=full_name,all_messages=all_messages,recciver_mobile=recciver_mobile)


        
