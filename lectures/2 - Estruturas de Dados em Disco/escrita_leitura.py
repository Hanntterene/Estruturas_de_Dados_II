import pandas as pd
import os
import time

class Anime:
    def __init__(self, name, episodes, votes, weight, rate, genres):
        self.name = name
        self.episodes = episodes
        self.votes = votes
        self.weight = weight
        self.rate = rate
        self.genres = genres
    
    def __str__(self):
        return f"Name: {self.name}, Episodes: {self.episodes}, Rate: {self.rate}, Genres: {', '.join(self.genres)}"

def df_to_anime_list(df):
    animes = []
    genre_columns = [col for col in df.columns if col.startswith('genre_')]
    
    for _, row in df.iterrows():
        genres = []
        for genre_col in genre_columns:
            if row.get(genre_col, 0) == 1:
                genre_name = genre_col.replace('genre_', '').replace('_', ' ').title()
                genres.append(genre_name)
        
        anime = Anime(
            str(row.get('anime', '')),
            row.get('episodes', 0),
            row.get('votes', 0),
            row.get('weight', 0.0),
            row.get('rate', 0.0),
            genres
        )
        animes.append(anime)
    
    return animes

# Carregar dataset
df = pd.read_csv(r'C:\Projetos\Faculdade\Estruturas_de_Dados_II\datasets\animes.csv')
dataset = df_to_anime_list(df)
OUTPUT_DIR = r'C:\Projetos\Faculdade\Estruturas_de_Dados_II\lectures\2 - Estruturas de Dados em Disco\outputs de leitura'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# MÉTODO 1: Tamanho Fixo
def escritaTamanhoFixo(arquivo, dataset):
    TAMANHOS = {'name': 100, 'episodes': 10, 'votes': 15, 'weight': 10, 'rate': 10, 'genres': 200}
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(f"TAMANHO_REGISTRO:{sum(TAMANHOS.values())}\n")
        for anime in dataset:
            registro = (
                str(anime.name).ljust(TAMANHOS['name'])[:TAMANHOS['name']] +
                str(anime.episodes).ljust(TAMANHOS['episodes'])[:TAMANHOS['episodes']] +
                str(anime.votes).ljust(TAMANHOS['votes'])[:TAMANHOS['votes']] +
                str(anime.weight).ljust(TAMANHOS['weight'])[:TAMANHOS['weight']] +
                str(anime.rate).ljust(TAMANHOS['rate'])[:TAMANHOS['rate']] +
                str(', '.join(anime.genres)).ljust(TAMANHOS['genres'])[:TAMANHOS['genres']]
            )
            f.write(registro + '\n')

def leituraTamanhoFixo(arquivo):
    TAMANHOS = {'name': 100, 'episodes': 10, 'votes': 15, 'weight': 10, 'rate': 10, 'genres': 200}
    animes = []
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        f.readline()  # Pular cabeçalho
        for linha in f:
            linha = linha.rstrip('\n')
            if not linha:
                continue
                
            pos = 0
            name = linha[pos:pos + TAMANHOS['name']].strip()
            pos += TAMANHOS['name']
            episodes = int(linha[pos:pos + TAMANHOS['episodes']].strip() or 0)
            pos += TAMANHOS['episodes']
            votes = int(linha[pos:pos + TAMANHOS['votes']].strip() or 0)
            pos += TAMANHOS['votes']
            weight = float(linha[pos:pos + TAMANHOS['weight']].strip() or 0)
            pos += TAMANHOS['weight']
            rate = float(linha[pos:pos + TAMANHOS['rate']].strip() or 0)
            pos += TAMANHOS['rate']
            genres_str = linha[pos:pos + TAMANHOS['genres']].strip()
            genres = [g.strip() for g in genres_str.split(',') if g.strip()]
            
            animes.append(Anime(name, episodes, votes, weight, rate, genres))
    
    return animes

# MÉTODO 2: Quantidade de Campos
def escritaQtdeCampos(arquivo, dataset):
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write("NUM_CAMPOS:6\n")
        for anime in dataset:
            f.write(f"6|{anime.name}|{anime.episodes}|{anime.votes}|{anime.weight}|{anime.rate}|{', '.join(anime.genres)}\n")

# MÉTODO 3: Quantidade de Bytes
def escritaQtdeBytes(arquivo, dataset):
    with open(arquivo, 'wb') as f:
        f.write("METODO:QTDE_BYTES\n".encode('utf-8'))
        for anime in dataset:
            campos = [str(anime.name), str(anime.episodes), str(anime.votes), 
                     str(anime.weight), str(anime.rate), ', '.join(anime.genres)]
            registro_bytes = b""
            for campo in campos:
                campo_bytes = campo.encode('utf-8')
                registro_bytes += f"{len(campo_bytes):04d}".encode('utf-8') + campo_bytes
            f.write(registro_bytes + b'\n')

# MÉTODO 4: Arquivo de Índices
def escritaArquivoIndices(arquivo, dataset):
    arquivo_dados = arquivo.replace('.txt', '_dados.txt')
    arquivo_indices = arquivo.replace('.txt', '_indices.txt')
    
    # Criar arquivo principal vazio (índices.txt)
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write("METODO:ARQUIVO_INDICES\n")
    
    with open(arquivo_dados, 'wb') as f_dados, open(arquivo_indices, 'w', encoding='utf-8') as f_indices:
        f_indices.write("NAME|POSICAO|TAMANHO\n")
        for anime in dataset:
            pos_inicial = f_dados.tell()
            registro = f"{anime.name}|{anime.episodes}|{anime.votes}|{anime.weight}|{anime.rate}|{', '.join(anime.genres)}\n"
            f_dados.write(registro.encode('utf-8'))
            tamanho = f_dados.tell() - pos_inicial
            f_indices.write(f"{anime.name.replace('|', '\\|')}|{pos_inicial}|{tamanho}\n")

# MÉTODO 5: Delimitadores
def escritaDelimitadores(arquivo, dataset):
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write("DELIM_CAMPO:|\nname|episodes|votes|weight|rate|genres\n")
        for anime in dataset:
            campos = [str(anime.name).replace('|', '\\|'), str(anime.episodes), str(anime.votes),
                     str(anime.weight), str(anime.rate), ', '.join(anime.genres).replace('|', '\\|')]
            f.write('|'.join(campos) + '\n')

def medirTempo(funcao, nome, arquivo, dataset):
    inicio = time.time()
    funcao(arquivo, dataset)
    tempo = time.time() - inicio
    
    tamanho = os.path.getsize(arquivo)
    if nome == "Arquivo Índices":
        dados = arquivo.replace('.txt', '_dados.txt')
        indices = arquivo.replace('.txt', '_indices.txt')
        if os.path.exists(dados): tamanho += os.path.getsize(dados)
        if os.path.exists(indices): tamanho += os.path.getsize(indices)
    
    return {'metodo': nome, 'tempo': tempo, 'tamanho': tamanho}

if __name__ == "__main__":
    print(f"✅ Dataset: {len(dataset)} animes\n")
    
    # TESTE DE LEITURA
    print("📖 TESTE DE LEITURA - MÉTODO 1")
    print("=" * 50)
    arquivo_teste = os.path.join(OUTPUT_DIR, 'animes_tamanho_fixo.txt')
    
    if not os.path.exists(arquivo_teste):
        escritaTamanhoFixo(arquivo_teste, dataset)
    
    inicio = time.time()
    animes_lidos = leituraTamanhoFixo(arquivo_teste)
    tempo_leitura = time.time() - inicio
    
    print(f"⏱️  Leitura: {tempo_leitura:.4f}s")
    print(f"📊 Originais: {len(dataset)} | Lidos: {len(animes_lidos)}")
    if len(animes_lidos) == len(dataset):
        print("✅ Integridade OK!")
    
    print(f"\n📋 Primeiros 3:")
    for i, anime in enumerate(animes_lidos[:3]):
        print(f"   {i+1}: {anime}")
    
    # PROCESSAMENTO
    print(f"\n\n🚀 PROCESSANDO {len(dataset)} REGISTROS")
    print("=" * 50)
    
    resultados = []
    resultados.append(medirTempo(escritaTamanhoFixo, "Tamanho Fixo", os.path.join(OUTPUT_DIR, 'animes_tamanho_fixo.txt'), dataset))
    resultados.append(medirTempo(escritaQtdeCampos, "Qtde Campos", os.path.join(OUTPUT_DIR, 'animes_qtde_campos.txt'), dataset))
    resultados.append(medirTempo(escritaQtdeBytes, "Qtde Bytes", os.path.join(OUTPUT_DIR, 'animes_qtde_bytes.txt'), dataset))
    resultados.append(medirTempo(escritaArquivoIndices, "Arquivo Índices", os.path.join(OUTPUT_DIR, 'animes_indices.txt'), dataset))
    resultados.append(medirTempo(escritaDelimitadores, "Delimitadores", os.path.join(OUTPUT_DIR, 'animes_delimitadores.txt'), dataset))
    
    # RELATÓRIO
    print("\n📈 RELATÓRIO")
    print("=" * 50)
    resultados_ordenados = sorted(resultados, key=lambda x: x['tempo'])
    
    for i, r in enumerate(resultados_ordenados):
        emoji = "🏆" if i == 0 else "  "
        print(f"{emoji} {i+1}º {r['metodo']:<15} {r['tempo']:.4f}s | {r['tamanho']/1024/1024:.2f}MB")
    
    melhor = resultados_ordenados[0]
    print(f"\n🏆 VENCEDOR: {melhor['metodo']} ({melhor['tempo']:.4f}s)")
    print(f"🎉 CONCLUÍDO!")