class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.Conections = {}

    def addconnection(self, Node):
        self.Conections[Node.name] = 0

    def setpeso(self, Node, peso):
        self.Conections[Node.name] = peso
