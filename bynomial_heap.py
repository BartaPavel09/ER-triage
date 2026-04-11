class BinomialNode:
    def __init__(self, patient_name, severity):
        self.patient_name = patient_name
        self.severity = severity # Lower number = higher priority
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None

class BinomialHeap:
    def __init__(self):
        self.head = None

    def insert(self, patient_name, severity):
        pass