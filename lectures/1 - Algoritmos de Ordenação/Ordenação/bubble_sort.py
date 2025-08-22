''' Ordena o vetor usando BubbleSort
Parâmetros:
array: vetor a ser ordenado
option: opção que define se a ordenação é crescente ou
decrescente
Esse algoritmo tem um comportamento assintótico O(N2) */
bubbleSort(array, option)
'''
def bubbleSort(array, opcao):
    menor = 0
    maior = 1
    ter_troca = True
    cont = len (array)

    if opcao == 2:
        #decrescente 
                    #a1 a2 a3
        while (ter_troca == True):
            ter_troca = False
            for i in range(cont - 1):
                if (array [menor] > array [maior]):
                    menor = menor + 1
                    maior = maior + 1
                else:
                    array [menor], array [maior] = array[maior], array[menor]
                    menor = menor + 1
                    maior = maior + 1
                    ter_troca = True
            cont = cont - 1
            menor = 0
            maior = 1
    
    if opcao == 1:
        #crescente 
        while (ter_troca == True):
            ter_troca = False
            for i in range(cont - 1):
                if (array [menor] < array [maior]):
                    menor = menor + 1
                    maior = maior + 1
                else:
                    array [menor], array [maior] = array[maior], array[menor]
                    menor = menor + 1
                    maior = maior + 1
                    ter_troca = True
            cont = cont - 1
            menor = 0
            maior = 1
    
    return array

# -------------------------------------------------------------------------------

vetor = [58,	-13,	66,	50,	-80,	77,	-97,	60,	-15,	-17] 
print (vetor)

escolha_user = input ("digite:\n1 - crescente\n2 - decrescente\n R:")
escolha_user = int(escolha_user)

newvetor = bubbleSort(vetor, escolha_user)
print (newvetor)