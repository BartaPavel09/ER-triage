class RBNode:
    def __init__(self, key, patientName=""):
        self.key = key
        self.patientName = patientName
        self.col = "BLACK"
        self.p = None
        self.left = None
        self.right = None


class RedBlackTree:
    def __init__(self):
        self.Nil = RBNode(0)
        self.Nil.col = "BLACK"
        self.Nil.left = self.Nil
        self.Nil.right = self.Nil
        self.root = self.Nil

    def isNil(self, node):
        return node == self.Nil

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.Nil:
            y.left.p = x
        y.p = x.p
        if x.p == self.Nil:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def rightRotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.Nil:
            x.right.p = y
        x.p = y.p
        if y.p == self.Nil:
            self.root = x
        elif y == y.p.left:
            y.p.left = x
        else:
            y.p.right = x
        x.right = y
        y.p = x

    def insert(self, key, patientName):
        z = RBNode(key, patientName)

        y = self.Nil
        x = self.root
        while not self.isNil(x):
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.p = y
        if self.isNil(y):
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        z.left = self.Nil
        z.right = self.Nil
        z.col = "RED"
        self.insertFixup(z)

    def insertFixup(self, z):
        while z.p.col == "RED":
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.col == "RED":
                    z.p.col = "BLACK"
                    y.col = "BLACK"
                    z.p.p.col = "RED"
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.leftRotate(z)
                    z.p.col = "BLACK"
                    z.p.p.col = "RED"
                    self.rightRotate(z.p.p)
            else:
                y = z.p.p.left
                if y.col == "RED":
                    z.p.col = "BLACK"
                    y.col = "BLACK"
                    z.p.p.col = "RED"
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.rightRotate(z)
                    z.p.col = "BLACK"
                    z.p.p.col = "RED"
                    self.leftRotate(z.p.p)
        self.root.col = "BLACK"

    def search(self, w, key):
        if self.isNil(w) or w.key == key:
            return w
        if key < w.key:
            return self.search(w.left, key)
        return self.search(w.right, key)
