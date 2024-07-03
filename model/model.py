import copy

import networkx as nx
from geopy import distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listaAnni = []
        self.listaForma = []

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}
        self.adiacenti = []

        self.bestPath = []
        self.bestScore = 0

        self.loadAnni()
        self.loadForme()

    def getBestPath(self):
        self.bestPath = []
        self.bestScore = 0

        for n in self.nodes:
            parziale = [n]
            archi_visitati = []
            pesi = []

            self._ricorsione(parziale, archi_visitati, pesi)

        return self.bestPath, self.bestScore

    def _ricorsione(self, parziale, archi_visitati, pesi):
        rimanenti = self.getRimanenti(parziale, pesi, archi_visitati)

        if len(rimanenti) == 0:
            if self.calcolaDistanza(parziale) > self.bestScore:
                self.bestScore = self.calcolaDistanza(parziale)
                self.bestPath = copy.deepcopy(parziale)
            return

        for v in rimanenti:
            archi_visitati.append((parziale[-1], v))
            pesi.append(self.graph[parziale[-1]][v]['weight'])
            parziale.append(v)
            self._ricorsione(parziale, archi_visitati, pesi)
            archi_visitati.pop()
            pesi.pop()
            parziale.pop()

    def getRimanenti(self, parziale, pesi, archi_visitati):
        vicini = sorted(self.graph[parziale[-1]], key=lambda x: self.graph[parziale[-1]][x]['weight'], reverse=True)
        rimanenti = []
        for v in vicini:
            if (not pesi or self.graph[parziale[-1]][v]['weight'] > max(pesi)) and (parziale[-1], v) not in archi_visitati and (v, parziale[-1]) not in archi_visitati:
                rimanenti.append(v)
        return rimanenti


    def calcolaDistanza(self, lista):
        distanza = 0
        for i in range(len(lista) - 1):
            v1 = lista[i]
            v2 = lista[i + 1]
            distanza += distance.geodesic((v1.Lat, v1.Lng), (v2.Lat, v2.Lng)).km

        return distanza


    def loadAnni(self):
        self.listaAnni = DAO.getAnni()

    def loadForme(self):
        self.listaForma = DAO.getForme()

    def buildGraph(self, forma, anno):
        self.graph.clear()
        self.nodes = DAO.getNodes()
        self.graph.add_nodes_from(self.nodes)
        for node in self.nodes:
            self.idMap[node.id] = node

        self.edges = DAO.getEdge(forma, anno, self.idMap)
        for e in self.edges:
            self.graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getAdiacenti(self):
        self.adiacenti = []
        for n in self.nodes:
            peso = 0
            for v in self.graph[n]:
                peso += self.graph[n][v]['weight']

            self.adiacenti.append((n, peso))

    def getWeight(self, v0,v1):
        return self.graph[v0][v1]['weight']

    def calcolaDistanzaSingola(self, v1, v2):
        distanza = distance.geodesic((v1.Lat, v1.Lng), (v2.Lat, v2.Lng)).km
        return distanza

