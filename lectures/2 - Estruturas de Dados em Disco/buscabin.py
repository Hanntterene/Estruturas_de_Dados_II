
import re

def lerLinhas(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return [ln.rstrip('\n') for ln in f.readlines()]
    except FileNotFoundError:
        return []

def lerRegistroComRRN(arquivo, rrn):
    linhas = lerLinhas(arquivo)
    if not linhas:
        return None

    inicio = 0
    if linhas[0].startswith('TAMANHO_REGISTRO:'):
        inicio = 1
    if inicio < len(linhas) and linhas[inicio].startswith('DELIM_CAMPO:'):
        inicio += 1

    # detecta linha de nomes de colunas (opcional) e ajusta data_start
    data_start = inicio
    if data_start < len(linhas) and '|' in linhas[data_start]:
        first_field = linhas[data_start].split('|', 1)[0].strip()
        if any(c.isalpha() for c in first_field) and not first_field.isdigit():
            data_start += 1

    try:
        idx = data_start + int(rrn)
    except Exception:
        return None

    if idx < data_start or idx >= len(linhas):
        return None

    linha = linhas[idx].rstrip()
    if not linha or linha.startswith('*'):
        return None

    campos = linha.split('|')
    rec = type('Record', (), {})()
    rec.chave = campos[0].strip()
    rec.fields = campos
    return rec

def numeroRegistros(arquivo):
    linhas = lerLinhas(arquivo)
    if not linhas:
        return 0

    inicio = 0
    if linhas[0].startswith('TAMANHO_REGISTRO:'):
        inicio = 1
    if inicio < len(linhas) and linhas[inicio].startswith('DELIM_CAMPO:'):
        inicio += 1
    return sum(1 for l in linhas[inicio:] if l.strip() != '')

def buscaBinaria(arquivo, chave):
    chave_norm = chave.strip().lower()
    inicio = 0
    fim = numeroRegistros(arquivo) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        registro_lido = lerRegistroComRRN(arquivo, meio)

        # se registro central estiver apagado, procurar próximo não-apagado
        if registro_lido is None:
            esq_meio = meio - 1
            dir_meio = meio + 1
            encontrado = None
            while esq_meio >= inicio or dir_meio <= fim:
                if esq_meio >= inicio:
                    registro_esq = lerRegistroComRRN(arquivo, esq_meio)
                    if registro_esq:
                        encontrado = (registro_esq, esq_meio)
                        break
                    esq_meio -= 1
                if dir_meio <= fim:
                    registro_dir = lerRegistroComRRN(arquivo, dir_meio)
                    if registro_dir:
                        encontrado = (registro_dir, dir_meio)
                        break
                    dir_meio += 1
            if not encontrado:
                return False, None, None
            registro_lido, meio = encontrado

        if registro_lido.chave.lower() == chave_norm:
            return True, registro_lido, meio
        if registro_lido.chave.lower() < chave_norm:
            inicio = meio + 1
        else:
            fim = meio - 1

    return False, None, None


caminho = r"C:\Projetos\Faculdade\Estruturas_de_Dados_II\lectures\2 - Estruturas de Dados em Disco\testebusc_bin.txt"

ok, rec, rrn = buscaBinaria(caminho, "Naruto")
print(ok, rrn, rec.chave if rec else None)

ok, rec, rrn = buscaBinaria(caminho, "Myself; Yourself")
print(ok, rrn, rec)