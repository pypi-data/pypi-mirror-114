import numpy as np
from time import time
from typing import List, Tuple
from tsp_heuristics.heuristics.utils import get_tour_distance

def nn_algo(
    dist_matrix: np.array,
    start: int = 0
) -> Tuple[List, float]:
    """
    From a start city index, get an Tour according to the Nearest Neighbor
    algorithm from the collection of the cities indexes.
    
    Args:
        dist_matrix (np.array)
        start (int, optional): The first city that we will begin the Tour and
        eventually return. Defaults to 0.

    Returns:
        np.array: Array of indexes representing the city Tour.
        float: Time to complete the algorithm.
    """
    t0 = time()
    Tour = [start]
    
    dist_matrix = dist_matrix.astype(float)
    # Making the distance to go to the same
    # city impossible.
    for i in range(dist_matrix.shape[0]):
        dist_matrix[i][i] = np.Inf
    
    for _ in range(dist_matrix.shape[0] - 1):
        # Finding the best next city.
        min_index = np.argmin(dist_matrix[Tour[-1]])
        # Making sure that we won't revisit
        # the same city.
        for t in Tour:
            dist_matrix[min_index][t] = np.Inf
            dist_matrix[t][min_index] = np.Inf
        Tour.append(min_index)
    
    return Tour, get_tour_distance(Tour, dist_matrix), (time() - t0)
