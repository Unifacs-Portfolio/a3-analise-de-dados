import pandas as pd
import glob
import os

# ==========================================
# CONFIGURAÇÃO DE COLUNAS (O MAPA AGORA É SÓ PARA OS VALORES)
# ==========================================
MAPA_COLUNAS = {
    'gini': 'Índice de Gini', # Ajuste para o nome da coluna no GINI 18, 21, 22, 23.csv
    'renda': 'Rendimento',    # Ajuste para o nome da coluna no PNAD 18, 21, 22, 23.csv
    'pib': 'PIB'              # Ajuste para o nome da coluna no PIB 18, 21, 22, 23.csv
}

def limpar_string_uf(df, nome_coluna):
    """Extrai apenas os 2 dígitos do código do Estado (Ex: '29 Bahia' -> '29')"""
    df['id_uf'] = df[nome_coluna].astype(str).str.extract(r'^\s*(\d{2})')[0]
    df = df.dropna(subset=['id_uf'])
    return df

def processar_matriz_temporal_datasus(caminho_arquivo, nome_valor):
    """Lê os arquivos do DATASUS que têm os anos como colunas e transforma em linhas (Melt)"""
    df = pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, skipfooter=1, engine='python')
    
    # O HACK SÊNIOR: Pega o nome da primeira coluna dinamicamente, ignorando erros de digitação do governo
    coluna_uf = df.columns[0]
    df = limpar_string_uf(df, coluna_uf)
    
    # Transforma as colunas de anos (2018, 2021...) em linhas
    df_melt = pd.melt(df, id_vars=['id_uf'], value_vars=['2018', '2021', '2022', '2023'], var_name='ano', value_name=nome_valor)
    
    # Converte para número, removendo traços ou erros do DATASUS
    df_melt[nome_valor] = pd.to_numeric(df_melt[nome_valor].astype(str).str.replace('-', '0'), errors='coerce').fillna(0)
    return df_melt

def processar_matriz_ibge(caminho_arquivo, nome_valor, col_original):
    """Lê os arquivos do IBGE (Gini, PNAD, PIB) e padroniza para o Merge"""
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', skiprows=3) 
    except (pd.errors.ParserError, UnicodeDecodeError):
        df = pd.read_csv(caminho_arquivo, sep=',')
        
    # O HACK SÊNIOR APLICADO AO IBGE TAMBÉM
    coluna_uf = df.columns[0]
    df = limpar_string_uf(df, coluna_uf)
    
    # Se o arquivo já vier com a coluna 'Ano' pronta (Formato longo)
    if 'Ano' in df.columns or 'ano' in df.columns:
        col_ano = 'Ano' if 'Ano' in df.columns else 'ano'
        
        # Pega a coluna de valor usando .loc para evitar erros se o nome não bater 100%
        # Se o MAPA falhar, ele tenta pegar a última coluna numérica do arquivo
        try:
            df = df.rename(columns={col_original: nome_valor, col_ano: 'ano'})
        except:
            ultima_coluna = df.columns[-1]
            df = df.rename(columns={ultima_coluna: nome_valor, col_ano: 'ano'})
            
        return df[['id_uf', 'ano', nome_valor]]
    else:
        # Se vier com anos nas colunas, faz o melt igual DATASUS
        df_melt = pd.melt(df, id_vars=['id_uf'], value_vars=['2018', '2021', '2022', '2023'], var_name='ano', value_name=nome_valor)
        return df_melt

print('Iniciando processamento das matrizes históricas (Raiz)...')

# 1. Carregando as Matrizes do DATASUS
df_internacoes = processar_matriz_temporal_datasus('./datasets/datasets_juntos/datasus_internacoes.csv', 'total_internacoes')
df_permanencia = processar_matriz_temporal_datasus('./datasets/datasets_juntos/datasus_dias_permanencia.csv', 'dias_permanencia')
df_icsap = processar_matriz_temporal_datasus('./datasets/datasets_juntos/datasus_icsap.csv', 'internacoes_icsap')

# 2. Carregando as Matrizes Econômicas (IBGE)
df_gini = processar_matriz_ibge('./datasets/datasets_juntos/GINI.csv', 'indice_gini', MAPA_COLUNAS['gini'])
df_renda = processar_matriz_ibge('./datasets/datasets_juntos/PNAD.csv', 'renda_media', MAPA_COLUNAS['renda'])
df_pib = processar_matriz_ibge('./datasets/datasets_juntos/PIB.csv', 'pib_total', MAPA_COLUNAS['pib'])

print('Unificando as bases centrais...')
df_mestre = df_internacoes.merge(df_permanencia, on=['id_uf', 'ano'], how='left')\
                          .merge(df_icsap, on=['id_uf', 'ano'], how='left')\
                          .merge(df_gini, on=['id_uf', 'ano'], how='left')\
                          .merge(df_renda, on=['id_uf', 'ano'], how='left')\
                          .merge(df_pib, on=['id_uf', 'ano'], how='left')

# 3. Processando Pastas Anuais (Mortalidade e População)
anos_analise = ['2018', '2021', '2022', '2023']
bases_anuais = []

for ano in anos_analise:
    print(f'Buscando pastas locais do ano {ano}...')
    
    # Mortalidade Evitável
    arquivos_mort = glob.glob(f'./datasets/datasets{ano}/mortalidade_*.csv')
    if arquivos_mort:
        df_mort = pd.read_csv(arquivos_mort[0], encoding='latin1', sep=';', header=3, skipfooter=1, engine='python')
        
        # Pega a primeira coluna dinamicamente
        coluna_uf_mort = df_mort.columns[0]
        df_mort = limpar_string_uf(df_mort, coluna_uf_mort)
        
        df_mort = df_mort.rename(columns={df_mort.columns[1]: 'obitos_evitaveis'})
        df_mort['ano'] = ano
        df_mort = df_mort[['id_uf', 'ano', 'obitos_evitaveis']]
    else:
        print(f"Aviso: Arquivo de mortalidade não encontrado para {ano}")
        continue

    # População
    arq_pop = f'./datasets/datasets{ano}/populacao_ibge_{ano}.csv'
    if os.path.exists(arq_pop):
        df_pop = pd.read_csv(arq_pop)
        if 'id_municipio' in df_pop.columns:
            df_pop = df_pop.rename(columns={'id_municipio': 'id_uf'})
        df_pop['id_uf'] = df_pop['id_uf'].astype(str)
        df_pop['ano'] = ano
        df_pop = df_pop[['id_uf', 'ano', 'nome_uf', 'populacao']]
    else:
        print(f"Aviso: Arquivo de população não encontrado para {ano}")
        continue
        
    df_ano_consolidado = df_pop.merge(df_mort, on=['id_uf', 'ano'], how='left')
    bases_anuais.append(df_ano_consolidado)

df_anuais = pd.concat(bases_anuais, ignore_index=True)

# 4. O Grande Merge Final
print('Gerando Banco de Dados Final e Calculando Indicadores Relativos...')
df_final = df_anuais.merge(df_mestre, on=['id_uf', 'ano'], how='left')

# Convertendo colunas para numérico
cols_numericas = ['obitos_evitaveis', 'total_internacoes', 'dias_permanencia', 'internacoes_icsap', 'pib_total', 'renda_media']
for col in cols_numericas:
    df_final[col] = pd.to_numeric(df_final[col].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)

# ==========================================
# CRIAÇÃO DAS FEATURES CIENTÍFICAS
# ==========================================

df_final['pib_per_capita'] = (df_final['pib_total'] * 1000) / df_final['populacao']
df_final['taxa_icsap_100k'] = (df_final['internacoes_icsap'] / df_final['populacao']) * 100000
df_final['tempo_medio_permanencia'] = df_final['dias_permanencia'] / df_final['total_internacoes'].replace(0, 1)
df_final['taxa_mortalidade_evitavel_100k'] = (df_final['obitos_evitaveis'] / df_final['populacao']) * 100000

# Limpeza e Exportação
df_final = df_final.dropna(subset=['id_uf']).round(2)
caminho_saida = './datasets/base_consolidada_saude_historico.csv'
df_final.to_csv(caminho_saida, index=False)

print(df_final[['nome_uf', 'ano', 'taxa_mortalidade_evitavel_100k', 'tempo_medio_permanencia']].head())
print(f'\nPipeline concluído com sucesso! Tabela Mestra salva em: {caminho_saida}')