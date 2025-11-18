import os

class indicePrimario:
    def __init__(self, lista=None, arq1='', arq2=''):
        self.lista = lista or []      # lista de tuplas (chave, rrn)
        self.arq1 = arq1
        self.arq2 = arq2

    def _ler_linhas(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return [l.rstrip('\n') for l in f.readlines()]
        except FileNotFoundError:
            return []

    def _salvar_arquivo_indice(self):
        if not self.arq2:
            return
        try:
            with open(self.arq2, 'w', encoding='utf-8') as f:
                for chave, rrn in self.lista:
                    f.write(f"{chave}|{rrn}\n")
        except Exception:
            pass

    def Construtor(self):
        if not self.arq1:
            self.lista = []
            self._salvar_arquivo_indice()
            return self.lista

        linhas = self._ler_linhas(self.arq1)
        if not linhas:
            self.lista = []
            self._salvar_arquivo_indice()
            return self.lista

        inicio = 0
        # arquivo de registros fixos com header
        if linhas[0].startswith('TAMANHO_REGISTRO:'):
            inicio = 1
        if inicio < len(linhas) and linhas[inicio].startswith('DELIM_CAMPO:'):
            inicio += 1

        # detectar possível linha de cabeçalhos (pode ser '|' ou ',')
        data_start = inicio
        cabecalhos = []
        delimiter = None
        if data_start < len(linhas):
            sample = linhas[data_start]
            if '|' in sample:
                delimiter = '|'
            elif ',' in sample:
                delimiter = ','
            if delimiter:
                primeiro = sample.split(delimiter, 1)[0].strip()
                if any(c.isalpha() for c in primeiro) and not primeiro.isdigit():
                    cabecalhos = [h.strip() for h in sample.split(delimiter)]
                    data_start += 1

        # índice: determinar coluna da chave ('key' se existir), senão primeira coluna
        chave_col = 0
        for i, h in enumerate(cabecalhos):
            if h.lower() == 'key':
                chave_col = i
                break

        indice = []
        rrn = 0
        for i in range(data_start, len(linhas)):
            linha = linhas[i]
            # pular linhas vazias (não contam)
            if linha.strip() == '' or linha.strip() == delimiter:
                continue
            # tombstone
            if linha.startswith('*'):
                rrn += 1
                continue
            # escolher delimitador para essa linha (prefere detectado, senão tenta ambos)
            if delimiter:
                campos = linha.rstrip().split(delimiter)
            else:
                if '|' in linha:
                    campos = linha.rstrip().split('|')
                else:
                    campos = linha.rstrip().split(',')
            chave = campos[chave_col].strip() if len(campos) > chave_col else ''
            indice.append((chave, rrn))
            rrn += 1

        indice.sort(key=lambda x: x[0].lower())
        self.lista = indice
        self._salvar_arquivo_indice()
        return self.lista

    def Pesquisar(self, chave):
        chave_norm = chave.strip().lower()
        lo, hi = 0, len(self.lista) - 1
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

    def Inserir(self, chave, rrn):
        tupla = (chave, rrn)
        if not self.lista:
            self.lista = [tupla]
            self._salvar_arquivo_indice()
            return True
        chave_norm = chave.lower()
        lo, hi = 0, len(self.lista) - 1
        pos = len(self.lista)
        # localizar posição de inserção (estável: após iguais)
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.lista[mid][0].lower() <= chave_norm:
                lo = mid + 1
            else:
                pos = mid
                hi = mid - 1
        self.lista.insert(pos, tupla)
        self._salvar_arquivo_indice()
        return True

    def Remover(self, chave):
        chave_norm = chave.strip().lower()
        lo, hi = 0, len(self.lista) - 1
        found = None
        while lo <= hi:
            mid = (lo + hi) // 2
            mid_chave = self.lista[mid][0].lower()
            if mid_chave == chave_norm:
                found = mid
                break
            if mid_chave < chave_norm:
                lo = mid + 1
            else:
                hi = mid - 1
        if found is None:
            return None
        rrn = self.lista[found][1]
        # retroceder até o primeiro igual
        while found > 0 and self.lista[found-1][0].lower() == chave_norm:
            found -= 1
        self.lista.pop(found)
        self._salvar_arquivo_indice()
        return rrn

    def Destrutor(self):
        self.lista = []
        if self.arq2 and os.path.exists(self.arq2):
            try:
                os.remove(self.arq2)
            except Exception:
                pass
        return True

def main():
    base = os.path.dirname(__file__)
    # tenta nome padrão; se não existir, tenta heroes_dataset.csv
    arquivo_dados = os.path.join(base, "arquivoDadosRegistrosFixos.txt")
    if not os.path.exists(arquivo_dados):
        alt = os.path.join(base, "heroes_dataset.csv")
        if os.path.exists(alt):
            arquivo_dados = alt

    arquivo_indice = os.path.join(base, "indice_primario.txt")

    ip = indicePrimario(arq1=arquivo_dados, arq2=arquivo_indice)

    if not os.path.exists(arquivo_dados):
        print(f"Arquivo de dados não encontrado: {arquivo_dados}")
        return

    ip.Construtor()
    print(f"Índice carregado. Entradas = {len(ip.lista)} (arquivo: {os.path.basename(arquivo_dados)})")

    while True:
        print("\n=== Índice Primário — Menu ===")
        print("1 - Inserir entrada (chave, rrn)")
        print("2 - Remover entrada por chave")
        print("3 - Destrutor (apagar índice em memória e arquivo de índice)")
        print("4 - Sair")
        escolha = input("Escolha (1-4): ").strip()

        if escolha == "1":
            chave = input("Digite a chave a inserir: ").strip()
            if not chave:
                print("Chave vazia.")
                continue
            s = input("Digite o RRN (número) associado: ").strip()
            try:
                rrn = int(s)
            except ValueError:
                print("RRN inválido.")
                continue
            ok = ip.Inserir(chave, rrn)
            print("Inserção realizada." if ok else "Falha na inserção.")

        elif escolha == "2":
            chave = input("Digite a chave a remover: ").strip()
            if not chave:
                print("Chave vazia.")
                continue
            rrn_removido = ip.Remover(chave)
            if rrn_removido is None:
                print("Chave não encontrada; nada removido.")
            else:
                print(f"Removido. RRN removido = {rrn_removido}")

        elif escolha == "3":
            confirma = input("Confirma destrutor (apagar índice em memória e arquivo)? (s/N): ").strip().lower()
            if confirma == 's':
                ip.Destrutor()
                print("Índice destruído.")
            else:
                print("Cancelado.")

        elif escolha == "4":
            print("Saindo.")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
