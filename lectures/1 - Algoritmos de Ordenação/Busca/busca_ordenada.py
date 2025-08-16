# Testa todas as posições até encontrar o elemento desejado, 
# ou até que o valor da posição testada seja maior do que o elemento, 
# ou até chegar ao final do vetor.
#
# Parâmetros:
#   array    -> vetor
#   elemento -> valor que se deseja procurar

def estaOrdenado(array):
    n = len(array)
    for i in range(n - 1):
        i_menor = i
        for j in range (i + 1, n):
            if array[j] < array[i_menor]:
                i_menor = j
        array[i], array[i_menor] = array[i_menor], array[i]
    return array

def buscaOrdenada(array, elemento):
    n  = len (array)
    for i in range(n - 1):
        if elemento == array[i]:
            return i
    return -1

# ----------------------------------------------------------------------

lista = [9, 7, 6, 8, 2, 4, 5, 1, 3]
print (lista)
estaOrdenado(lista)
print(lista)

elemento = int(input("digite o elemento = "))
print ("buscando elemento = ", elemento)
valor = buscaOrdenada(lista, elemento)

if valor == -1:
    print ("elemento não existe nessa lista")
else:
    print("elemento está na posição = ", valor)