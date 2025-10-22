import os
import tempfile
import re

ALVO = r"C:\Projetos\Faculdade\Estruturas_de_Dados_II\lectures\2 - Estruturas de Dados em Disco\outputs de leitura\animes_delimitadores.txt"
PADDING_CHAR = ' '

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

def _parse_header(line):
    # returns (tamanho:int or None, livre:int or -1)
    if not line or not line.startswith("TAMANHO_REGISTRO:"):
        return None, -1
    parts = line.split('|')
    tamanho = None
    livre = -1
    m = re.match(r"TAMANHO_REGISTRO:(\d+)", parts[0])
    if m:
        tamanho = int(m.group(1))
    for p in parts[1:]:
        mm = re.match(r"LIVRE:(-?\d+)", p)
        if mm:
            livre = int(mm.group(1))
    return tamanho, livre

def _make_header(tamanho, livre):
    return f"TAMANHO_REGISTRO:{tamanho}|LIVRE:{livre}"

def pad_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw = [ln.rstrip('\n') for ln in f.readlines()]
    except FileNotFoundError:
        print("Arquivo não encontrado:", path)
        return False

    if not raw:
        print("Arquivo vazio.")
        return False

    inicio = 0
    tamanho_header, livre = _parse_header(raw[0])
    if tamanho_header is not None:
        inicio = 1

    dados = raw[inicio:]
    if not dados:
        # nothing to pad, still ensure header exists
        tamanho = tamanho_header or 0
        new_lines = [_make_header(tamanho, livre)]
        return _atomic_write(path, new_lines)

    # compute actual max length among data lines (preserve tombstones as-is)
    actual_max = max(len(line.rstrip()) for line in dados)
    # choose target size: if header specifies a larger size, keep it; otherwise use actual_max
    target = max(actual_max, tamanho_header or 0)

    # pad/truncate each data line to target (truncate only if longer)
    padded = []
    for line in dados:
        s = line.rstrip()  # remove trailing whitespace to standardize
        if len(s) > target:
            s = s[:target]
        else:
            s = s + (PADDING_CHAR * (target - len(s)))
        padded.append(s)

    header = _make_header(target, livre if livre is not None else -1)
    new_lines = [header] + padded
    ok = _atomic_write(path, new_lines)
    if ok:
        print(f"Arquivo atualizado: tamanho_registro = {target}, livre = {livre}")
    else:
        print("Erro ao gravar arquivo.")
    return ok

if __name__ == "__main__":
    pad_file(ALVO)