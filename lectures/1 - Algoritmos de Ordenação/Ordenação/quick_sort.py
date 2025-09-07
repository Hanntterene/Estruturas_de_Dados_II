'''
/* Ordena o vetor usando Quick Sort
Parâmetros:
 array: vetor a ser ordenado
 option: 1 - ordenação crescente, 2 - ordenação decrescente
Esse algoritmo tem um comportamento assintótico O(N log N) */
'''
def quickSort(array, inicio, fim, opcao):
        if inicio < fim:
            pivo = Particiona(array, inicio, fim, opcao)

            quickSort (array, inicio, pivo - 1)   # subproblema esquerda
            quickSort (array, pivo + 1, fim)      # subproblema direita   
        return array

def Particiona (array, inicio, fim):
        esq = inicio
        dirt = fim
        pivo = array[inicio]
        
        # procurar elementos para trocar de posição
        while (esq < dirt):
               # procurar do inicio ao fim elementos > que o pivo
            while (esq <= fim) and (array[esq] <= pivo):
                  esq = esq + 1
               # procurar do fim ao inicio elementos < que o pivo
            while (dirt >= inicio) and (array[dirt] >= pivo):
                  dirt = dirt - 1
                # se dois vetores forem encontrados troca a posição deles
            if esq < dirt:
                  array[esq], array[dirt] = array[dirt], array[esq]
        array[dirt], array [inicio] = array[inicio], array [dirt]
        return dirt
                          

# -------------------------------------------------------------------------------

vetor = [58,-13,66,	50,	-80,77,	-97,60,	-15,-17] 
print (vetor)

escolha_user = input ("digite:\n1 - crescente\n2 - decrescente\n R:")
escolha_user = int(escolha_user)

newvetor = quickSort(vetor, 0, len(vetor)-1, escolha_user)
print (newvetor)