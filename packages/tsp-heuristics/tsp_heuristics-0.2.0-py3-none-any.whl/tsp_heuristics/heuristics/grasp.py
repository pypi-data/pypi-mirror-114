"""Pure GRASP solver"""
from random import sample
from timeit import default_timer
from typing import List, Optional, Tuple

import numpy as np
from tsp_heuristics.heuristics.local_search import local_search_algo
from tsp_heuristics.heuristics.utils import get_tour_distance as compute_permutation_distance

# Testing
from tsp_heuristics.utils.readfile import tsplib_distance_matrix
from tsp_heuristics.heuristics.nn import nn_algo

def solve_tsp_grasp(
    distance_matrix: np.ndarray,
    start_position: int = 0,
    alpha: float = 0.5,
    perturbation_scheme: str = "two_opt",
    max_iterations: int = 1, 
    max_processing_time: Optional[float] = None,
    log_file: Optional[str] = None,
) -> Tuple[List, float, float]:
    """Solve a TSP problem with a GRASP heuristic
    """
    max_processing_time = max_processing_time or np.inf

    tic = default_timer()
    best_Tour = setup(distance_matrix, None)[0]
    i = 0
    while i <= max_iterations:
        intial_Tour = constructive_phase(distance_matrix, alpha, start_position)
        optimized_Tour = local_search_algo(intial_Tour, distance_matrix,method='first improvement')[0]
        
        f_best_tour = compute_permutation_distance(best_Tour, distance_matrix)
        f_optimized_tour = compute_permutation_distance(optimized_Tour, distance_matrix)
        
        if f_best_tour > f_optimized_tour:
            best_Tour = optimized_Tour
        
        if default_timer() - tic > max_processing_time:
            i = max_iterations + 1
            break
        
        i += 1
    return best_Tour, compute_permutation_distance(best_Tour, distance_matrix), (default_timer() - tic)


def constructive_phase(
    distance_matrix: np.ndarray,
    alpha: float,
    start: int = 0
) -> List:    
    Tour = [start]
    
    for _ in range(distance_matrix.shape[0] - 1):
        min_index = get_maxmin_index_from_row(distance_matrix, Tour[-1], Tour, 'min')
        max_index = get_maxmin_index_from_row(distance_matrix, Tour[-1], Tour, 'max')
        
        f_min = distance_matrix[Tour[-1]][min_index]
        f_max = distance_matrix[Tour[-1]][max_index]
        
        # List of Restrict Candidates = LRC
        LRC_index = np.array(range(len(distance_matrix[Tour[-1]])))
        
        LRC_condition = distance_matrix[Tour[-1]] <= f_min + alpha*(f_max - f_min)
        LRC_condition[Tour[-1]] = False
        LRC_index = LRC_index[LRC_condition]
        
        new_city_index = np.random.choice(LRC_index, 1, replace=False)[0]
        Tour.append(new_city_index)

    return Tour


def get_maxmin_index_from_row(
    distance_matrix: np.ndarray,
    row: int,
    previous_indexes: List,
    type: str,
    )-> int:
    """Get the minimum/maximum element in the adjusted row array from a distance matrix.
    We adjust the row array in order to never get the "previous_indexes" list of indexes.
    """
    distance_matrix = distance_matrix.copy()
    arr = distance_matrix[row].astype(float)
    
    aux_list = range(arr.shape[0])
    aux_list_2 = []
    for i in aux_list:
        if i in previous_indexes:
            aux_list_2.append(True)
        else:
            aux_list_2.append(False)
    previous_indexes_bool = aux_list_2
    
    if type == 'max':
        arr[previous_indexes_bool] = -1
        target_index = np.argmax(arr)
    if type == 'min':
        arr[previous_indexes_bool] = np.Inf
        target_index = np.argmin(arr)
    
    return target_index


def setup(
    distance_matrix: np.ndarray, x0: Optional[List] = None
) -> Tuple[List[int], float]:
    """Return initial solution and its objective value

    Parameters
    ----------
    distance_matrix
        Distance matrix of shape (n x n) with the (i, j) entry indicating the
        distance from node i to j

    x0
        Permutation of nodes from 0 to n - 1 indicating the starting solution.
        If not provided, a random list is created.

    Returns
    -------
    x0
        Permutation with initial solution. If ``x0`` was provided, it is the
        same list

    fx0
        Objective value of x0
    """

    if not x0:
        n = distance_matrix.shape[0]  # number of nodes
        x0 = [0] + sample(range(1, n), n - 1)  # ensure 0 is the first node

    fx0 = compute_permutation_distance(x0, distance_matrix)
    return x0, fx0


if __name__ == '__main__':
    tsplib_file = "tests/test_data/a280.tsp"
    distance_matrix = tsplib_distance_matrix(tsplib_file)

    print(solve_tsp_grasp(distance_matrix))
    
    initial_tour = nn_algo(distance_matrix)[0]
    print(local_search_algo(initial_tour, distance_matrix, method='first improvement'))
    
    
        