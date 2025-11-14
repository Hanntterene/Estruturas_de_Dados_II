# sorts/mergesort.py

def merge_sort(items, key=lambda x: x, reverse=False):
    """Retorna nova lista ordenada (estável)."""
    if len(items) <= 1:
        return items[:]

    mid = len(items) // 2
    left = merge_sort(items[:mid], key=key, reverse=reverse)
    right = merge_sort(items[mid:], key=key, reverse=reverse)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a = key(left[i])
        b = key(right[j])
        if reverse:
            if a >= b:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        else:
            if a <= b:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
    # resto
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

if __name__ == "__main__":
    # teste rápido
    print(merge_sort([3,1,2], key=lambda x: x))
