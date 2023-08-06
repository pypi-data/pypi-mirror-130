
class GraphOptimal1Cycle(object):
    """The class represents an optimal (not volume-optimal) 1-cycle computed from graph information.

    You can aquaire an optimal one cycle by :meth:`Pair.optimal_1_cycle`.

    Examples:
        >>> import numpy as np
        >>> import homcloud.interface as hc
        >>> distance_matrix = np.loadtxt("distance_matrix.txt")
        >>> pdlist = hc.PDList.from_rips_filtration(distance_matrix, maxdim=1, save_graph=True)
        >>> pd1 = pdlist.dth_diagram(1)
        >>> pair = pd1.nearest_pair_to(1.2, 1.5)
        >>> optimal_1_cycle = pair.optimal_1_cycle()
        >>> optimal_1_cycle.boundary_points()
        => [0, 2, 41, 17, 9]
    """

    def __init__(self, pair, path_vertices):
        self.pair = pair
        self.path_vertices = path_vertices

    def birth_time(self):
        """Returns the birth time of the pair.

        Returns:
            float: The birth time
        """
        return self.pair.birth_time()

    def death_time(self):
        """Returns the death time of the pair.

        Returns:
            float: The death time
        """
        return self.pair.death_time()

    def boundary_points(self):
        """Returns the points on the 1-cycle.

        Returns:
            list of int: The list of points on the cycle.
            Each point is represented by a number, which is assigned in 0-origin.
        """
        return self.path_vertices

    def boundary_points_symbols(self):
        return self.geometry_resolver(False).resolve_graph_path(self.path_vertices)

    path = boundary_points
        
    def geometry_resolver(self, use_symbol):
        return self.pair.diagram.pd.geometry_resolver(use_symbol)

    def shrink(self, epsilon):
        matrix = self.pair.diagram.pd.graph_adjacent_matrix
        result = self.path_vertices.copy()

        def reduce_once(ary):
            if len(ary) <= 3:
                return False
            v1 = ary[-3]
            v2 = ary[-2]
            v3 = ary[-1]
            if matrix[v1, v3] < self.birth_time() + epsilon:
                ary[-2:-1] = []
                return True
            else:
                return False

        
        result = self.path_vertices[:2]
        for v in self.path_vertices[3:] + [self.path_vertices[0]]:
            result.append(v)
            while reduce_once(result):
                print(result)

            
        return GraphOptimal1Cycle(self.pair, result)
        
