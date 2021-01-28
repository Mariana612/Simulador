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

