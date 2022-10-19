import datetime # as we know all block has a timestamp so we should to know timestamp of block to do check proof.
import hashlib  # this lib for creating sha256 encryption
import json     # its for change type to json data type because we will send a request to htpp (GET) 
from flask import Flask, jsonify # Its for creating a web app (API)

class blockChain:  # creating a class
    def __init__(self): # creating a init method to build chain and first(genesis block) block.
        self.chain = []  # empty python list for blocks
        self.create_block(proof=1, previous_hash = '0') # we created genesis block with proof and previous hash arguments. proof is will be random number, previous hash should be 0 because it doesnt have previous hash.
   
    def create_block(self, proof, previous_hash): # this method for create block with proof and previous hash.
        block = { # data will be dictionary format because we will work with json.
                 'index':len(self.chain)+1,  # index should be one more than length of chain
                 'timestamp':str(datetime.datetime.now()),# timestamp is creating date of block. It have to be string because we are working with json.
                 'proof':proof, # It is the result of the actions taken to prove the correctness of the block. true or false
                 'previous_hash':previous_hash # is the hash value of the block before the newly created block.
                }
        self.chain.append(block) # we can add new block to chain list.
        return block
    
    def get_previous_block(self): # we are getting previous block to do check proof.
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof): # we should create a conditions to do proof.
        new_proof = 1 # Its like number of attempts
        check_proof = False # Its for while loop
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # this code we created a hash number in accordance with sha256 rules.
            # We can set the operations (proof or difficulty of the hash) ourselves. we did encode and hexdigest method To create the hash value in hexadecimal format
            if hash_operation[:4] == '0000': # The more 0s there is at the beginning of the hash code, the lower the probability of decryption. As an example, we added 4 zeros.
                check_proof = True
            else:
                new_proof+=1
        return new_proof
            
    def hash(self, block):  # created hash method to return encoded hash numbers.
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
            
    def is_chain_valid(self,chain): # This method doing validation to chain.
        previous_block = chain[0]  # We defined the first block as the previous block because we will be checking the entire chain.
        block_index = 1  # block index have to start 1
        while block_index < len(chain):  # a while loop to check the blocks in the whole chain.
            block = chain[block_index]  
            if block['previous_hash'] != self.hash(previous_block): # The method returns false if the "previous hash number" of the block we are checking is different from the hash number of the previous block.
                return False
            
            # Another verification method is proof numbers. If the proof numbers do not match the proof number in the previous block, the valid operation returns false.
            previous_proof = previous_block['proof'] 
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block # To move forward in the while loop, we assign the block we have to the "previous block" value at the end of each operation.
            block_index += 1
        return True  
app = Flask(__name__) # we crated web app with Flask API.
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False # It blocked to 500 Internal Server Error.
blockchain = blockChain() # created a object from blockChain class.

@app.route('/is_chain_valid',methods=['GET']) # Using route decator, we create a URL and send a request to our API application through our own server.
def is_valid(): # sends a message if validation is successful. If not successful, it sends a negative message.
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            'message' : 'All Good. Blockchain is valid.'
            }
    else:
        response = {
            'message' : 'Houston, We have a problem. The blockchain is not valid.'
            }
    return jsonify(response),200 # jsonify is a method that allows us to return JSON data. From the Flask library

@app.route('/mine_block',methods=['GET'])
def mine_block(): # A method that adds new blocks to the chain by performing proof operations and sends them as JSON to the web app.
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response  = {
            'message':'Conguratulations, you just mined a block!',
            'index' : block['index'],
            'timestamp': block['timestamp'],
            'proof' : block['proof'],
            'previous_hash' : block['previous_hash']
                }
    return jsonify(response), 200

@app.route('/get_chain',methods=['GET'])
def get_chain(): # A method that sends the entire blockchain as JSON to the web app.
    response = {
        'chain':blockchain.chain,
        'length': len(blockchain.chain)
                }
    return jsonify(response), 200

# Running the app
app.run(host= '0.0.0.0',port=5000) # We used the run() method to run the web app we created. From the Flask library.
# host = '0.0.0.0' means, every people can access our blockchain. host value should be string
# port = 5000 its depends on API. but this value should be integer.