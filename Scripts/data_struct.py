class Graphe:
    def __init__(self):
        self.adj = {}
    
    def addsummit(self, s):
        if s not in self.adj:
            self.adj[s] = set()
    
    def addedge(self, s1, s2):
        self.addsummit(s1)
        self.addsummit(s2)
        self.adj[s1].add(s2)
        self.adj[s2].add(s1)
    
    def edge(self, s1, s2):
        return s2 in self.adj[s1]
    
    def summits(self):
        return list(self.adj)
    
    def neightboor(self, s):
        return list(self.adj[s])
    #EX 8
    def display(self):
        for s1 in self.adj:
            print(s1,self.neightboor(s1))
    #EX 9
    def nb_summit(self):
        return len(self.summits())
    
    def degre(self,s):
        return len(self.adj[s])
    
    def nb_edge(self):
        compt = 0
        for s in self.adj:
            compt += self.degre(s)
        return compt/2
    
    def remove_edge(self,s1,s2):
        self.adj[s1].remove(s2)

class Pile:
    """structure de pile"""
    
    def __init__(self):
        self.contenu = []
    
    def est_vide(self):
        return len(self.contenu) == 0
    
    def empiler(self, v):
        self.contenu.append(v)
    
    def depiler(self):
        if self.est_vide():
            raise IndexError("depiler sur une pile vide")
        return self.contenu.pop()
        
    def taille(self):
        return len(self.contenu)
    
    def vider(self):
        self.contenu = []


class File:
    def __init__(self) -> None:
        self.contenu = []

    def __str__(self) -> str:

        self.chaine = ""

        for ele in self.contenu:
            self.chaine += str(ele) + ", " 
        
        return self.chaine
    
    def is_empty(self):
        return len(self.contenu) == 0
    
    def add(self, e):
        self.contenu.append(e)
    
    def remove(self):
        return self.contenu.pop(0)


