from flask import Flask, jsonify, request, render_template
from binomial_heap import BinomialHeap
from red_black_tree import RedBlackTree

app = Flask(__name__)

er_waiting_room = BinomialHeap()
er_database = RedBlackTree()

# --- SERIALIZATION HELPERS ---

# Recursively walks through a Binomial Tree building a nested dictionary
def serialize_bh_node(node):
    children = []
    curr_child = node.child
    while curr_child is not None:
        children.append(serialize_bh_node(curr_child))
        curr_child = curr_child.sibling
    
    return {
        "name": node.patient_name,
        "severity": node.key,
        "degree": node.degree,
        "children": children
    }

# Grabs the root list of the Binomial Heap and serializes each tree
def serialize_binomial_heap(heap):
    roots = []
    curr = heap.head
    while curr is not None:
        roots.append(serialize_bh_node(curr))
        curr = curr.sibling
    return roots

# Recursively walks the Red-Black Tree. Returns None when it hits the Sentinel Nil
def serialize_rbt_node(tree, node):
    if tree.is_nil(node):
        return None
    return {
        "name": node.patient_name,
        "key": node.key,
        "color": node.col,
        "left": serialize_rbt_node(tree, node.left),
        "right": serialize_rbt_node(tree, node.right)
    }


# --- API ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.get_json()
    name = data.get('name', 'Unknown')
    severity = int(data.get('severity', 5))

    # Add to the priority queue
    er_waiting_room.insert(name, severity)
    # Add to the RB Tree
    er_database.insert(severity, name)

    return jsonify({"status": "success", "message": f"Patient {name} added."})

@app.route('/treat_patient', methods=['POST'])
def treat_patient():
    # Removes the minimum node from the Binomial Heap
    treated_patient = er_waiting_room.extract_min()
    
    if treated_patient:
        return jsonify({
            "status": "success", 
            "message": f"Treated {treated_patient.patient_name} (Severity: {treated_patient.key})"
        })
    else:
        return jsonify({"status": "error", "message": "No patients in waiting room."})

@app.route('/reset', methods=['POST'])
def reset_hospital():
    # Uses global so it can override the existing structures with new empty ones
    global er_waiting_room, er_database
    er_waiting_room = BinomialHeap()
    er_database = RedBlackTree()
    
    return jsonify({"status": "success", "message": "All records cleared!"})

@app.route('/get_state', methods=['GET'])
def get_state():
    # Returns the full layout of both structures
    return jsonify({
        "binomial_heap": serialize_binomial_heap(er_waiting_room),
        "red_black_tree": serialize_rbt_node(er_database, er_database.root)
    })

if __name__ == '__main__':
    app.run(debug=True)