import pytest
import pkg_resources
from Heisler import Heisler as hs

problem = hs("W", "lE", verbose=0)

def test_function_1():
    a, b = problem.calculator(1, 1, 1, 1, 1, verbose=0)
    assert a == 1
def test_function_2():
    r = problem.show_plot()
    assert "Internal_Energy_Wall"
