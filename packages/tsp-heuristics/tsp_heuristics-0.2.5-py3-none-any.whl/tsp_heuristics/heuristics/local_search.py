import numpy as np
from random import sample
from tsp_heuristics.heuristics.utils import get_tour_distance

from typing import Generator, List, Tuple
from time import time


def two_opt_gen(
    Tour: List
) -> Generator:
    """
    Generates a neighborhood of 2-opt in the Tour, which means deleting
    two edges from the Tour and swap it. It creates in a random order all the
    neighborhood.

    Args:
        Tour (List)

    Yields:
        Generator: List of neighborhood from the 2-opt method.
    """
    x = Tour
    n = len(x)
    i_range = range(2, n)
    for i in sample(i_range, len(i_range)):
        j_range = range(i + 1, n + 1)
        for j in sample(j_range, len(j_range)):
            xn = x
            xn = xn[:i - 1] + list(reversed(xn[i - 1:j])) + xn[j:]
            yield xn


def local_search_algo(
    Tour: List,
    dist_matrix: np.array,
    method: str = 'best improvement'
) -> Tuple[List, float, float]:
    """
    In summary, search through 3 available methods the best solution in the
    neighboring initial solution or Tour.

    Args:
        Tour (List)
        dist_matrix (np.array)
        method (str, optional): One of the 3 available methods:
        'first improvement', 'best improvement' and 'random'.
        Defaults to 'best improvement'.

    Returns:
        Tuple[List, float]: Tour and time to execute the algorithm.
    """
    t0 = time()
    
    early_stop = False if method == 'best improvement' else True
    improvement = True
    while improvement:
        improvement = False
        best_Tour_distance = get_tour_distance(Tour, dist_matrix)
        for n in two_opt_gen(Tour):
            n_tour_distance = get_tour_distance(n, dist_matrix)
            if n_tour_distance < best_Tour_distance:
                improvement = True
                Tour = n
                best_Tour_distance = n_tour_distance
                if early_stop:
                    break
    
    return Tour, get_tour_distance(Tour, dist_matrix), (time() - t0)

