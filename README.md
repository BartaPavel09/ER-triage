# Emergency Room Triage Simulator

## 1. Application Overview
The ER Triage Simulator is an interactive web application that models real-time patient management in a hospital emergency room using two advanced data structures. Patients can be admitted with a severity score, queued by priority, treated in order of urgency, updated if their condition changes, or removed from the system entirely. Both data structures are visualized live on HTML5 Canvas after every action.

The backend is a Python Flask server. The frontend is plain HTML/CSS/JavaScript with two Canvas elements - one per data structure.

---

## 2. Data Structures

### Binomial Heap (Waiting room / priority queue)
- **Purpose:** Holds patients currently waiting to be seen. The doctor always treats the most critical patient first (lowest severity key).
- **Why:** A standard binary heap has an O(n) union operation. The Binomial Heap reduces this to O(log n) by storing the queue as a forest of Binomial Trees merged analogously to binary addition - useful when two ward queues need to be merged.
- **Key methods:**
  - `insert(patientName, severity)` - wraps the new node as a B0 tree and calls `union()`. O(log n).
  - `union(otherHead)` - merges two root lists via `_mergeRoots()` then consolidates equal-degree trees with `binomialLink()`. O(log n).
  - `extractMin()` - removes the minimum root, reverses its children, and reintegrates them via `union()`. O(log n).
  - `decreaseKey(node, newKey)` - lowers a node's key and bubbles it up by swapping data with its parent. O(log n).
  - `delete(node)` - calls `decreaseKey(node, -1)` to float the node to the top, then `extractMin()`. O(log n).
  - `findNode(name)` - recursive search across the full heap forest by patient name. O(n).

### Red-Black Tree (Patient records database)
- **Purpose:** Stores every admitted patient permanently, sorted by severity. Supports fast lookup, insert, update, and delete.
- **Why:** A plain BST degrades to O(n) height with sorted input. The Red-Black Tree enforces five coloring invariants that bound height to 2 log(n+1), guaranteeing O(log n) in all cases.
- **Key methods:**
  - `insert(key, patientName)` - standard BST insert followed by `insertFixup()`. O(log n).
  - `insertFixup(z)` - restores coloring invariants via recolorings and at most two rotations (three symmetric cases). O(log n).
  - `delete(z)` - full CLRS RB-DELETE: splices in the successor via `rbTransplant()`, preserves original color, calls `deleteFixup()` if a BLACK node was removed. O(log n).
  - `deleteFixup(x)` - restores black-height invariant via four cases (and mirrors), at most three rotations total. O(log n).
  - `findNode(w, key, name)` - BST walk by key; searches both subtrees on key ties since rotations can place duplicates on either side. O(log n) typical, O(n) worst case with many duplicates.
  - `leftRotate(x)` / `rightRotate(y)` - O(1) structural rotations, update all affected parent pointers.

---

## 3. API Endpoints

| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| GET | `/` | `home()` | Serves the HTML page |
| POST | `/add_patient` | `addPatient()` | Inserts patient into heap and RBT |
| POST | `/treat_patient` | `treatPatient()` | Calls `extractMin()` on the heap |
| POST | `/delete_patient` | `deletePatient()` | Removes patient from both structures |
| POST | `/update_severity` | `updateSeverity()` | Delete + reinsert with new key in both structures |
| POST | `/reset` | `resetHospital()` | Reinitializes both structures to empty |
| GET | `/get_state` | `getState()` | Returns serialized state of both structures |

---

## 4. How to Run

**Prerequisites:** Python 3.8+

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependency
pip install Flask

# Run
python app.py
```

Open `http://127.0.0.1:5000/` in a browser.

---

## 5. Usage

- **Admit patient:** Enter a name and severity (1–10), click Admit Patient.
- **Treat patient:** Click Doctor Ready - removes the highest-priority patient from the heap. Record stays in the RBT.
- **Delete patient:** Enter exact name and current severity in the Manage Patient section, click Delete Patient.
- **Update severity:** Enter name, current severity, and new severity, click Switch Severity. Internally deletes and reinserts in both structures.
- **Reset:** Click Clear All Records to wipe everything.
