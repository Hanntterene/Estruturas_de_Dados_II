''' Utiliza a divisão e conquista. Testa sempre o elemento na metade
do intervalo válido.
Parametros:
 array é o vetor
 elemento é o elemento que se deseja procurar
*/
/* Retorna a posição do elemento ou -1 caso não encontre 
'''
def buscaBinaria(array, elemento):
    n = 0

def estaOrdenado(array):
    n = len(array)
    for i in range(n - 1):
        i_menor = i
        for j in range (i + 1, n):
            if array[j] < array[i_menor]:
                i_menor = j
        array[i], array[i_menor] = array[i_menor], array[i]
    return array

# ----------------------------------------------------------------------

lista = [9, 7, 6, 8, 2, 4, 5, 1, 3]
print (lista)

print("----------LISTA ORDENADA---------")
estaOrdenado(lista)
print(lista)

print("---------------------------------")

elemento = int(input("digite o elemento = "))
print ("buscando elemento = ", elemento)
buscaBinaria()