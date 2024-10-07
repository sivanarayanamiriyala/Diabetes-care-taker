from flask import *
import mysql.connector
import os
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import matplotlib


matplotlib.use('Agg')

app=Flask(__name__)
app.secret_key = "sivanarayana"  

mydb = mysql.connector.connect(host="localhost",user="root",password="123456",database="Diabeties")	



@app.route('/',methods=['GET','POST'])
def index():
	return render_template('/index.html')

@app.route('/visual',methods=['GET','POST'])
def visual():
	return render_template('/visual.html')

@app.route('/Register',methods=['GET','POST'])
def register():
	return render_template('/register.html')

@app.route('/loginsuccessful',methods=['GET','POST'])
def loginsuccessful():
	return render_template('/login.html')

@app.route('/store',methods=['GET','POST'])
def store():
	if request.method=='POST':
		fullname=request.form.get('fullname')
		email=request.form.get('email')
		number=request.form.get('number')
		dob=request.form.get('dob')
		username=request.form.get('username')
		password=request.form.get('password')
		question1=request.form.get('question1')
		question2=request.form.get('question2')
		question3=request.form.get('question3')
		answer1=request.form.get('answer1')
		answer2=request.form.get('answer2')
		answer3=request.form.get('answer3')
		try:
			mycursor = mydb.cursor()
			sql = "INSERT INTO register (fullname,email,number,dob,username,password,question1,answer1,question2,answer2,question3,answer3) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = (fullname,email,number,dob,username,password,question1,answer1,question2,answer2,question3,answer3)
			mycursor.execute(sql, val)
			mydb.commit()
			flash("Registration Successful");
			return redirect(url_for('index'))

		except mysql.connector.IntegrityError:
			flash("UserName Already Exists.Try a Different UserName");
			return redirect(url_for('register'))
			


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		username=request.form.get('username')
		password=request.form.get('password')
		mycursor = mydb.cursor()
		mycursor.execute("SELECT username,password,fullname FROM register")
		myresult = mycursor.fetchall()	
		for result in myresult:
			if result[0]==username and result[1]==password:
				session['username']=result[0]
				session['name']=result[2]
#				return render_template('/login.html',name=result[2])
				return redirect(url_for('loginsuccessful'))

		else:
			return redirect(url_for('index'))


@app.route('/diabeties',methods=['GET','POST'])
def diabeties():
	if request.method=='POST':
		username=session['username']
		FBS=request.form.get('FBS')
		meal=request.form.get('meal')
		fbstime=request.form.get('fbstime')
		breakfast=request.form.get('breakfast')
		bfweight=request.form.get('bfweight')
		bftime=request.form.get('bftime')
		lunch=request.form.get('lunch')
		lweight=request.form.get('lweight')
		ltime=request.form.get('ltime')
		dinner=request.form.get('dinner')
		dweight=request.form.get('dweight')
		dtime=request.form.get('dtime')
		pp=request.form.get('pp')
		pptime=request.form.get('pptime')
		today=date.today()
		mycursor = mydb.cursor()
		if meal=='Breakfast':
			sql = "INSERT INTO breakfasttable(username,RecordedDate,FBS,fbstime,breakfast,bfweight,bftime,PP,pptime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = (username,today,FBS,fbstime,breakfast,bfweight,bftime,pp,pptime)
			mycursor.execute(sql, val)
			mydb.commit()
			return  Response(status=204)
		elif meal=='Lunch':
			sql = "INSERT INTO lunchtable(username,RecordedDate,FBS,fbstime,lunch,lweight,ltime,PP,pptime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = (username,today,FBS,fbstime,lunch,lweight,ltime,pp,pptime)
			mycursor.execute(sql, val)
			mydb.commit()
			return  Response(status=204)
		elif meal=='Dinner':
			sql = "INSERT INTO dinnertable(username,RecordedDate,FBS,fbstime,dinner,dweight,dtime,PP,pptime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = (username,today,FBS,fbstime,dinner,dweight,dtime,pp,pptime)
			mycursor.execute(sql, val)
			mydb.commit()
			return  Response(status=204)
	
		
	
@app.route('/Reports',methods=['GET','POST'])
def Reports():
	if request.method=='GET':
		username=session['username']
		mycursor1 = mydb.cursor(buffered=True)
		mycursor2 = mydb.cursor(buffered=True)
		mycursor3= mydb.cursor(buffered=True)
		mycursor1.execute("SELECT * FROM breakfasttable where username=%s",(username,))
		mycursor2.execute("SELECT * FROM lunchtable where username=%s",(username,))
		mycursor3.execute("SELECT * FROM dinnertable where username=%s",(username,))
		data1= mycursor1.fetchall()
		data2= mycursor2.fetchall()
		data3= mycursor3.fetchall()		
	
	return render_template('/reports.html',data1=data1,data2=data2,data3=data3)


@app.route('/Analysis',methods=['GET','POST'])
def Analysis():
	if request.method=='POST':	
		X=[]
		Y=[]
	
		username=session['username']
		meal=request.form.get("meal")
		breakfast=request.form.get("breakfast")
		lunch=request.form.get("lunch")
		dinner=request.form.get("dinner")
		if meal=="Breakfast":
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("SELECT PP,bfweight FROM breakfasttable where username=%s and breakfast=%s order by bfweight,PP",(username,breakfast))
			data= mycursor.fetchall()
			for i in data:
				X.append(i[0])
				Y.append(i[1])
			plt.plot(Y,X)
			plt.xlabel("BreakFast Food Items Names")
			plt.ylabel("Sugar Levels")
			plt.title("Sugar Level's Tracking")
			plt.savefig(os.path.join('static', 'photo', 'chart.png'))
			return redirect(url_for('visual'))

		elif meal=="Lunch":
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("SELECT PP,lweight FROM lunchtable where username=%s and lunch=%s order by lweight,PP ",(username,lunch))
			data= mycursor.fetchall()
			for i in data:
				X.append(i[0])
				Y.append(i[1])
			plt.plot(Y,X)
			plt.xlabel("Lunch Food Items Names")
			plt.ylabel("Sugar Levels")
			plt.title("Sugar level's Tracking")
			plt.savefig(os.path.join('static', 'photo', 'chart.png'))
			return redirect(url_for('visual'))
		if meal=="Dinner":
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("SELECT PP,dweight FROM dinnertable where username=%s and dinner=%s order by dweight,PP",(username,dinner))
			data= mycursor.fetchall()
			for i in data:
				X.append(i[0])
				Y.append(i[1])
			plt.plot(Y,sorted(X))
			plt.xlabel("Dinner Food Items Names")
			plt.ylabel("Sugar Levels")
			plt.title("Sugar level's Tracking")
			plt.savefig(os.path.join('static', 'photo', 'chart.png'))
			return redirect(url_for('visual'))

	return  Response(status=204)

	
@app.route('/verify',methods=['GET','POST'])
def verify():
	return render_template('/verify.html')


@app.route('/Questions',methods=['GET','POST'])
def Questions():
	email=request.form.get('email')
	try:
		mycursor = mydb.cursor()
		mycursor.execute("SELECT  question1,question2,question3 FROM register where email=%s",(email,))
		myresult = mycursor.fetchall()
		session['question1']=myresult[0][0]
		session['question2']=myresult[0][1]
		session['question3']=myresult[0][2]	
		if(len(myresult)<1):
			return redirect(url_for('verify'))
		else:
			session['verificationemail']=email
			return redirect(url_for('question'))
	except IndexError:
		flash("Enter valid Email!!")
		return redirect(url_for('verify'))             


@app.route('/question',methods=['GET','POST'])
def question():
	return render_template('/Questions.html')


 

@app.route('/check',methods=['GET','POST'])
def check():
	if request.method=='POST':
		username=request.form.get('username')
		answer1=request.form.get('answer1')
		answer2=request.form.get('answer2')
		answer3=request.form.get('answer3')
		email=session['verificationemail']
		try:
			mycursor = mydb.cursor()
			mycursor.execute("SELECT username,answer1,answer2,answer3 FROM register where email=%s",(email,))
			myresult = mycursor.fetchall()			
			if myresult[0][0]==username and myresult[0][1]==answer1 and myresult[0][2]==answer2 and myresult[0][3]==answer3:	
				return render_template('/change.html')
			else:
				flash("Invalid Answers!!")
				return redirect(url_for('question'))
		except IndexError:
			flash("Invalid Answers!!")
			return redirect(url_for('question'))
	

@app.route('/updatepswd',methods=['GET','POST'])
def updatepswd():
	if request.method=='POST':
		password=request.form.get('password')
		email=session['verificationemail']
		mycursor = mydb.cursor()
		mycursor.execute("update register set password=%s where email=%s",(password,email,))	
		mydb.commit()
		return redirect(url_for('index'))


@app.route('/info',methods=['GET','POST'])
def info():
	return render_template('/info.html')
		

@app.route('/logout',methods=['GET','POST'])
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/Views',methods=['GET','POST'])
def views():
	return render_template('/views.html')		




if __name__=="__main__":
	app.run(debug=True)
