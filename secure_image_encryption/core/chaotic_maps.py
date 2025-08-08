"""
Chaotic map implementations for secure image encryption.
"""

import numpy as np

def ikeda_map(x: float, y: float, u: float = 0.918) -> tuple[float, float]:
    """
    Ikeda map implementation.
    
    Args:
        x: x-coordinate
        y: y-coordinate
        u: Parameter controlling the map's behavior
        
    Returns:
        Tuple of (x1, y1) - the next point in the map
    """
    t = 0.4 - 6 / (1 + x**2 + y**2)
    x1 = 1 + u * (x * np.cos(t) - y * np.sin(t))
    y1 = u * (x * np.sin(t) + y * np.cos(t))
    return x1 % 1, y1 % 1

def circle_map(x: float, k: float = 0.5) -> float:
    """
    Circle map implementation.
    
    Args:
        x: Input value
        k: Parameter controlling the map's behavior
        
    Returns:
        Next value in the map
    """
    return (x + k - (0.5 / (2 * np.pi)) * np.sin(2 * np.pi * x)) % 1

def logistic_map(x: float, r: float = 3.99) -> float:
    """
    Logistic map implementation.
    
    Args:
        x: Input value (0 < x < 1)
        r: Growth rate parameter
        
    Returns:
        Next value in the map
    """
    return r * x * (1 - x)

def generate_chaotic_matrix(height: int, width: int, seed: float) -> np.ndarray:
    """
    Generate a chaotic matrix using a combination of chaotic maps.
    
    Args:
        height: Height of the matrix
        width: Width of the matrix
        seed: Seed value for the chaotic maps
        
    Returns:
        2D numpy array of chaotic values
    """
    # Initialize matrix
    matrix = np.zeros((height, width))
    x, y = 0.1, 0.1  # Initial values
    
    # Generate chaotic sequence
    for i in range(height):
        for j in range(width):
            # Use logistic map to update x
            x = logistic_map(x + seed)
            # Use circle map to update y
            y = circle_map(y + x)
            # Use ikeda map to get final value
            x, y = ikeda_map(x, y)
            matrix[i, j] = (x + y) % 1
    
    return matrix
