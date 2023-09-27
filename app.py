from blockchain import Blockchain
from flask import Flask, jsonify


# Creating a Web App
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Mining a new block

blockchain = Blockchain()


@app.route("/mine_block", methods=['GET'])
def mine_block():
    # 이전 블록을 들고옴
    previous_block = blockchain.get_previous_block()
    # 이전 블록의 proof(nonce)를 들고 옴
    previous_proof = previous_block['proof']
    # 이전 블록의 proof(nonce)를 통해 새로운 proof를 구함
    proof = blockchain.proof_of_work(previous_proof)
    # 이전 블록의 해시를 구함
    previous_hash = blockchain.hash(previous_block)
    # 새로운 proof(nonce)와 이전 블록의 해시으로 새로운 블록을 만듦
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {
        'is_valid': is_valid
    }
    return jsonify(response), 200


app.run('0.0.0.0', 5500)
