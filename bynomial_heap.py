class BinomialNode:
    def __init__(self, patient_name, severity):
        self.patient_name = patient_name
        self.key = severity  # Lower number = higher priority
        self.degree = 0
        self.p = None        # parent pointer
        self.child = None    # leftmost child
        self.sibling = None  # right sibling

class BinomialHeap:
    def __init__(self):
        self.head = None

    def binomial_link(self, y, z):
        y.p = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def _merge_roots(self, h1, h2):
        if not h1: return h2
        if not h2: return h1

        dummy = BinomialNode(None, -1)
        tail = dummy
        
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling
            
        tail.sibling = h1 if h1 else h2
        return dummy.sibling

    # Union with 4 cases
    def union(self, other_head):
        new_head = self._merge_roots(self.head, other_head)
        if not new_head:
            self.head = None
            return

        prev_x = None
        x = new_head
        next_x = x.sibling

        while next_x is not None:
            # Cases 1 and 2
            if (x.degree != next_x.degree) or \
               (next_x.sibling is not None and next_x.sibling.degree == x.degree):
                prev_x = x
                x = next_x
            # Case 3
            elif x.key <= next_x.key:
                x.sibling = next_x.sibling
                self.binomial_link(next_x, x)
            # Case 4
            else:
                if prev_x is None:
                    new_head = next_x
                else:
                    prev_x.sibling = next_x
                self.binomial_link(x, next_x)
                x = next_x
            next_x = x.sibling
            
        self.head = new_head

    def insert(self, patient_name, severity):
        new_node = BinomialNode(patient_name, severity)
        self.union(new_node)

    def extract_min(self):
        if not self.head:
            return None

        # Find the root with the minimum key
        min_node = self.head
        min_prev = None
        curr = self.head
        prev = None

        while curr is not None:
            if curr.key < min_node.key:
                min_node = curr
                min_prev = prev
            prev = curr
            curr = curr.sibling

        # Delete min_node from the root list
        if min_prev is None:
            self.head = min_node.sibling
        else:
            min_prev.sibling = min_node.sibling

        # Reverse the order of the chained list of children
        child = min_node.child
        prev_child = None
        while child is not None:
            next_child = child.sibling
            child.sibling = prev_child
            child.p = None  # Roots have no parent
            prev_child = child
            child = next_child

        # Union the main heap with the reversed children heap
        self.union(prev_child)

        return min_node