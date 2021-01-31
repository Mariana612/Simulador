class Node:
    """
Clase que representa un Nodo de un grafo
Autor: Marcelo Truque
    """

    def __init__(self, name, value):
        """
Inicializador de la clase Nodo
Autor: Marcelo Truque
Entrada:Nombre del nodo, valor de resistencia o voltaje
        """
        self.name = name
        self.value = value
        self.Distance=float("inf")
        self.path=[]
        self.Conections = {}
        self.Points = []

    def eliminateConnection(self, Node1, Node2):
        """
Función para eliminar la conxión entre dos nodos
Autor: Marcelo Truque
Entrada:Nodos a desconectar
        """
        Node1.Conections.pop(Node2.name)
        Node2.Conections.pop(Node1.name)

    def addconnection(self, Node, Peso):
    """
Función Añadir una conexión entre dos nodos
Autor: Marcelo Truque
Entrada:Nodo a conectar y el peso a asignar a la conexión
        """
        if Node.name in self.Conections:
            if isinstance(self.Conections[Node.name],list):
                newvalue=[Peso]
                newvalue+=self.Conections[Node.name]
                self.Conections[Node.name]=newvalue
            else:
                self.Conections[Node.name] = [self.Conections[Node.name], Peso]

        else:
            self.Conections[Node.name] = Peso