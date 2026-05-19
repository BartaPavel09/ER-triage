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

    def findNode(self, w, key, name):
        if self.isNil(w):
            return self.Nil
        if w.key == key and w.patientName == name:
            return w
        
        # If the key is smaller, it MUST be on the left
        if key < w.key:
            return self.findNode(w.left, key, name)
        # If the key is larger, it MUST be on the right
        elif key > w.key:
            return self.findNode(w.right, key, name)
        else:
            # Key is equal, but name is different. 
            # Due to rotations, it could be in either subtree.
            left_res = self.findNode(w.left, key, name)
            if not self.isNil(left_res):
                return left_res
            return self.findNode(w.right, key, name)

    def minimum(self, x):
        while not self.isNil(x.left):
            x = x.left
        return x

    def rbTransplant(self, u, v):
        if self.isNil(u.p):
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def delete(self, z):
        y = z
        y_original_color = y.col
        if self.isNil(z.left):
            x = z.right
            self.rbTransplant(z, z.right)
        elif self.isNil(z.right):
            x = z.left
            self.rbTransplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.col
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.rbTransplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.rbTransplant(z, y)
            y.left = z.left
            y.left.p = y
            y.col = z.col
        
        if y_original_color == "BLACK":
            self.deleteFixup(x)

    def deleteFixup(self, x):
        while x != self.root and x.col == "BLACK":
            if x == x.p.left:
                w = x.p.right
                if w.col == "RED":
                    w.col = "BLACK"
                    x.p.col = "RED"
                    self.leftRotate(x.p)
                    w = x.p.right
                if w.left.col == "BLACK" and w.right.col == "BLACK":
                    w.col = "RED"
                    x = x.p
                else:
                    if w.right.col == "BLACK":
                        w.left.col = "BLACK"
                        w.col = "RED"
                        self.rightRotate(w)
                        w = x.p.right
                    w.col = x.p.col
                    x.p.col = "BLACK"
                    w.right.col = "BLACK"
                    self.leftRotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.col == "RED":
                    w.col = "BLACK"
                    x.p.col = "RED"
                    self.rightRotate(x.p)
                    w = x.p.left
                if w.right.col == "BLACK" and w.left.col == "BLACK":
                    w.col = "RED"
                    x = x.p
                else:
                    if w.left.col == "BLACK":
                        w.right.col = "BLACK"
                        w.col = "RED"
                        self.leftRotate(w)
                        w = x.p.left
                    w.col = x.p.col
                    x.p.col = "BLACK"
                    w.left.col = "BLACK"
                    self.rightRotate(x.p)
                    x = self.root
        x.col = "BLACK"
