# settings.py
from itertools import islice
from typing import List

WIDTH, HEIGHT = 450, 450
N_CELLS = 9
CELL_SIZE = (WIDTH // N_CELLS, HEIGHT // N_CELLS)

def convert_list(lst: List[int], row_lengths: List[int]) -> List[List[int]]:
    it = iter(lst)
    return [list(islice(it, length)) for length in row_lengths]
