# sorts/heapsort.py

def heapify(arr, n, i, key, reverse):
    largest = i
    l = 2*i + 1
    r = 2*i + 2

    def cmp(a, b):
        return (a > b) if not reverse else (a < b)

    if l < n and cmp(key(arr[l]), key(arr[largest])):
        largest = l
    if r < n and cmp(key(arr[r]), key(arr[largest])):
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, key, reverse)

def heap_sort(items, key=lambda x: x, reverse=False):
    """Implementação que modifica uma cópia e retorna a lista ordenada."""
    arr = items[:]  # trabalha em cópia
    n = len(arr)
    # build heap
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i, key, reverse)
    # extract
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0, key, reverse)
    # se reverse True, a lógica de cmp inverte, então já sai na ordem pedida
    return arr

if __name__ == "__main__":
    print(heap_sort([4,1,7,3], key=lambda x: x))
