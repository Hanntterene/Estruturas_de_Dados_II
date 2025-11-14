
def quick_sort(items, key=lambda x: x, reverse=False):
    """Retorna nova lista; não-in-place, simples e legível."""
    if len(items) <= 1:
        return items[:]

    pivot = key(items[len(items)//2])
    less, equal, greater = [], [], []
    for it in items:
        k = key(it)
        if k == pivot:
            equal.append(it)
        elif (k < pivot and not reverse) or (k > pivot and reverse):
            less.append(it)
        else:
            greater.append(it)

    # recursão: menos, equal, greater
    if reverse:
        # se reverse, keep direction swapped to keep stable-ish behavior
        return quick_sort(greater, key=key, reverse=reverse) + equal + quick_sort(less, key=key, reverse=reverse)
    else:
        return quick_sort(less, key=key, reverse=reverse) + equal + quick_sort(greater, key=key, reverse=reverse)

if __name__ == "__main__":
    print(quick_sort([5,2,9,1], key=lambda x: x))

def merge_sort(items, key=lambda x: x, reverse=False):
    """Retorna nova lista ordenada (estável)."""
    if len(items) <= 1:
        return items[:]

    mid = len(items) // 2
    left = merge_sort(items[:mid], key=key, reverse=reverse)
    right = merge_sort(items[mid:], key=key, reverse=reverse)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a = key(left[i])
        b = key(right[j])
        if reverse:
            if a >= b:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        else:
            if a <= b:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
    # resto
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

if __name__ == "__main__":
    # teste rápido
    print(merge_sort([3,1,2], key=lambda x: x))


def insertion_sort(items, key=lambda x: x, reverse=False):
    arr = items[:]  # copia
    for i in range(1, len(arr)):
        current = arr[i]
        cur_key = key(current)
        j = i - 1
        if not reverse:
            while j >= 0 and key(arr[j]) > cur_key:
                arr[j+1] = arr[j]
                j -= 1
        else:
            while j >= 0 and key(arr[j]) < cur_key:
                arr[j+1] = arr[j]
                j -= 1
        arr[j+1] = current
    return arr

if __name__ == "__main__":
    print(insertion_sort([8,3,5,1], key=lambda x: x))

def heapify(arr, n, i, key, reverse):
    largest = i
    l = 2*i + 1
    r = 2*i + 2

    def cmp(a, b):
        return (a > b) if not reverse else (a < b)

    if l < n and cmp(key(arr[l]), key(arr[largest])):
        largest = l
    if r < n and cmp(key(arr[r]), key(arr[largest])):
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, key, reverse)

def heap_sort(items, key=lambda x: x, reverse=False):
    """Implementação que modifica uma cópia e retorna a lista ordenada."""
    arr = items[:]  # trabalha em cópia
    n = len(arr)
    # build heap
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i, key, reverse)
    # extract
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0, key, reverse)
    # se reverse True, a lógica de cmp inverte, então já sai na ordem pedida
    return arr

if __name__ == "__main__":
    print(heap_sort([4,1,7,3], key=lambda x: x))


MAP_ORDENACAO = {
    'Q': quick_sort,
    'M': merge_sort,
    'H': heap_sort,
    'I': insertion_sort
}

PADDING_CHAR = ' '

class Heroi:
    def __init__(self, valores, cabecalhos):
        for h, v in zip(cabecalhos, valores):
            nome = h.strip().replace(' ', '_')
            setattr(self, nome, v.strip())
    def para_lista(self, cabecalhos):
        return [getattr(self, h.strip().replace(' ', '_')) for h in cabecalhos]

def inferir_valor_chave(v):
    if v is None:
        return ''
    vs = v.strip()
    try:
        return int(vs)
    except:
        try:
            return float(vs)
        except:
            return vs.lower()

# helper: imprime e grava mensagem de erro no arquivo de saída (se fornecido)
def _reportar_erro(mensagem, caminho_saida=None):
    print(mensagem)
    if caminho_saida:
        try:
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(mensagem + '\n')
        except Exception:
            pass

def main():
    if len(sys.argv) != 3:
        print("Uso: python ED2-AT02-Keysorting-LohannaMonteiro.py CasosdeTeste/entrada.txt saida.txt")
        return

    entrada, saida = sys.argv[1], sys.argv[2]

    if not os.path.exists(entrada):
        _reportar_erro(f"Arquivo de entrada '{entrada}' não encontrado.", saida)
        return

    with open(entrada, 'r', encoding='utf-8') as f:
        linhas = [l.rstrip('\n') for l in f]

    if len(linhas) < 2:
        _reportar_erro("Arquivo de entrada inválido: menos de 2 linhas.", saida)
        return

    # ler e validar meta (SORT / ORDER) na primeira linha
    meta = linhas[0].upper()
    m_sort = re.search(r"SORT\s*=\s*([QMHI])", meta)
    m_order = re.search(r"ORDER\s*=\s*([CD])", meta)
    if not m_sort or not m_order:
        erro = "Meta inválida na primeira linha. Deve conter 'SORT=[Q/M/H/I]' e 'ORDER=[C/D]'."
        _reportar_erro(erro, saida)
        return
    metodo = m_sort.group(1)
    ordem = m_order.group(1)

    if metodo not in MAP_ORDENACAO:
        _reportar_erro(f"SORT inválido: {metodo}. Deve ser Q, M, H ou I.", saida)
        return
    if ordem not in ('C', 'D'):
        _reportar_erro(f"ORDER inválido: {ordem}. Deve ser C ou D.", saida)
        return

    # leitura dos cabeçalhos e registros (linha 2 = cabeçalhos)
    linha_cab = linhas[1]
    cabecalhos = linha_cab.split(',') if ',' in linha_cab and '|' not in linha_cab else linha_cab.split('|')
    registros = []
    for linha in linhas[2:]:
        if linha.strip():
            valores = linha.split('|') if '|' in linha else linha.split(',')
            if len(valores) < len(cabecalhos):
                valores += [''] * (len(cabecalhos) - len(valores))
            registros.append(Heroi(valores, cabecalhos))

    if not registros:
        _reportar_erro("Nenhum registro encontrado no arquivo.", saida)
        return

    # escolher campo chave: obrigatoriamente 'key'
    campo_chave = None
    for h in cabecalhos:
        if h.strip().lower() == 'key':
            campo_chave = h.strip()
            break
    if not campo_chave:
        _reportar_erro("Erro: arquivo deve conter a coluna 'key' no cabeçalho para ordenar.", saida)
        return

    def func_chave(h):
        raw = getattr(h, campo_chave.replace(' ', '_'))
        return inferir_valor_chave(raw)

    reverso = (ordem == 'D')

    sorter = MAP_ORDENACAO[metodo]
    try:
        ordenados = sorter(registros, key=func_chave, reverse=reverso)
    except TypeError:
        ordenados = sorter(registros, key=func_chave)
        if reverso:
            ordenados = list(reversed(ordenados))

    # montar linhas de dados (pipe-separated) e aplicar padding para tamanho fixo
    linhas_dados = ['|'.join(h.para_lista(cabecalhos)) for h in ordenados]
    tamanho_registro = max((len(s) for s in linhas_dados), default=0)
    # padding
    linhas_padded = [s.ljust(tamanho_registro, PADDING_CHAR) for s in linhas_dados]

    # gravar saída: header com TAMANHO_REGISTRO e LIVRE:-1, depois cabeçalhos e registros padded
    with open(saida, 'w', encoding='utf-8') as f:
        f.write(f"TAMANHO_REGISTRO:{tamanho_registro}|LIVRE:-1\n")
        f.write('|'.join([h.strip() for h in cabecalhos]) + '\n')
        for ln in linhas_padded:
            f.write(ln + '\n')

    print(f"Ordenação concluída usando {metodo} ({'decrescente' if reverso else 'crescente'}). Saída: {saida}")

if __name__ == "__main__":
    main()
