import numpy as np
from typing import List


def get_tour_distance(
    Tour: List,
    dist_matrix: np.array
) -> float:
    """
    Given an array of indexes, calculate the distance through the
    distance matrix.

    Args:
        Tour (np.array): array of indexes
        dist_matrix (np.array): 2-d array of distance values

    Returns:
        float: total distance of the Tour.
    """
    Tour = Tour[0:-1]
    d = 0
    for i in range(len(Tour)):
        city_index = Tour[i]
        # The TSP always begin and end in the same city. When
        # in the last city in the tour go back to the start.
        try:
            next_city_index = Tour[i + 1]
        except IndexError:
            next_city_index = Tour[0]
        d += dist_matrix[city_index][next_city_index]
    return d
