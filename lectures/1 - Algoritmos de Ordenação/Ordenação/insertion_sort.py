'''/* Ordena o vetor usando Insertion Sort
Parâmetros:
 array: vetor a ser ordenado
 option: 1 - ordenação crescente, 2 - ordenação decrescente
Esse algoritmo tem um comportamento assintótico O(N2) */
    '''

def insertion_sort(array, option=1):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        if option == 1:  # crescente
            while j >= 0 and array[j] > key:
                array[j + 1] = array[j]
                j -= 1
        elif option == 2:  # decrescente
            while j >= 0 and array[j] < key:
                array[j + 1] = array[j]
                j -= 1
        array[j + 1] = key
    return array
# -------------------------------------------------------------------------------

vetor = [58,-13,66,	50,	-80,77,	-97,60,	-15,-17] 
print (vetor)

escolha_user = input ("digite:\n1 - crescente\n2 - decrescente\n R:")
escolha_user = int(escolha_user)

newvetor = insertion_sort(vetor, escolha_user)
print (newvetor)