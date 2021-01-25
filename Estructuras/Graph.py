from Estructuras import Node
class Grafo:
    def __init__(self):
        self._Nodes=[]
    def searchnode(self,Name):
        #Busqueda del nodo mediante el nombre
        for i in range(0,len(self._Nodes)):
            if self._Nodes[i].name==Name:
                return self._Nodes[i]
            else:
                continue
    def addnode(self,name,value):
        #Creación del nodo
        NewNode=Node.Node(name,value)
        #Adición a la lista de nodos
        self._Nodes.append(NewNode)
    def makeconection(self,Name1,Name2):
        #Registrar conexión en el primer nodo
        self.searchnode(Name1).addconnection(self.searchnode(Name2))
        #Registrar conexión en el segundo nodo
        self.searchnode(Name2).addconnection(self.searchnode(Name1))
    def searchshortestpath(self,Name1,Name2):
        Node1=self.searchnode(Name1)
        Node2=self.searchnode(Name2)
