"""
An empty python package.

Examples
--------
>>> from prototype_python_library import fib
>>> fib(0)
0
"""

__version__ = "0.7.0"


def fib(n: int) -> int:
    """Compute an element in the fibonacci sequence.

    Args:
        n (int): the position in the sequence.

    Returns:
        The nth element in the fibonacci sequence.
    """
    if n == 0:
        return 0

    if n == 1:
        return 1

    return fib(n - 1) + fib(n - 2)
