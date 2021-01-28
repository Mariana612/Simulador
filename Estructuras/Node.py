class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.Conections = {}
        self.Points = []
    def eliminateConnection(self,Node1,Node2):
        Node1.Conections.pop(Node2.name)
        Node2.Conections.pop(Node1.name)
    def addconnection(self, Node,Peso) :
        if Node.name in self.Conections:
            self.Conections[Node.name]=[self.Conections[Node.name],Peso]
        else:
            self.Conections[Node.name]=Peso
