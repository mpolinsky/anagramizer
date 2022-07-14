# Node.py

# class node
# holds integer data
# Note: I tried to make this more of a proper node class
# by adding the parent, hvalue, and pathCost, though they
# are not used by this traversal program.
class Node:
    def __init__(self, name, anagram, pool, parent):
        # node data
        self.name = name
        self.anagram = anagram
        self.pool = pool
        # parent node
        self.parent = parent
        # heuristic score of node
        self.hvalue  = 0
        # g(n) cost from root to this node.
        self.pathCost = 0
        # action is the action that generated this node
        self.action = 0

    #### ACCESSORS ####

    # returns node data
    def getData(self):
        return self.data
    # sets node data    
    def setData(self, data):
        self.data = data
    # returns parent node
    def getParent(self):
        return self.parent
    # sets parent node
    def setParent(self, parentNode):
        self.parent = parentNode
    # sets hvalue
    def getValue(self):
        return self.hvalue
    # sets node hvalue    
    def sethvalue(self, value):
        hvalue = value
    
    # returns pathCost from root (g(n))
    def getPathCost(self):
        return self.pathCost
    # sets pathCost
    def setPathCost(self, cost):
        pathCost = cost
    
    def getAction(self):
        return self.action
    
    def setAction(self,action):
        self.action = action

    def get_name(self):
        return self.name

    def get_anagram(self):
        return self.anagram

    def get_word_pool(self):
        return self.pool
    
    def __repr__(self):
       return f"""Node({self.name}, {self.anagram}, {self.pool})"""

    # test parent, name, anagram, and word pool for equality.
    def __eq__(self, other):
        return self.parent == other.parent and self.name == other.name and self.anagram == other.anagram and self.pool == other.pool

    
