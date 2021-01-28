class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.Conections = {}
        self.Points = []

    def addconnection(self, Node,Peso) :
        self.Conections[Node.name] = Peso
