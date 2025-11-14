# sorts/quicksort.py

def quick_sort(items, key=lambda x: x, reverse=False):
    """Retorna nova lista; não-in-place, simples e legível."""
    if len(items) <= 1:
        return items[:]

    pivot = key(items[len(items)//2])
    less, equal, greater = [], [], []
    for it in items:
        k = key(it)
        if k == pivot:
            equal.append(it)
        elif (k < pivot and not reverse) or (k > pivot and reverse):
            less.append(it)
        else:
            greater.append(it)

    # recursão: menos, equal, greater
    if reverse:
        # se reverse, keep direction swapped to keep stable-ish behavior
        return quick_sort(greater, key=key, reverse=reverse) + equal + quick_sort(less, key=key, reverse=reverse)
    else:
        return quick_sort(less, key=key, reverse=reverse) + equal + quick_sort(greater, key=key, reverse=reverse)

if __name__ == "__main__":
    print(quick_sort([5,2,9,1], key=lambda x: x))
