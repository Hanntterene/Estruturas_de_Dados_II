"""
    Testa todas as posições até encontrar o elemento desejado
    ou até chegar ao final do vetor.

    Parâmetros:
        array    -> vetor
        elemento -> valor que se deseja procurar

    Retorna a posição do elemento ou -1 caso não encontre.
"""

def buscaLinear(array, elemento, tempo):
    n  = len (array)
    for i in range(n - 1):
        tempo = tempo + 1
        if elemento == array[i]:
            valor = i
            return valor, tempo
    valor = -1
    return valor, tempo

lista = [9, 7, 6, 8, 2, 4, 5, 1, 3]
print (lista)

elemento = int(input("digite o elemento = "))
print ("buscando elemento = ", elemento)

print("----------LISTA NÃO ORDENADA---------")
valor, tempo = buscaLinear(lista, elemento, tempo = 0)

if valor == -1:
    print ("elemento não existe nessa lista", 
           "tempo de busca = ", tempo)
else:
    print("elemento está na posição = ", valor, "\ntempo de busca = ", tempo)
    