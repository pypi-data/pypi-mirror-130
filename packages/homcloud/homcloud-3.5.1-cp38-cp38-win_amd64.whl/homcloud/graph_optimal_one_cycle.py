from collections import deque
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


def search(adj_matrix, birth, weighted=False):
    if weighted:
        return search_for_weighted_graph(adj_matrix, birth)
    else:
        return Finder(adj_matrix, birth).search()

TERM = -1


def search_starting_edge(matrix, birth):
    xs, ys = np.nonzero(matrix == birth)
    if xs.size == 0:
        raise(RuntimeError("Invalid birth time"))
    if xs.size > 2:
        raise(RuntimeError("Pairs with the same birth time"))
    return sorted([xs[0], ys[0]])


def search_for_weighted_graph(adjacent_matrix, birth):
    def path(predecessors, start, end):
        result = [end]
        at = end
        while at != start:
            at = predecessors[at]
            result.append(at)
        return result

    start, end = search_starting_edge(adjacent_matrix, birth)
    matrix = adjacent_matrix.copy()
    matrix[matrix >= birth] = 0.0
    graph = csr_matrix(matrix)
    dist_matrix, predecessors = dijkstra(graph, False, start, True)
    return path(predecessors, start, end)
 
    
class Finder(object):
    def __init__(self, adjacent_matrix, birth):
        self.matrix = adjacent_matrix
        self.birth = birth
        self.visited = set()
        self.prev = dict()

    def search(self):
        start, end = search_starting_edge(self.matrix, self.birth)
        g = self.matrix < self.birth
        queue = deque([start])
        self.visited.add(start)
        self.prev[start] = TERM
        
        while queue:
            v = queue.popleft()
            if v == end:
                return self.path(end)
            for n in range(self.num_points):
                if not g[n, v]:
                    continue
                if n in self.visited:
                    continue
                
                self.visited.add(n)
                self.prev[n] = v
                queue.append(n)

        raise(RuntimeError("No loop containing birth"))

    def path(self, end):
        v = end
        path = []
        while True:
            path.append(v)
            v = self.prev[v]
            if v == TERM:
                return path

    @property
    def num_points(self):
        return self.matrix.shape[0]
        


        
    
