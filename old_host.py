from flask import Flask, render_template, Response, request, redirect, url_for, flash, logging, session
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import pickle
from start import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'notforyou'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

iplist=[]
# userlist=[]
state = {u'p_1':0,u'p_2':0,u'p_3':0}  # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
genesisHash = hashMe( genesisBlockContents)
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
#genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
chain = [genesisBlock]

@app.route('/',methods=["GET","POST"])
def index():
	return render_template('index.html')

class RegisterForm(Form):
	name = StringField('Name',[validators.length(min=3,max=50),validators.DataRequired()],render_kw={"placeholder":"Kalyani Asthana"})
	username = StringField('Username',[validators.length(min=4,max=25),validators.DataRequired()],render_kw={"placeholder":"bcb0082"})
	email = StringField('Email',[validators.length(min=6,max=50),validators.DataRequired()],render_kw={"placeholder":"jb@xyz.com"})
	aadharid = StringField('AadharID',[validators.length(min=10,max=15),validators.DataRequired()],render_kw={"placeholder":"Aadhar ID Card No."})
	vid = StringField('VoterID',[validators.length(min=10,max=15),validators.DataRequired()],render_kw={"placeholder":"Voter ID Card No."})
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message="Passwords do not match")
	])
	confirm = PasswordField('Confirm Password')

@app.route('/signup/',methods=["GET","POST"])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		username = form.username.data
		email = form.email.data
		aadharid = form.aadharid.data
		vid = form.vid.data
		password = sha256_crypt.encrypt(str(form.password.data))

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, username, email, aadharid, voterid, password) VALUES(%s,%s,%s,%s,%s,%s)",
			(name, username, email, aadharid, vid, password))
		
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('login'))
	return render_template('signup.html',form=form)

@app.route('/login/',methods=["GET","POST"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']

		cur = mysql.connection.cursor()
		
		query_result = cur.execute("SELECT username, password FROM users WHERE username = %s", 
			[username])

		if query_result > 0:
			data = cur.fetchone()
			password = data['password']
			if sha256_crypt.verify(password_candidate,password):
				app.logger.info("PASSWORD MATCHED")
				session['logged_in'] = True
				session['username'] = username
				userdata = data['username']
				return redirect(url_for('vote'))
			else:
				app.logger.info("PASSWORD NOT MATCHED")
				error = 'Invalid User'
				return render_template('login.html')
		else:
			app.logger.info("NO USER FOUND")
			error = 'Invalid User'
			return render_template('login.html')
		cur.close()

	return render_template('login.html')

@app.route('/done/')
def done():
	return render_template('done.html')

@app.route('/not_done/')
def not_done():
	return render_template('not_done.html')

def check_v_index(chain):
    v=1
    t = json.dumps(genesisBlock, sort_keys=True)
    
    for i in range(1,5):
        temp_chain = pickle.load(open("mine"+str(i)+".pickle","rb"))
		
    t1 = json.dumps(genesisBlock, sort_keys=True) 
	#print("t",t,"t1",t1)   
    if(t==t1):
        v=v+1
 	        
    return float(v/4)

def define_v_index(chain):
    for i in range(1,5):
        pickle.dump(chain, open('mine'+str(i)+'.pickle',"wb"))

ip=0
@app.route('/vote/',methods=["GET","POST"])
def vote():
   
	if request.method=="POST":
		global ip		
		result=(request.form['party'])	
		ip=(request.remote_addr)
		#print(result,ip)
		#ip=ip+1
		global iplist,state
		if(ip not in iplist):
			iplist.append(ip)
			state[ip]=1 
	
		txn = {ip:-1,result:1}
		if(isValidTxn(txn,state)):
			
			print("Success")
			
			state=updateState(txn,state)
			block = makeBlock(txn,chain)
			k=check_v_index(chain)
			print("***v****",k)
			if(k>=0.5):
				chain.append(block)
				define_v_index(chain)
				#chain.append(block)	
				#checkChain(chain)
				print("State",state)
				session.clear()
				return redirect(url_for('done'))
			else:
				print("Fail")
				session.clear()
				return redirect(url_for('not_done'))
		else:
			print("Fail")
			return redirect(url_for('not_done'))
	return render_template('vote.html')
	

if __name__ == '__main__':
	app.secret_key = 'bcbhomies'
	app.run(host='0.0.0.0', debug=True, threaded=True, port=8100)
