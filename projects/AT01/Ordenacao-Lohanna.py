

import sys
import random
import time

def bubble_sort(array):
    n = len(array)
    comparacoes = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            comparacoes += 1
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return comparacoes

def insertion_sort(array):
    n = len(array)
    comparacoes = 0
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if array[j] > key:
                array[j + 1] = array[j]
                j -= 1
            else:
                break
        array[j + 1] = key
    return comparacoes

def selection_sort(array):
    n = len(array)
    comparacoes = 0
    for i in range(n):
        idx = i
        for j in range(i + 1, n):
            comparacoes += 1
            if array[j] < array[idx]:
                idx = j
        array[i], array[idx] = array[idx], array[i]
    return comparacoes

def merge_sort(array):
    comparacoes = [0]
    def merge(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            comparacoes[0] += 1
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    def merge_sort_rec(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort_rec(arr, l, m)
            merge_sort_rec(arr, m + 1, r)
            merge(arr, l, m, r)
    merge_sort_rec(array, 0, len(array) - 1)
    return comparacoes[0]

def quick_sort(array):
    comparacoes = [0]
    def partition(arr, low, high):
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            comparacoes[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    def quick_sort_rec(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_rec(arr, low, pi - 1)
            quick_sort_rec(arr, pi + 1, high)
    quick_sort_rec(array, 0, len(array) - 1)
    return comparacoes[0]

def heap_sort(array):
    comparacoes = [0]
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n:
            comparacoes[0] += 1
            if arr[l] > arr[largest]:
                largest = l
        if r < n:
            comparacoes[0] += 1
            if arr[r] > arr[largest]:
                largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    n = len(array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(array, n, i)
    for i in range(n - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        heapify(array, i, 0)
    return comparacoes[0]

def cocktail_sort(array):
    n = len(array)
    comparacoes = 0
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            comparacoes += 1
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            comparacoes += 1
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
        start += 1
    return comparacoes

algoritmos = [
    ("Insertion Sort", insertion_sort),
    ("Selection Sort", selection_sort),
    ("Bubble Sort", bubble_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
    ("Heap Sort", heap_sort),
    ("Cocktail Sort", cocktail_sort)
]

if len(sys.argv) != 3:
    print("Uso correto: python Ordenacao-Lohanna.py <entrada.txt> <saida.txt>")
    sys.exit(1)

entrada_path = sys.argv[1]
saida_path = sys.argv[2]

try:
    with open(entrada_path, 'r', encoding='utf-8') as f:
        linhas = [linha.strip().lower() for linha in f.readlines() if linha.strip()]
        if len(linhas) < 2:
            raise ValueError("Arquivo deve conter pelo menos duas linhas (tamanho e gerador).")
        tamanho_str = ''.join(filter(str.isdigit, linhas[0]))
        if not tamanho_str:
            raise ValueError("O valor do tamanho não contém nenhum dígito.")
        tamanho = int(tamanho_str)
        if tamanho <= 0:
            raise ValueError("O valor do tamanho deve ser um número inteiro maior que zero.")
        gerador = None
        for letra in linhas[1]:
            if letra in ('r', 'c', 'd'):
                gerador = letra
                break
        if not gerador:
            raise ValueError("O gerador deve conter pelo menos uma letra válida: 'r', 'c' ou 'd'.")
        if gerador == 'c':
            vetor = list(range(1, tamanho + 1))
        elif gerador == 'd':
            vetor = list(range(tamanho, 0, -1))
        elif gerador == 'r':
            vetor = [random.randint(0, 32000) for _ in range(tamanho)]
        else:
            raise ValueError("Modo de geração inválido.")

    print(f"Vetor gerado com {tamanho} elementos. Executando algoritmos...")

    resultados = []
    for nome, func in algoritmos:
        print(f"  {nome}: executando...")
        vetor_copia = vetor.copy()
        inicio = time.perf_counter()
        comparacoes = func(vetor_copia)
        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000
        vetor_str = ' '.join(str(x) for x in vetor_copia)
        linha = (
            f"{nome}; "
            f"{vetor_str}; "
            f"{comparacoes} comparações; "
            f"{tempo_ms:.3f} ms\n"
        )
        resultados.append((nome, tempo_ms, comparacoes, linha))

    menor_tempo = min(r[1] for r in resultados)
    algoritmos_mais_rapidos = [r[0] for r in resultados if abs(r[1] - menor_tempo) < 1e-6]
    menor_comparacoes = min(r[2] for r in resultados)
    algoritmos_menos_comparacoes = [r[0] for r in resultados if r[2] == menor_comparacoes]

    with open(saida_path, "w", encoding="utf-8") as saida:
        for _, _, _, linha in resultados:
            saida.write(linha)
        if len(algoritmos_mais_rapidos) == 1:
            saida.write(f"\nAlgoritmo mais rápido: {algoritmos_mais_rapidos[0]}\n")
            print(f"Mais rápido: {algoritmos_mais_rapidos[0]}")
        else:
            saida.write(f"\nAlgoritmos mais rápidos: {', '.join(algoritmos_mais_rapidos)}\n")
            print(f"Mais rápidos: {', '.join(algoritmos_mais_rapidos)}")
        if len(algoritmos_menos_comparacoes) == 1:
            saida.write(f"Algoritmo com menos comparações: {algoritmos_menos_comparacoes[0]}\n")
            print(f"Menos comparações: {algoritmos_menos_comparacoes[0]}")
        else:
            saida.write(f"Algoritmos com menos comparações: {', '.join(algoritmos_menos_comparacoes)}\n")
            print(f"Menos comparações: {', '.join(algoritmos_menos_comparacoes)}")

except Exception as e:
    print(f"Erro ao processar '{entrada_path}': {str(e)}")
    with open(saida_path, "w", encoding="utf-8") as saida:
        saida.write(f"Arquivo '{entrada_path}' inválido: {str(e)}\n")