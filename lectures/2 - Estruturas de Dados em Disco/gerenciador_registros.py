# Gerenciador de registros: remoção, compactação e reuso (arquivo de dados delimitados)

import os
import tempfile
import re

PADDING_CHAR = ' '
TOMBSTONE = '*'

def _read_lines(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return [l.rstrip('\n') for l in f.readlines()]
    except FileNotFoundError:
        return None

def _atomic_write(path, lines):
    dirn = os.path.dirname(path) or '.'
    fd, tmp = tempfile.mkstemp(dir=dirn, text=True)
    os.close(fd)
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            for l in lines:
                f.write(l + '\n')
        os.replace(tmp, path)
        return True
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass

def _pad_record(s, size):
    if size is None or size == 0:
        return s
    if len(s) > size:
        return s[:size]
    return s + (PADDING_CHAR * (size - len(s)))

def _parse_header(line):
    tamanho = None
    head = -1
    if not line:
        return tamanho, head
    parts = line.split('|')
    if parts:
        if parts[0].startswith('TAMANHO_REGISTRO:'):
            try:
                tamanho = int(parts[0].split(':',1)[1])
            except Exception:
                tamanho = None
    for p in parts[1:]:
        if p.startswith('LIVRE:'):
            try:
                head = int(p.split(':',1)[1])
            except Exception:
                head = -1
    return tamanho, head

def _make_header(tamanho, head):
    return f"TAMANHO_REGISTRO:{tamanho}|LIVRE:{head}"

def removeRegistro(arquivo, chave):
    linhas = _read_lines(arquivo)
    if linhas is None or not linhas:
        return False

    inicio = 0
    tamanho_reg, head = None, -1
    if linhas[0].startswith('TAMANHO_REGISTRO:'):
        inicio = 1
        tamanho_reg, head = _parse_header(linhas[0])

    novas = linhas.copy()
    removidos = 0
    chave_norm = chave.strip().lower()

    for i in range(inicio, len(linhas)):
        linha = linhas[i]
        if not linha:
            continue

        if linha.startswith(TOMBSTONE):
            conteudo_sem = linha[1:]
            already_deleted = True
        else:
            conteudo_sem = linha
            already_deleted = False

        conteudo_sem = conteudo_sem.rstrip(PADDING_CHAR).strip()

        campo0 = conteudo_sem.split('|', 1)[0].strip().lower() if conteudo_sem else ''
        if chave_norm == campo0:
            if already_deleted:
                continue
            rrn_atual = i - inicio
            resto = linha[1:] if len(linha) > 1 else ''
            marca = TOMBSTONE + str(head) + resto
            if tamanho_reg:
                marca = _pad_record(marca, tamanho_reg)
            novas[i] = marca
            head = rrn_atual
            removidos += 1

    if removidos == 0:
        return False

    tamanho_reg = tamanho_reg or 0
    linhas_a_escrever = [ _make_header(tamanho_reg, head) ] + novas[inicio:]
    return _atomic_write(arquivo, linhas_a_escrever)

def compactacaoDados(arquivo):
    linhas = _read_lines(arquivo)
    if linhas is None or not linhas:
        return False

    inicio = 0
    tamanho_reg, head = None, -1
    if linhas[0].startswith('TAMANHO_REGISTRO:'):
        inicio = 1
        tamanho_reg, head = _parse_header(linhas[0])

    conteudos = []
    for l in linhas[inicio:]:
        if not l:
            continue
        if l.startswith(TOMBSTONE):
            continue
        conteudo = l.rstrip(PADDING_CHAR)
        if conteudo:
            conteudos.append(conteudo)

    if not conteudos:
        linhas_novas = [_make_header(0, -1)]
        return _atomic_write(arquivo, linhas_novas)

    novo_tamanho = max(len(c) for c in conteudos)
    linhas_novas = [_make_header(novo_tamanho, -1)]
    for c in conteudos:
        linhas_novas.append(_pad_record(c, novo_tamanho) if novo_tamanho else c)

    return _atomic_write(arquivo, linhas_novas)

def inserirRegistroComReuso(arquivo, registro):
    linhas = _read_lines(arquivo)
    if linhas is None or not linhas:
        tamanho = len(registro)
        linhas_novas = [_make_header(tamanho, -1), _pad_record(registro, tamanho)]
        ok = _atomic_write(arquivo, linhas_novas)
        return 0 if ok else None

    inicio = 0
    tamanho_cabecalho, head = None, -1
    if linhas[0].startswith('TAMANHO_REGISTRO:'):
        inicio = 1
        tamanho_cabecalho, head = _parse_header(linhas[0])

    if head is not None and head >= 0:
        idx = inicio + head
        if idx < inicio or idx >= len(linhas):
            head = -1
        else:
            tomb = linhas[idx]
            next_head = -1
            if tomb.startswith(TOMBSTONE):
                m = re.match(r'^-?\d+', tomb[1:].lstrip())
                if m:
                    try:
                        next_head = int(m.group(0))
                    except Exception:
                        next_head = -1
            novo_tam = max(tamanho_cabecalho or 0, len(registro))
            rec = _pad_record(registro, novo_tam) if novo_tam else registro
            linhas[idx] = rec
            if tamanho_cabecalho is None:
                tamanho_cabecalho = novo_tam
            if novo_tam > (tamanho_cabecalho or 0):
                padded = [_pad_record(x.rstrip(PADDING_CHAR), novo_tam) for x in linhas[inicio:]]
                linhas = [_make_header(novo_tam, next_head)] + padded
            else:
                linhas[0] = _make_header(tamanho_cabecalho or novo_tam, next_head)
            return (idx - inicio) if _atomic_write(arquivo, linhas) else None

    novo_tam = max(tamanho_cabecalho or 0, len(registro))
    rec = _pad_record(registro, novo_tam) if novo_tam else registro

    if inicio == 1:
        if novo_tam > (tamanho_cabecalho or 0):
            existentes_padded = [_pad_record(x.rstrip(PADDING_CHAR), novo_tam) for x in linhas[inicio:]]
        else:
            existentes_padded = [x for x in linhas[inicio:]]
        linhas_novas = [_make_header(novo_tam, -1)] + existentes_padded + [rec]
        rrn = len(linhas_novas) - inicio - 1
    else:
        existentes_padded = [_pad_record(x.rstrip(PADDING_CHAR), novo_tam) for x in linhas]
        linhas_novas = [_make_header(novo_tam, -1)] + existentes_padded + [rec]
        inicio = 1
        rrn = len(linhas_novas) - inicio - 1

    ok = _atomic_write(arquivo, linhas_novas)
    return rrn if ok else None

caminho = r"C:\Projetos\Faculdade\Estruturas_de_Dados_II\lectures\2 - Estruturas de Dados em Disco\outputs de leitura\animes_delimitadores.txt"

if not os.path.exists(caminho):
    print(f"Arquivo não encontrado: {caminho}")
    raise SystemExit(1)

while True:
    print("\n=== Menu rápido ===")
    print("1 - Remover registros por chave")
    print("2 - Compactar arquivo")
    print("3 - Inserir registro")
    print("4 - Sair")
    escolha = input("Escolha (1/2/3/4): ").strip()

    if escolha == "1":
        chave = input("Digite a chave (campo chave): ").strip()
        if not chave:
            print("Chave vazia.")
            continue
        ok = removeRegistro(caminho, chave)
        print("Registros marcados." if ok else "Nada foi removido ou ocorreu erro.")

    elif escolha == "2":
        confirmar = input("Isso vai reescrever o arquivo (s/N): ").strip().lower()
        if confirmar != 's':
            print("Cancelado.")
            continue
        ok = compactacaoDados(caminho)
        print("Compactação concluída." if ok else "Erro na compactação.")

    elif escolha == "3":
        registro = input("Digite o registro completo (linha): ").rstrip('\n')
        if not registro:
            print("Registro vazio.")
            continue
        rrn = inserirRegistroComReuso(caminho, registro)
        if rrn is None:
            print("Erro ao inserir registro.")
        else:
            print(f"Registro inserido no RRN = {rrn}")

    elif escolha == "4":
        print("Saindo.")
        break

    else:
        print("Opção inválida. Tente novamente.")