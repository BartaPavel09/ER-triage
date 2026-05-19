from flask import Flask, jsonify, request, render_template

from BinomialNode import BinomialHeap
from RedBlackTree import RedBlackTree

app = Flask(__name__)

erWaitingRoom = BinomialHeap()
erDatabase = RedBlackTree()

# --- SERIALIZATION HELPERS ---


# Recursively walks through a Binomial Tree building a nested dictionary
def serializeBhNode(node):
    children = []
    curr = node.child
    while curr is not None:
        children.append(serializeBhNode(curr))
        curr = curr.sibling

    return {
        "name": node.patientName,
        "severity": node.key,
        "degree": node.degree,
        "children": children,
    }


# Grabs the root list of the Binomial Heap and serializes each tree
def serializeBinomialHeap(heap):
    roots = []
    curr = heap.head
    while curr is not None:
        roots.append(serializeBhNode(curr))
        curr = curr.sibling
    return roots


# Recursively walks the Red-Black Tree. Returns None when it hits the Sentinel Nil
def serializeRbtNode(tree, node):
    if tree.isNil(node):
        return None
    return {
        "name": node.patientName,
        "key": node.key,
        "color": node.col,
        "left": serializeRbtNode(tree, node.left),
        "right": serializeRbtNode(tree, node.right),
    }


# --- API ROUTES ---


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_patient', methods=['POST'])
def addPatient():
    data = request.get_json()
    name = data.get('name', 'Unknown')
    severity = int(data.get('severity', 5))

    # Add to the priority queue
    erWaitingRoom.insert(name, severity)
    # Add to the RB Tree
    erDatabase.insert(severity, name)

    return jsonify({"status": "success", "message": f"Patient {name} added."})


@app.route('/treat_patient', methods=['POST'])
def treatPatient():
    # Removes the minimum node from the Binomial Heap
    treatedPatient = erWaitingRoom.extractMin()

    if treatedPatient:
        return jsonify(
            {
                "status": "success",
                "message": f"Treated {treatedPatient.patientName} (Severity: {treatedPatient.key})",
            }
        )
    return jsonify({"status": "error", "message": "No patients in waiting room."})


@app.route('/reset', methods=['POST'])
def resetHospital():
    # Uses global so it can override the existing structures with new empty ones
    global erWaitingRoom, erDatabase
    erWaitingRoom = BinomialHeap()
    erDatabase = RedBlackTree()

    return jsonify({"status": "success", "message": "All records cleared!"})


@app.route('/get_state', methods=['GET'])
def getState():
    # Returns the full layout of both structures
    return jsonify(
        {
            "binomialHeap": serializeBinomialHeap(erWaitingRoom),
            "redBlackTree": serializeRbtNode(erDatabase, erDatabase.root),
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
