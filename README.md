# Emergency Room Triage Simulator

## 1. Application Overview
The ER Triage Simulator is an interactive web application designed to demonstrate the real-time management of a hospital emergency room using advanced data structures. It provides a visual dashboard where patients can be admitted with varying levels of severity and treated based on priority. 

The application utilizes two primary data structures running on a Python backend, with real-time visualization rendered on an HTML5 Canvas via a Flask API.

## 2. Data Structures Used

### Binomial Heap (The waiting room / priority queue)
* **Purpose:** Handles the immediate triage queue, ensuring the doctor always treats the patient with the highest severity (lowest key number) next.
* **Why it was chosen:** While a standard binary heap could work, a Binomial Heap was selected for its superior $O(\log n)$ union operation. In a real-world scenario where two hospital wards might merge their waiting rooms, a binomial heap handles this exponentially faster than standard priority queues.
* **Implementation details:** Written from scratch following CLRS logic. It uses a `BinomialNode` with pointers to its parent, leftmost child, and right sibling. It supports $O(\log n)$ `insert` and `extractMin` operations, utilizing the standard `union` and `binomialLink` logic to merge trees of equal degree.

### Red-Black Tree (The patient records database)
* **Purpose:** Acts as the historical database for all admitted patients.
* **Why it was chosen:** A hospital needs to quickly look up, insert, and update patient records regardless of how many patients arrive. A standard Binary Search Tree (BST) could degrade into a linked list $O(n)$ if patients arrive with perfectly increasing severities. The Red-Black Tree guarantees $O(\log n)$ height, ensuring fast performance in all scenarios.
* **Implementation details:** Implements strict CLRS Red-Black logic, including the use of a centralized sentinel `Nil` node (colored Black) to replace standard null pointers. It automatically executes Left and Right Rotations and color-flipping (`insertFixup`) to maintain its balanced properties after every insertion.

## 3. How to Run the Program

**Prerequisites:**
* Python 3.8+ installed on your machine.

**Setup instructions:**
1. Open a terminal and navigate to the project directory.
2. Create and activate a virtual environment:
   * Mac/Linux: `python -m venv venv` followed by `source venv/bin/activate`
   * Windows: `python -m venv venv` followed by `venv\Scripts\activate`
3. Install the required web framework:
   * `pip install Flask`
4. Start the server:
   * `python app.py`
5. Open a web browser and navigate to: `http://127.0.0.1:5000/`

**Usage:**
Enter a patient's name and a severity score (e.g., 1 for critical, 10 for minor). Click "Admit Patient" to watch the data structures update in real-time. Click "Doctor Ready" to extract the minimum node from the Binomial Heap.
