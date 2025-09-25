#/* função principal */
def heapSort(array, option=1):
    heapsize = len(array)
    buildMaxHeap(array, option)
    # Para i de vetor.tamanho até 2, faça:
    for i in range(heapsize - 1, 0, -1):
        # "Remove" o maior elemento (primeira posição) trocando com o último
        array[0], array[i] = array[i], array[0]
        # Reduz o tamanho do heap e reconstroi o heap de máximo
        maxHeapify(array, 0, i, option)


#/* constrói heap de máximo ou mínimo a partir do vetor */
def buildMaxHeap(array, option):
    heapsize = len(array)
    # Começa do último nó pai até a raiz (índice 0)
    for i in range((heapsize // 2) - 1, -1, -1):
        maxHeapify(array, i, heapsize, option)


#/* reconstrói o heap, desconsiderando o elemento já ordenado */
def maxHeapify(array, i, heapsize, option):
    esquerda = 2 * i + 1
    direita = 2 * i + 2
    maior = i
    if option == 1:  # crescente (heap de máximo)
        if esquerda < heapsize and array[esquerda] > array[maior]:
            maior = esquerda
        if direita < heapsize and array[direita] > array[maior]:
            maior = direita
    elif option == 2:  # decrescente (heap de mínimo)
        if esquerda < heapsize and array[esquerda] < array[maior]:
            maior = esquerda
        if direita < heapsize and array[direita] < array[maior]:
            maior = direita
    if maior != i:
        array[i], array[maior] = array[maior], array[i]
        maxHeapify(array, maior, heapsize, option)

# -------------------------------------------------------------------------------

vetor = [58, -13, 66, 50, -80, 77, -97, 60, -15, -17]
print("Vetor original:", vetor)

escolha = int(input("Digite:\n1 - crescente\n2 - decrescente\nR: "))
heapSort(vetor, escolha)
print("Vetor ordenado:", vetor)