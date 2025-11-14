import os

class Indiceprimario:
    def __init__(self, lista=None, arq1="", arq2=""):
        self.lista = lista or []   # lista de tuplas (chave, rrn)
        self.arq1 = arq1           # arquivo de dados
        self.arq2 = arq2           # arquivo de índice (para salvar/carregar)

    def _ler_linhas(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return [l.rstrip('\n') for l in f.readlines()]
        except FileNotFoundError:
            return []

    def lerRegistroComRRN(self, arq, rrn):
        linhas = self._ler_linhas(arq)
        if not linhas:
            return None

        inicio = 0
        if linhas[0].startswith('TAMANHO_REGISTRO:'):
            inicio = 1
        if inicio < len(linhas) and linhas[inicio].startswith('DELIM_CAMPO:'):
            inicio += 1

        # possivel linha de cabeçalho de colunas
        data_start = inicio
        if data_start < len(linhas) and '|' in linhas[data_start]:
            first_field = linhas[data_start].split('|', 1)[0].strip()
            if any(c.isalpha() for c in first_field) and not first_field.isdigit():
                data_start += 1

        idx = data_start + int(rrn)
        if idx < data_start or idx >= len(linhas):
            return None

        linha = linhas[idx].rstrip()
        if not linha or linha.startswith('*'):
            return None
        # remove padding
        return linha.rstrip(' ')

    def Construtor(self):
        if not self.arq1:
            return []

        linhas = self._ler_linhas(self.arq1)
        if not linhas:
            self.lista = []
            return self.lista

        inicio = 0
        if linhas[0].startswith('TAMANHO_REGISTRO:'):
            inicio = 1
        if inicio < len(linhas) and linhas[inicio].startswith('DELIM_CAMPO:'):
            inicio += 1

        # linha de nomes de colunas (opcional)
        data_start = inicio
        cabecalhos = []
        if data_start < len(linhas) and '|' in linhas[data_start]:
            first_field = linhas[data_start].split('|', 1)[0].strip()
            if any(c.isalpha() for c in first_field) and not first_field.isdigit():
                cabecalhos = [h.strip() for h in linhas[data_start].split('|')]
                data_start += 1

        # determinar coluna chave: 'key' se existir, senão primeira coluna (0)
        chave_col = 0
        for i, h in enumerate(cabecalhos):
            if h.lower() == 'key':
                chave_col = i
                break

        indice = []
        rrn = 0
        for i in range(data_start, len(linhas)):
            linha = linhas[i]
            if not linha:
                continue
            if linha.startswith('*'):
                # registro apagado -> pular
                rrn += 1
                continue
            conteudo = linha.rstrip(' ')
            campos = conteudo.split('|') if '|' in conteudo else conteudo.split(',')
            chave = campos[chave_col].strip() if len(campos) > chave_col else ''
            indice.append((chave, rrn))
            rrn += 1

        # ordenar índice por chave (case-insensitive)
        indice.sort(key=lambda x: x[0].lower())
        self.lista = indice

        # gravar arquivo de índice (chave|rrn) se arq2 fornecido
        if self.arq2:
            try:
                with open(self.arq2, 'w', encoding='utf-8') as f:
                    for k, r in self.lista:
                        f.write(f"{k}|{r}\n")
            except Exception:
                pass

        return self.lista

    def Pesquisar(self, chave):
        chave_norm = chave.strip().lower()
        lo = 0
        hi = len(self.lista) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            mid_chave = self.lista[mid][0].lower()
            if mid_chave == chave_norm:
                return self.lista[mid][1]
            if mid_chave < chave_norm:
                lo = mid + 1
            else:
                hi = mid - 1
        return None
