import pandas as pd
import numpy as np
import tsplib95

def distance(a, b):
    """Euclidean distance of two points.

    Args:
        a (numpy.array or pd.Series)
        b (numpy.array or pd.Series)

    Returns:
        [float]
    """
    return np.sqrt(np.sum(np.power((a-b), 2)))

def get_dist_matrix(path):
    """Given a csv of rows each containing
    index, x, y coordinates, return the distance matrix,
    for the group of points.
    """
    df = pd.read_csv(path,
                     sep=' ',
                     names=['x', 'y'])
    
    full_matrix = []
    for i in df.index:
        vec_distance = []
        for j in df.index:
            vec_distance.append(distance(df.iloc[i,].to_numpy(),
                                    df.iloc[j,].to_numpy()))
        vec_distance = np.array(vec_distance)
        full_matrix.append(vec_distance)
    full_matrix = np.array(full_matrix)
    return full_matrix

def tsplib_distance_matrix(tsplib_file: str) -> np.ndarray:
    """Distance matrix from a TSPLIB file
    Parameters
    ----------
    tsplib_file
        A string with the complete path of the TSPLIB file (or just its name if
        it is the in current path)
    Returns
    -------
    distance_matrix
        A ND-array with the equivalent distance matrix of the input file
    Notes
    -----
    This function can handle any file supported by the `tsplib95` lib.
    """

    tsp_problem = tsplib95.load(tsplib_file)
    distance_matrix_flattened = np.array([
        tsp_problem.get_weight(*edge) for edge in tsp_problem.get_edges()
    ])
    distance_matrix = np.reshape(
        distance_matrix_flattened,
        (tsp_problem.dimension, tsp_problem.dimension),
    )

    # Some problems with EXPLICIT matrix have a large number in the distance
    # from a node to itself, which makes no sense for our problems. Thus,
    # always ensure a diagonal filled with zeros
    np.fill_diagonal(distance_matrix, 0)
    return distance_matrix