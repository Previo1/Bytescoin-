from flask import Flask, request, jsonify
import time, hashlib, json

app = Flask(__name__)

# --- Blockchain Data ---
blockchain = []
mempool = []

def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def create_genesis_block():
    genesis = {
        "index": 0,
        "timestamp": time.time(),
        "transactions": [],
        "previous_hash": "0",
        "nonce": 0
    }
    genesis["hash"] = calculate_hash(genesis)
    return genesis

if not blockchain:
    blockchain.append(create_genesis_block())


# --- Routes ---

@app.route("/")
def home():
    return "🚀 Bytecoin Public Blockchain (Vercel Hosted)"


@app.route("/get_work")
def get_work():
    """ Miner gets the work """
    last_block = blockchain[-1]
    return jsonify({
        "index": len(blockchain),
        "previous_hash": last_block["hash"],
        "transactions": mempool,
        "difficulty": 4,
        "timestamp": time.time()
    })


@app.route("/submit_block", methods=["POST"])
def submit_block():
    """ Miner submits mined block """
    block = request.json
    blockchain.append(block)
    return jsonify({"status": "✅ Block accepted", "height": len(blockchain)})


@app.route("/chain")
def chain():
    """ Full blockchain explorer """
    return jsonify(blockchain)
  
