from Estructuras import Node


class Graph:
    def __init__(self):
        self._Nodes = []

    #Funciones útiles para el grupo
    def searchnode(self, Name):
        # Busqueda del nodo mediante el nombre
        for i in range(0, len(self._Nodes)):
            if self._Nodes[i].name == Name:
                return self._Nodes[i]
            else:
                continue
    def addnode(self, name, value):
        # Creación del nodo
        NewNode = Node.Node(name, value)
        # Adición a la lista de nodos
        self._Nodes.append(NewNode)
        return NewNode

    def fusenodes(self,Name1,Name2):
        Node1=self.searchnode(Name1)
        Node2=self.searchnode(Name2)
        Node1.Points+=Node2.Points
        Dictionary=Node2.Conections.copy()
        Keys=Dictionary.keys()
        for i in Keys:
            if i==Node1.name:
                Node1.eliminateConnection(Node1,Node2)
            elif i in Node1.Conections:
                Fuse=self.searchnode(i)
                Node1.Conections[i]=[Node1.Conections[i],Node2.Conections[i]]
                self.QuickSort(Node1.Conections[i])
                Fuse.Conections[Node1.name]=Node1.Conections[i]
                Node2.eliminateConnection(Node2,self.searchnode(i))
            else:
                self.makeconection(Node1.name,i,Node2.Conections[i])
                Node2.eliminateConnection(Node2,self.searchnode(i))
        self._Nodes.remove(Node2)
        Node2.Points=[]


    def makeconection(self, Name1, Name2, peso):
        # Registrar conexión en el primer nodo
        self.searchnode(Name1).addconnection(self.searchnode(Name2),peso)
        # Registrar conexión en el segundo nodo
        self.searchnode(Name2).addconnection(self.searchnode(Name1),peso)

    def searchshortestpath(self, Name1, Name2):
        self.resetDijkstra(self._Nodes,True)
        Node1 = self.searchnode(Name1)
        Node2 = self.searchnode(Name2)
        self.Dijkstra(Node1,True)
        return Node2.path
    def searchlongestpath(self,Name1,Name2):
        self.resetDijkstra(self._Nodes,False)
        Node1 = self.searchnode(Name1)
        Node2 = self.searchnode(Name2)
        self.Dijkstra(Node1,False)
        return Node2.path


    #Funciones del algoritmo de Dijkstra
        #Funciones para corto

    def Dijkstra(self,Node1,Short):
        Node1.Distance=0
        VisitedNodes=[]
        UnvisitedNodes=[Node1]
        while len(UnvisitedNodes)!=0:
            currentNode=self.LowestDistance(UnvisitedNodes)
            UnvisitedNodes.remove(currentNode)
            for key in currentNode.Conections.keys():
                adjacentNode=self.searchnode(key)
                value=currentNode.Conections[key]
                if (adjacentNode not in VisitedNodes):
                    self.MinimumDistance(adjacentNode,value,currentNode,Short)
                    UnvisitedNodes.append(adjacentNode)
            VisitedNodes.append(currentNode)

    def MinimumDistance(self,evaluationNode,weight,sourceNode,Short):
        SourceDistance=sourceNode.Distance
        if Short:
            if (SourceDistance+weight<evaluationNode.Distance):
                evaluationNode.Distance=SourceDistance+weight
                Shortestpath=[]
                Shortestpath+=sourceNode.path
                Shortestpath.append(sourceNode)
                evaluationNode.path=Shortestpath
        else:
            if (SourceDistance+weight>evaluationNode.Distance):
                evaluationNode.Distance=SourceDistance+weight
                Shortestpath=[]
                Shortestpath+=sourceNode.path
                Shortestpath.append(sourceNode)
                evaluationNode.path=Shortestpath
    def LowestDistance(self,NodeList):
        LowestDistanceNode=None
        lowestdistance=float("inf")
        for Node in NodeList:
            nodeDistance=Node.Distance
            if nodeDistance<lowestdistance:
                lowestdistance=nodeDistance
                LowestDistanceNode=Node
        return LowestDistanceNode
        #Funciones para largo


    def resetDijkstra(self,Lista,Short):
        for i in Lista:
            if Short:
                i.Distance=float("inf")
                i.path=[]
            else:
                i.Distance=-float("inf")
                i.path=[]