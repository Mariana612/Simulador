class Node:
    def __init__(self,name,value):
        self.name=name
        self.value=value
        self.Conections={}

    def addconnection(self,Nodo):
        self.Conections[Nodo.name]=0
    def setpeso(self,Node,peso):
        self.Conections[Node.name]=peso