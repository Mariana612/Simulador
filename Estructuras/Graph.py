from Estructuras import Node


class Graph:
    def __init__(self):
        self._Nodes = []

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
        Node1 = self.searchnode(Name1)
        Node2 = self.searchnode(Name2)

    #Ordenamiento de Datos
    def shellsort(self, list):
        n = len(list)
        partition=n//2
        while partition>0:
            for i in range(partition,n):
                temporal=list[i]
                j=i
                while j>=partition and list[j-partition]<temporal:
                    list[j]=list[j-partition]
                    j-=partition
                list[j]=temporal
            partition//=2
    def QuickSort(self,Lista):
        self.QuickSortaux(Lista,0,len(Lista)-1)
    def QuickSortaux(self,Lista,Low,High):
        if Low<High:
            index=self.Partition(Lista,Low,High)

            self.QuickSortaux(Lista,Low,index-1)
            self.QuickSortaux(Lista,index,High)
    def Partition(self,Lista,Low,High):
        index=Low-1
        pivot=Lista[High]
        for i in range(Low,High):
            if Lista[i]<pivot:
                index=index+1
                Lista[index],Lista[i]=Lista[i],Lista[index]
        Lista[index+1],Lista[High]=Lista[High],Lista[index+1]
        return i+1

Grafo=Graph()
Grafo.addnode("Mike",12)
Grafo.addnode("Kory",90)
Grafo.addnode("Banana",34)
Grafo.makeconection("Mike","Kory",23)
Grafo.makeconection("Banana","Mike",7)
Grafo.searchnode("Banana").Points=[1,2,3,4]
Grafo.searchnode("Mike").Points=[4,5,6,7]
Grafo.fusenodes("Banana","Mike")
print("Fin")