from os import path, getcwd
from PyQt5.QtWidgets import QMessageBox
from collections import deque
from ast import literal_eval

class Graph:
    _adj: dict
    _directed: bool
    _weighted: bool
    _filePath: str
    _inputType: str
    _algoValues: dict


    def __init__(self):
        self._adj = {}
        self._directed = False
        self._weighted = False
        self._inputType = "adj list"
        self._filePath = path.join(getcwd(), "input.txt").replace("\\", "/")
        self._algoValues = {}

    def getFields(self):
        return self._adj, self._directed, self._weighted, self._algoValues


    def print(self):
        for key, value in self._adj.items():
            print(f"[{key}] -> ", end="")
            print(f"{value}")


    def addVertices(self, *verts):
        for v in verts:
            if v not in self._adj.keys():
                self._adj[v] = {}


    def addEdges(self, start, ends):
        self.addVertices(*range(1, max(start, *ends)+1))
        self._adj[start] = {**self._adj[start], **ends}
        
        if not self._directed:  # if underected
            for end in ends.keys():
                if end in self._adj.keys():
                    self._adj[end] = {**self._adj[end], **{start: 1}}
                else:
                    self._adj[end] = {start: 1}


    def convert_matrix_to_list(self, matrix):
        G = {}
        for a in range(len(matrix)):
            for b in range(len(matrix)):
                if matrix[a][b]:
                    if a + 1 not in G:
                        G[a + 1] = {b + 1: matrix[a][b]}
                    else:
                        G[a + 1][b + 1] = matrix[a][b]
        return G


    def openGraph(self, path):
        try:
            with open(path, "r") as file:
                    self.setFields(literal_eval(file.readline()))
        except Exception:
            self.showError("File corrupted")


    def setFields(self, values):
        self._adj = values["_adj"]
        self._directed = values["_directed"]
        self._weighted = values["_weighted"]
        self._algoValues = values["_algoValues"]


    def saveGraph(self, path):
        with open(path, "w") as file:
            tempdict = {}
            tempdict["_adj"] = self._adj
            tempdict["_directed"] = self._directed
            tempdict["_weighted"] = self._weighted
            tempdict["_algoValues"] = self._algoValues
            file.write(f"{tempdict}")


    def readGraph(self):
        try:
            with open(self._filePath, "r") as fin:
                if self._inputType == "Adjacency List":
                    self._adj = {}
                    while True:
                        temp = [int(i) for i in fin.readline().split()]
                        if temp == []:
                            break
                        if self._weighted:
                            for i in range(0, len(temp), 3):
                                self.addEdges(temp[i], {temp[i+1]:temp[i+2]})
                        else:
                            for i in range(0, len(temp), 2):
                                self.addEdges(temp[i], {temp[i+1]:1})
                elif self._inputType == "Adjacency Matrix":
                    matrix = []
                    while True:
                        temp = [int(i) for i in fin.readline().split()]
                        if temp == []:
                            break
                        matrix.append(temp)
                    self._adj = self.convert_matrix_to_list(matrix)
        except FileNotFoundError:
            self.showError("Path error")
        except IndexError:
            self.showError("File not match input type")


    def showError(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        if error == "Path error":
            msg.setWindowTitle("Path error")
            msg.setText("Choose correct file.")
        elif error == "File not match input type":
            msg.setWindowTitle("File not match input type")
            msg.setText("Choose file with correct graph input type.")
        elif error == "Vertices not in graph":
            msg.setWindowTitle("Vertices not in graph")
            msg.setText("Select vertices in graph ")
        elif error == "Minimal path error":
            msg.setWindowTitle("The path between the vertices does not exist ")
            msg.setText("Choose other vertices")
        elif error == "File corrupted":
            msg.setWindowTitle("File corrupted")
            msg.setText("Fix file or choose another")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


    def minPathFind(self, start, goal, graph):
        if start not in graph or goal not in graph:
            self.showError("Vertices not in graph")
        queue = deque()
        visited = {start: 0}
        tmp_path = {}
        queue.append(start)
        while queue:
            v = queue.popleft()
            for u in graph[v]:
                if u not in visited or visited[v] + graph[v][u] < visited[u]:
                    visited[u] = visited[v] + graph[v][u]
                    queue.append(u)
                    tmp_path[u] = v
        v = goal
        path = deque()
        path.append(v)
        if v in tmp_path:
            while v != start:
                v = tmp_path[v]
                path.appendleft(v)
            return visited[goal], list(path)
        elif start == goal:
            return 0, [start]
        else:
            self.showError("Minimal path error")


    def coloring(self):
        colors = {}
        print("Coloring match with needed input type")
        return colors


    def initGraphFile(self, filepath):
        self._filePath = filepath
        self.readGraph()