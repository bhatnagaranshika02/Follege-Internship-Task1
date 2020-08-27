from flask import Flask, jsonify, request,render_template
import sqlite3 as sql

con=sql.connect('user_database.db')
con.execute('CREATE TABLE IF NOT EXISTS User (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'username TEXT, password TEXT)')
con.execute('CREATE TABLE IF NOT EXISTS SavedPass (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'userId TEXT,website TEXT, password TEXT)')
con.close()

# creating a Flask app 
app = Flask(__name__) 

@app.route('/signuppage')
def signuppage():
	return render_template('signup.html')

@app.route('/loginpage')
def loginpage():
	return render_template('login.html')

@app.route('/savesite')
def savepage():
	return render_template('savesite.html')

@app.route('/app/user',methods=['POST'])
def signup():
	username=request.form['username']
	password=request.form['password']
	print(username,password)
	try:
		con = sql.connect('user_database.db')
		c =  con.cursor() # cursor
		print(username,password)
		query="INSERT INTO User (username,password) VALUES ('{0}','{1}')".format(username,password)
		print(query)
		c.execute(query)
		con.commit()
		return "account created"
	except con.Error as err: # if error
		return "account can't be created"
	finally:
		con.close() # close the connection

@app.route('/app/user/auth',methods=['POST'])
def login():
	username=request.form['username']
	password=request.form['password']
	try:
		con = sql.connect('user_database.db')
		c =  con.cursor() # cursor
		print("yaha aaya kya")
		query="Select * from User where username='{0}';".format(username)
		print(query)
		c.execute(query)
		print("yaha bhui aata kya")
		row=c.fetchone()
		print(row)
		if row==None:
			return "username not found"
		con.commit() # apply changes
		if row[1]==username and row[2]==password:
			return jsonify({'status':'success',"userId":row[0]})
	except con.Error as err: # if error
		return "account can't be created"
	finally:
		con.close() # close the connection

@app.route('/app/sites/:userId',methods=['POST'])
def saveWebsite():
	website=request.form['website']
	username=request.form['username']
	password=request.form['password']
	try:
		con = sql.connect('user_database.db')
		c =  con.cursor() # cursor
		print(username,password,website)
		query1="Select * from User where username='{0}'".format(username)
		print(query1)
		c.execute(query1)
		row=c.fetchone()
		if row!=None:
			print(row)
			query="INSERT INTO SavedPass (userId,website,password) VALUES ('{0}','{1}','{2}')".format(row[0],website,password)
			print(query)
			c.execute(query)
			con.commit()
			return jsonify({'status':'success'})	
		return "Error"
	except con.Error as err: # if error
		return "Error"
	finally:
		con.close() # close the connection

@app.route('/app/sites/list/<int:userId>',methods=['GET'])
def listSites(userId):
	#userId=request.args.get('')
	try:
		con = sql.connect('user_database.db')
		c =  con.cursor() # cursor
		print(userId)
		query1="Select * from SavedPass where userId='{0}'".format(userId)
		print(query1)
		c.execute(query1)
		row=c.fetchall()
		if row!=None:
			return jsonify(row)	
		return "Error"
	except con.Error as err: # if error
		return "Error"
	finally:
		con.close() # close the connection
 
if __name__ == '__main__': 
  
    app.run(debug = True) 