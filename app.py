from flask import Flask, jsonify, request

app = Flask(__name__)

# er_waiting_room = BinomialHeap()
# er_database = RedBlackTree()

@app.route('/')
def home():
    return "Emergency Room Triage Simulator is Running!"

@app.route('/api/state', methods=['GET'])
def get_state():
    # Later, this will return the JSON representation of Heap and Tree
    return jsonify({
        "status": "success",
        "message": "Data structures will go here."
    })

if __name__ == '__main__':
    app.run(debug=True)