'''
/* Ordena o vetor usando Merge Sort
Parâmetros:
 array: vetor a ser ordenado
 option: 1 - ordenação crescente, 2 - ordenação decrescente
Esse algoritmo tem um comportamento assintótico O(N log N) */
'''

def mergeSort(array, inicio, fim, option):

    if inicio < fim:
        meio = (inicio + fim) // 2

        #chamada para subproblemas
        mergeSort(array, inicio, meio, option)
        mergeSort(array, meio+1, fim, option)

        # função para combinar os problemas
        Merge(array, inicio, meio, fim, option)

def Merge (array, inicio, meio, fim, option):
    aux = []
    p1 = inicio
    p2 = meio + 1

    while p1 <= meio and p2 <= fim:
        if option == 1:  # crescente
            if array[p1] <= array[p2]:
                aux.append(array[p1])
                p1 += 1
            else:
                aux.append(array[p2])
                p2 += 1
        elif option == 2:  # decrescente
            if array[p1] >= array[p2]:
                aux.append(array[p1])
                p1 += 1
            else:
                aux.append(array[p2])
                p2 += 1

    # Ao final do laço, sobrarão elementos apenas no subproblema da direita ou esquerda
    while p1 <= meio:
        aux.append(array[p1])
        p1 += 1
    while p2 <= fim:
        aux.append(array[p2])
        p2 += 1

    # Copiar o vetor auxiliar de volta para o original
    for i in range(len(aux)):
        array[inicio + i] = aux[i]
        

vetor = [58, -13, 66, 50, -80, 77, -97, 60, -15, -17]
print("Vetor original:", vetor)

escolha_user = int(input("digite:\n1 - crescente\n2 - decrescente\nR: "))
mergeSort(vetor, 0, len(vetor) - 1, escolha_user)
print("Vetor ordenado:", vetor)