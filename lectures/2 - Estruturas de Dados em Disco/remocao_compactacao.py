import os
import tempfile
import re

PADDING_CHAR = ' '    # NÃO é '*'
TOMBSTONE = '*'       # marca de remoção (primeiro caractere)
# Header format: "TAMANHO_REGISTRO:{size}|LIVRE:{head}"
# where head is 0-based RRN of top of free list, -1 = none

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

    # percorre e marca; cada novo tombstone aponta para head atual (0-based), header vira pos atual (0-based)
    for i in range(inicio, len(linhas)):
        linha = linhas[i]
        if not linha:
            continue

        # conteudo sem marca e sem padding para busca
        if linha.startswith(TOMBSTONE):
            conteudo_sem = linha[1:]
            already_deleted = True
        else:
            conteudo_sem = linha
            already_deleted = False

        conteudo_sem = conteudo_sem.rstrip(PADDING_CHAR).strip()

        # comparação por campo chave (primeiro campo antes do '|')
        campo0 = conteudo_sem.split('|', 1)[0].strip().lower() if conteudo_sem else ''
        if chave_norm == campo0:
            if already_deleted:
                continue
            # calcula RRN 0-based do registro atual
            rrn_atual = i - inicio
            # new record content = "*" + str(head) + original[1:]
            resto = linha[1:] if len(linha) > 1 else ''
            marca = TOMBSTONE + str(head) + resto
            # sempre padronizar para tamanho_reg quando header existir
            if tamanho_reg:
                marca = _pad_record(marca, tamanho_reg)
            novas[i] = marca
            # update head to this RRN
            head = rrn_atual
            removidos += 1

    if removidos == 0:
        return False

    # atualiza cabeçalho (preserva tamanho_reg)
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
            # tombstone stores pointer like "*<n>" -> skip
            continue
        # remove padding spaces if any
        conteudo = l.rstrip(PADDING_CHAR)
        if conteudo:
            conteudos.append(conteudo)

    if not conteudos:
        linhas_novas = [_make_header(0, 0)]
        return _atomic_write(arquivo, linhas_novas)

    novo_tamanho = max(len(c) for c in conteudos)
    linhas_novas = [_make_header(novo_tamanho, 0)]
    for c in conteudos:
        linhas_novas.append(_pad_record(c, novo_tamanho) if novo_tamanho else c)

    return _atomic_write(arquivo, linhas_novas)

def inserirRegistroComReuso(arquivo, registro):
    linhas = _read_lines(arquivo)
    if linhas is None:
        # cria novo arquivo com cabeçalho
        tamanho = len(registro)
        linhas_novas = [_make_header(tamanho, -1), _pad_record(registro, tamanho)]
        ok = _atomic_write(arquivo, linhas_novas)
        return 0 if ok else None

    if not linhas:
        tamanho = len(registro)
        linhas_novas = [_make_header(tamanho, -1), _pad_record(registro, tamanho)]
        ok = _atomic_write(arquivo, linhas_novas)
        return 0 if ok else None

    inicio = 0
    tamanho_cabecalho, head = None, -1
    if linhas[0].startswith('TAMANHO_REGISTRO:'):
        inicio = 1
        tamanho_cabecalho, head = _parse_header(linhas[0])

    # se houver slot livre (head >= 0), reutiliza; head é 0-based
    if head is not None and head >= 0:
        idx = inicio + head
        if idx < inicio or idx >= len(linhas):
            # head inválido -> não reutiliza
            head = -1
        else:
            tomb = linhas[idx]
            # extrai próximo head do começo de tomb[1:] (pode ser -1 ou número) usando regex
            next_head = -1
            if tomb.startswith(TOMBSTONE):
                m = re.match(r'^-?\d+', tomb[1:].lstrip())
                if m:
                    try:
                        next_head = int(m.group(0))
                    except Exception:
                        next_head = -1
            # determine novo tamanho após inserção
            novo_tam = max(tamanho_cabecalho or 0, len(registro))
            # preparar registro com padding se header existe
            rec = _pad_record(registro, novo_tam) if novo_tam else registro
            # coloca novo registro no idx
            linhas[idx] = rec
            # se novo_tam > tamanho_cabecalho, padronizar todas as linhas de dados
            if tamanho_cabecalho is None:
                tamanho_cabecalho = novo_tam
            if novo_tam > (tamanho_cabecalho or 0):
                padded = [_pad_record(x.rstrip(PADDING_CHAR), novo_tam) for x in linhas[inicio:]]
                linhas = [_make_header(novo_tam, next_head)] + padded
            else:
                # atualiza header para apontar next_head, preservando tamanho
                linhas[0] = _make_header(tamanho_cabecalho or novo_tam, next_head)
            return (idx - inicio) if _atomic_write(arquivo, linhas) else None

    # sem slot livre: append no fim (e possivelmente criar header)
    novo_tam = max(tamanho_cabecalho or 0, len(registro))
    rec = _pad_record(registro, novo_tam) if novo_tam else registro

    if inicio == 1:
        # header existe: pad existing data to novo_tam if needed
        if novo_tam > (tamanho_cabecalho or 0):
            existentes_padded = [_pad_record(x.rstrip(PADDING_CHAR), novo_tam) for x in linhas[inicio:]]
        else:
            existentes_padded = [x for x in linhas[inicio:]]
        linhas_novas = [_make_header(novo_tam, -1)] + existentes_padded + [rec]
        inicio = 1
        rrn = len(linhas_novas) - inicio - 1
    else:
        # sem header: pad existing lines para novo_tam e inserir header
        existentes_padded = [_pad_record(x.rstrip(PADDING_CHAR), novo_tam) for x in linhas]
        linhas_novas = [_make_header(novo_tam, -1)] + existentes_padded + [rec]
        inicio = 1
        rrn = len(linhas_novas) - inicio - 1

    ok = _atomic_write(arquivo, linhas_novas)
    return rrn if ok else None

# usar arquivo fixo (não pedir caminho ao usuário)
caminho = r"C:\Projetos\Faculdade\Estruturas_de_Dados_II\lectures\2 - Estruturas de Dados em Disco\outputs de leitura\animes_delimitadores.txt"

if not os.path.exists(caminho):
    print(f"Arquivo não encontrado: {caminho}")
    raise SystemExit(1)

# menu principal
while True:
    print("\n=== Menu rápido ===")
    print("1 - Remover registros por chave (marca com '*<next>' na primeira posição)")
    print("2 - Compactar arquivo (remover registros marcados e atualizar header)")
    print("3 - Inserir registro (com reuso de tombstone)")
    print("4 - Sair")
    escolha = input("Escolha (1/2/3/4): ").strip()

    if escolha == "1":
        chave = input("Digite a chave (string) para remover (ex.: campo_chave): ").strip()
        if not chave:
            print("Chave vazia — operação abortada.")
            continue
        ok = removeRegistro(caminho, chave)
        print("OK — registros marcados como removidos." if ok else "Nada foi removido ou ocorreu erro.")

    elif escolha == "2":
        confirmar = input("Tem certeza? Isso vai reescrever o arquivo (s/N): ").strip().lower()
        if confirmar != 's':
            print("Compactação cancelada.")
            continue
        ok = compactacaoDados(caminho)
        print("Compactação concluída com sucesso." if ok else "Erro na compactação ou arquivo vazio.")

    elif escolha == "3":
        registro = input("Digite o registro completo (ex.: chave|campo2|campo3): ").rstrip('\n')
        if not registro:
            print("Registro vazio — abortando.")
            continue
        rrn = inserirRegistroComReuso(caminho, registro)
        if rrn is None:
            print("Erro ao inserir registro.")
        else:
            print(f"Registro inserido no RRN = {rrn} (reutilizou tombstone se disponível).")

    elif escolha == "4":
        print("Saindo. Valeu.")
        break

    else:
        print("Opção inválida. Tenta de novo.")