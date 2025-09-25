import os
import sys
import random

# Caminho da pasta com os arquivos txt
pasta = os.path.join(os.path.dirname(__file__), 'AT01 - Casos de teste')

# Lista todos os arquivos .txt na pasta
arquivos_txt = sorted([f for f in os.listdir(pasta) if f.startswith('input') and f.endswith('.txt')])

# Mostra as opções para o usuário
print("="*40)
print("Selecione um arquivo de entrada para o teste:")
print("="*40)
for idx, nome in enumerate(arquivos_txt, 1):
    print(f"{idx:2d} - {nome}")
print("="*40)

# Usuário escolhe o arquivo de entrada
opcao = int(input("Digite o número do arquivo desejado: "))

if 1 <= opcao <= len(arquivos_txt):
    nome_arquivo = arquivos_txt[opcao - 1]
    caminho_arquivo = os.path.join(pasta, nome_arquivo)
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        # Lê todas as linhas não vazias e já coloca em minúsculo
        linhas = [linha.strip().lower() for linha in f.readlines() if linha.strip()]
        if len(linhas) < 2:
            print("\n[ERRO] O arquivo deve conter pelo menos duas linhas (tamanho e gerador).")
            sys.exit(1)

        # Extrai o número da primeira linha (tamanho)
        tamanho_str = ''.join(filter(str.isdigit, linhas[0]))
        if not tamanho_str:
            print("\n[ERRO] O valor do tamanho não contém nenhum dígito.")
            sys.exit(1)
        tamanho = int(tamanho_str)
        if tamanho <= 0:
            print("\n[ERRO] O valor do tamanho deve ser um número inteiro maior que zero.")
            sys.exit(1)

        # Procura a primeira letra válida na segunda linha (gerador)
        gerador = None
        for letra in linhas[1]:
            if letra in ('r', 'c', 'd'):
                gerador = letra
                break
        if not gerador:
            print("\n[ERRO] O gerador deve conter pelo menos uma letra válida: 'r', 'c' ou 'd'.")
            sys.exit(1)

        print("\n" + "="*40)
        print(f"Arquivo selecionado: {nome_arquivo}")
        print(f"Tamanho lido: {tamanho}")
        print(f"Gerador lido: {gerador}")
        print("="*40)

        # Geração do vetor inicial conforme o modo escolhido
        if gerador == 'c':
            vetor = list(range(1, tamanho + 1))
            tipo = "Crescente"
        elif gerador == 'd':
            vetor = list(range(tamanho, 0, -1))
            tipo = "Decrescente"
        elif gerador == 'r':
            vetor = [random.randint(0, 32000) for _ in range(tamanho)]
            tipo = "Aleatório"
        else:
            print("\n[ERRO] Modo de geração inválido.")
            sys.exit(1)

        print(f"Tipo de vetor: {tipo}")
        print(f"Vetor gerado ({len(vetor)} elementos):")
        print(vetor)
        print("="*40)
else:
    print("\n[ERRO] Opção inválida.")
    sys.exit(1)