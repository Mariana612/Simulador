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
        NewNode = Node.Node(name,value)
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
                self.quicksort(Node1.Conections[i])
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

        chequeo=self.searchnode(Name1).Conections[Name2]

        if isinstance(chequeo,list):
            self.quicksort(self.searchnode(Name1).Conections[Name2])
            self.quicksort(self.searchnode(Name2).Conections[Name1])


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
            currentNode=self.LowBigDistance(UnvisitedNodes,Short)
            UnvisitedNodes.remove(currentNode)
            for key in currentNode.Conections.keys():
                adjacentNode=self.searchnode(key)
                value=currentNode.Conections[key]
                if (adjacentNode not in VisitedNodes):
                    if isinstance(value,list):
                        if Short:
                            self.MinMaxDistance(adjacentNode,value[0],currentNode,Short)
                            UnvisitedNodes.append(adjacentNode)
                        else:
                            self.MinMaxDistance(adjacentNode, value[len(value)-1], currentNode, Short)
                            UnvisitedNodes.append(adjacentNode)

                    else:
                        self.MinMaxDistance(adjacentNode, value, currentNode, Short)
                        UnvisitedNodes.append(adjacentNode)

            VisitedNodes.append(currentNode)

    def MinMaxDistance(self,evaluationNode,weight,sourceNode,Short):
        SourceDistance=sourceNode.Distance
        if Short:
            if (SourceDistance+weight<evaluationNode.Distance):
                evaluationNode.Distance=SourceDistance+weight
                Shortestpath=[]
                Shortestpath+=sourceNode.path
                Shortestpath.append((sourceNode,weight))
                evaluationNode.path=Shortestpath
        else:
            if (SourceDistance+weight>evaluationNode.Distance):
                evaluationNode.Distance=SourceDistance+weight
                Shortestpath=[]
                Shortestpath+=sourceNode.path
                Shortestpath.append((sourceNode,weight))
                evaluationNode.path=Shortestpath
    def LowBigDistance(self,NodeList,Short):
        if Short:
            LowestDistanceNode=None
            lowestdistance=float("inf")
            for Node in NodeList:
                nodeDistance=Node.Distance
                if nodeDistance<lowestdistance:
                    lowestdistance=nodeDistance
                    LowestDistanceNode=Node
            return LowestDistanceNode
        else:
            BigestDistanceNode=None
            Bigestdistance=-float("inf")
            for Node in NodeList:
                nodeDistance=Node.Distance
                if nodeDistance>Bigestdistance:
                    Bigestdistance=nodeDistance
                    BigestDistanceNode=Node
            return BigestDistanceNode

    def resetDijkstra(self,Lista,Short):
        for i in Lista:
            if Short:
                i.Distance=float("inf")
                i.path=[]
            else:
                i.Distance=-float("inf")
                i.path=[]

    # Ordenamiento de Datos

    # Shell Sort de mayor a menor

    def shellsort(self, list):
        n = len(list)
        partition = n // 2
        while partition > 0:
            for i in range(partition, n):
                temporal = list[i]
                j = i
                while j >= partition and list[j - partition] < temporal:
                    list[j] = list[j - partition]
                    j -= partition
                list[j] = temporal
            partition //= 2

    # QuickSort de menor a mayor

    def quicksort(self, Lista):
        self.QuickSortaux(Lista, 0, len(Lista) - 1)

    def QuickSortaux(self, Lista, Low, High):
        if Low < High:
            index = self.Partition(Lista, Low, High)

            self.QuickSortaux(Lista, Low, index - 1)
            self.QuickSortaux(Lista, index, High)

    def Partition(self, Lista, Low, High):
        index = Low - 1
        pivot = Lista[High]
        for i in range(Low, High):
            if Lista[i] < pivot:
                index = index + 1
                Lista[index], Lista[i] = Lista[i], Lista[index]
        Lista[index + 1], Lista[High] = Lista[High], Lista[index + 1]
        return i + 1


Grafo=Graph()

Grafo.addnode("A",32)
Grafo.addnode("B",65)
Grafo.addnode("C",90)

Grafo.makeconection("A","B",7.37)
Grafo.makeconection("A","C",2.52)
Grafo.makeconection("B","C",5.99)


Grafo.searchlongestpath("A","C")
print("Fin")
