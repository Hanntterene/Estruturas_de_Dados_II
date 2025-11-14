# sorts/insertionsort.py

def insertion_sort(items, key=lambda x: x, reverse=False):
    arr = items[:]  # copia
    for i in range(1, len(arr)):
        current = arr[i]
        cur_key = key(current)
        j = i - 1
        if not reverse:
            while j >= 0 and key(arr[j]) > cur_key:
                arr[j+1] = arr[j]
                j -= 1
        else:
            while j >= 0 and key(arr[j]) < cur_key:
                arr[j+1] = arr[j]
                j -= 1
        arr[j+1] = current
    return arr

if __name__ == "__main__":
    print(insertion_sort([8,3,5,1], key=lambda x: x))
