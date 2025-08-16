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

def buscaOrdenada(array, elemento, tempo):
    n  = len (array)
    for i in range(n - 1):
        tempo = tempo + 1
        if elemento == array[i]:
            valor = i
            return valor, tempo
    valor = -1
    return valor, tempo

# ----------------------------------------------------------------------

lista = [9, 7, 6, 8, 2, 4, 5, 1, 3]
print (lista)

elemento = int(input("digite o elemento = "))
print ("buscando elemento = ", elemento)

print("----------LISTA NÃO ORDENADA---------")
valor, tempo = buscaOrdenada(lista, elemento, tempo = 0)

if valor == -1:
    print ("elemento não existe nessa lista", 
           "tempo de busca = ", tempo)
else:
    print("elemento está na posição = ", valor, "\ntempo de busca = ", tempo)

print("------------LISTA ORDENADA-----------")
estaOrdenado(lista)
print(lista)
tempo = 0

valor, tempo = buscaOrdenada(lista, elemento, tempo = 0)

if valor == -1:
    print ("elemento não existe nessa lista", 
           "tempo de busca = ", tempo)
else:
    print("elemento está na posição = ", valor, "\ntempo de busca = ", tempo)