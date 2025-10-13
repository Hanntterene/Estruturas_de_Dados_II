#  ------------------------------------- EXERCÍCIO 1 ------------------------------------------
def grep(caminho, termo):
    encontrados = []
    busca = termo.lower()
    try:
        with open(caminho, 'r') as arquivo:
            for linha in arquivo:
                registro = linha.rstrip('\n')
                if busca in registro.lower():
                    encontrados.append(registro)
    except FileNotFoundError:
        return []
    return encontrados


#  ------------------------------------- EXERCÍCIO 2 ------------------------------------------
def grep_indices(caminho, termo):
    encontrados = []
    busca = termo.lower()
    try:
        with open(caminho, 'r') as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                registro = linha.rstrip('\n')
                if busca in registro.lower():
                    encontrados.append((numero, registro))
    except FileNotFoundError:
        return []
    return encontrados

#  ------------------------------------- EXERCÍCIO 3 ------------------------------------------
def readRecordByRRN(caminho, rrn):
    if rrn < 0:
        return ""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            primeira = f.readline()  # cabeçalho
            for indice, linha in enumerate(f):
                if indice == rrn:
                    return linha.rstrip('\n')
    except FileNotFoundError:
        return ""
    return ""

caminho = r"C:\Projetos\Faculdade\Estruturas_de_Dados_II\lectures\2 - Estruturas de Dados em Disco\outputs de leitura\animes_tamanho_fixo.txt"

try:
    with open(caminho, 'r', encoding='utf-8'):
        pass
except FileNotFoundError:
    print(f"Arquivo não encontrado: {caminho}")
    raise SystemExit(1)

# interação simples
escolha = input("escolha exercício (1=grep,2=grep_indices,3=RRN): ").strip()

if escolha == "1":
    termo = input("Termo: ").strip()
    res = grep(caminho, termo)
    if not res:
        print("Termo não encontrado.")
    else:
        for r in sorted(res):
            print(r)

elif escolha == "2":
    termo = input("Termo: ").strip()
    res = grep_indices(caminho, termo)
    if not res:
        print("Termo não encontrado.")
    else:
        for numero, registro in res:
            print(f"{numero}: {registro}")

elif escolha == "3":
    try:
        rrn = int(input("Informe RRN (0 = primeiro registro): ").strip())
    except ValueError:
        print("RRN inválido.")
    else:
        registro = readRecordByRRN(caminho, rrn)
        if registro:
            print(registro)
        else:
            print("Registro não encontrado.")

else:
    print("Opção inválida.")

