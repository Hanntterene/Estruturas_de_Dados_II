# sorts/__init__.py
from .mergesort import merge_sort
from .quicksort import quick_sort
from .heapsort import heap_sort
from .insertionsort import insertion_sort

__all__ = ["merge_sort", "quick_sort", "heap_sort", "insertion_sort"]
