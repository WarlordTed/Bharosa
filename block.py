import pickle


state = {u'Alice':0, u'Bob':0}  # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}``
genesisHash = hashMe( genesisBlockContents )
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)



def update_network(chain):
    for i in iplist:
        open_ip = open(ip+".pickel","wb")
        pickle.dump(chain,open_ip)

def check_v_index(chain):
    for i in iplist:
        temp_chain = pickle.load(open(i+".pickle","rb"))
        if(temp_chain==chain):
            v=v+1
    return v/len(iplist)


chain = [genesisBlock]

if(ip in iplist):
    break  
else:
    dump_chain = pickle.load('local.pickle')
    open_ip = open(ip+".pickle","wd")
    pickle.dump(open_ip,dump_chain)
    pickling.close()
    txn = {ip:-1,party:1}
        chain = pickle.load(ip+".pickle","rb")
        for i in iplist:
            temp_chain = pickle.load(i)
            if(temp_chain==chain):
                v_no=v_no+1
        v_index = v_no/len(iplist)
        if(v_index>=0.5):
            block = makeBlock(txn,chain)
            if(checkBlockValidity(block,chain[-1],state)):
                chain.append(block)
                checkChain(chain)
                update_network(chain)
    

