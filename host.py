
from flask import Flask, render_template, Response, request, redirect, url_for
import pickle
from start import *

iplist=[]
state = {u'p_1':0, u'p_2':0,u'p_3':0}  # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
genesisHash = hashMe( genesisBlockContents)
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
#genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
chain = [genesisBlock]

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
	return render_template('index.html')

@app.route('/done/')
def done():
	return render_template('done.html')


def check_v_index(chain):
    v=0
    for i in range(1,5):
        temp_chain = pickle.load(open("mine"+str(i)+".pickle","rb"))
        if(temp_chain==chain):
            v=v+1
    return v/len(iplist)


pickle.dump(chain, open('mine1.pickle',"wb"))
pickle.dump(chain, open('mine2.pickle',"wb"))
pickle.dump(chain, open('mine3.pickle',"wb"))
pickle.dump(chain, open('mine4.pickle',"wb"))
	
@app.route('/vote/',methods=["GET","POST"])
def vote():
	if request.method=="POST":
		
		result=(request.form['party'])
		ip=(request.remote_addr)
		print(result,ip)

		global iplist,state
		if(ip not in iplist):
			iplist.append(ip)
			state[ip]=1 
	
		txn = {ip:-1,result:1}
		if(isValidTxn(txn,state)):
			print("Success")
			print("Chain",chain)
			print("State",state)
			state=updateState(txn,state)
			block = makeBlock(txn,chain)
			v=check_v_index(chain)
			if(v>=0.5):
				pickle.dump(chain, open('mine1.pickle',"wb"))
				pickle.dump(chain, open('mine2.pickle',"wb"))
				pickle.dump(chain, open('mine3.pickle',"wb"))
				pickle.dump(chain, open('mine4.pickle',"wb"))
				chain.append(block)	
				#checkChain(chain)

			else:
				return redirect(url_for('done'))
			return redirect(url_for('done'))
		else:
			print("Fail")
			return redirect('done')
	return render_template('vote.html')
	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8000)
