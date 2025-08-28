'''
/* Ordena o vetor usando Selection Sort
Parâmetros:
 array: vetor a ser ordenado
 option: 1 - ordenação crescente, 2 - ordenação decrescente
Esse algoritmo tem um comportamento assintótico O(N2) */
'''

def selectionSort(array, opção):
    if opção == 1:
        menor = 0       
        #crescente
        for i in range (len (array)):
            menor = i
            for j in range (i, len (array)):
                if array[j] < array[menor]:
                    menor = j
            array[i], array[menor] = array [menor], array[i]
    else:
        maior = 0       
        #decrescente
        for i in range (len (array)):
            maior = i
            for j in range (i, len (array)):
                if array[j] > array[maior]:
                    maior = j
            array[i], array[maior] = array [maior], array[i]

    return array

#----------------------------------------------------------------------------

vetor = [58,	-13,	66,	50,	-80,	77,	-97,	60,	-15,	-17] 
print (vetor)


escolha_user = input ("digite:\n1 - crescente\n2 - decrescente\n R:")
escolha_user = int(escolha_user)

newvetor = selectionSort(vetor, escolha_user)
print (newvetor)
            

        