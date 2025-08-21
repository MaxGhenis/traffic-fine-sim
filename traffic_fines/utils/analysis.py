"""Analysis utilities for welfare and distributional metrics."""

import numpy as np
from typing import List, Tuple


def calculate_gini(values: np.ndarray) -> float:
    """
    Calculate Gini coefficient for a distribution.
    
    Parameters
    ----------
    values : np.ndarray
        Array of values (e.g., incomes, utilities)
        
    Returns
    -------
    float
        Gini coefficient (0 = perfect equality, 1 = perfect inequality)
    """
    # Sort values
    sorted_values = np.sort(values)
    n = len(values)
    
    # Calculate Gini using the formula
    cumsum = np.cumsum(sorted_values)
    gini = (2 * np.sum((i + 1) * v for i, v in enumerate(sorted_values))) / (n * cumsum[-1]) - (n + 1) / n
    
    return gini


def calculate_lorenz_curve(values: np.ndarray, n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate Lorenz curve coordinates.
    
    Parameters
    ----------
    values : np.ndarray
        Array of values (e.g., incomes)
    n_points : int
        Number of points for the curve
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        (x_coords, y_coords) for Lorenz curve
    """
    sorted_values = np.sort(values)
    cumsum = np.cumsum(sorted_values)
    total = cumsum[-1]
    
    x = np.linspace(0, 1, n_points)
    y = np.zeros(n_points)
    
    for i, xi in enumerate(x):
        idx = int(xi * len(sorted_values))
        if idx == 0:
            y[i] = 0
        else:
            y[i] = cumsum[idx - 1] / total
    
    return x, y