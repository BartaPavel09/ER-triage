class BinomialNode:
    def __init__(self, patientName, severity):
        self.patientName = patientName
        self.key = severity  # Lower number = higher priority
        self.degree = 0
        self.p = None  # parent pointer
        self.child = None  # leftmost child
        self.sibling = None  # right sibling


class BinomialHeap:
    def __init__(self):
        self.head = None

    def binomialLink(self, y, z):
        y.p = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def _mergeRoots(self, h1, h2):
        if not h1:
            return h2
        if not h2:
            return h1

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
    def union(self, otherHead):
        newHead = self._mergeRoots(self.head, otherHead)
        if not newHead:
            self.head = None
            return

        prevX = None
        x = newHead
        nextX = x.sibling

        while nextX is not None:
            # Cases 1 and 2
            if (x.degree != nextX.degree) or (
                nextX.sibling is not None and nextX.sibling.degree == x.degree
            ):
                prevX = x
                x = nextX
            # Case 3
            elif x.key <= nextX.key:
                x.sibling = nextX.sibling
                self.binomialLink(nextX, x)
            # Case 4
            else:
                if prevX is None:
                    newHead = nextX
                else:
                    prevX.sibling = nextX
                self.binomialLink(x, nextX)
                x = nextX
            nextX = x.sibling

        self.head = newHead

    def insert(self, patientName, severity):
        newNode = BinomialNode(patientName, severity)
        self.union(newNode)

    def extractMin(self):
        if not self.head:
            return None

        # Find the root with the minimum key
        minNode = self.head
        minPrev = None
        curr = self.head
        prev = None

        while curr is not None:
            if curr.key < minNode.key:
                minNode = curr
                minPrev = prev
            prev = curr
            curr = curr.sibling

        # Delete minNode from the root list
        if minPrev is None:
            self.head = minNode.sibling
        else:
            minPrev.sibling = minNode.sibling

        # Reverse the order of the chained list of children
        child = minNode.child
        prevChild = None
        while child is not None:
            nextChild = child.sibling
            child.sibling = prevChild
            child.p = None  # Roots have no parent
            prevChild = child
            child = nextChild

        # Union the main heap with the reversed children heap
        self.union(prevChild)

        return minNode

    def findNode(self, name, node="INIT"):
        # Initial call
        if node == "INIT":
            node = self.head
        
        # Base case for recursion
        if node is None:
            return None
        
        curr = node
        while curr is not None:
            if curr.patientName == name:
                return curr
            res = self.findNode(name, curr.child)
            if res:
                return res
            curr = curr.sibling
        return None

    def decreaseKey(self, node, newKey):
        if newKey > node.key:
            return  # Can't increase key in decreaseKey
        
        node.key = newKey
        y = node
        z = y.p
        while z is not None and y.key < z.key:
            # Swap data between y and z
            y.patientName, z.patientName = z.patientName, y.patientName
            y.key, z.key = z.key, y.key
            y = z
            z = y.p

    def delete(self, node):
        self.decreaseKey(node, -1)  # -1 is always smaller than 1-10 severity
        self.extractMin()
