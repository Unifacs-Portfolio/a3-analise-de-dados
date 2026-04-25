import pandas as pd
import glob

print('Iniciando pipeline de dados...')

# ==========================================
# CONSOLIDAÇÃO DO DATASUS
# ==========================================
print('Lendo e unificando arquivos do DATASUS...')
arquivos_estados = glob.glob('./datasets/mortalidade_estados/*.csv')

df_list = []
for f in arquivos_estados:
    with open(f, 'r', encoding='latin1') as file:
        linhas = file.readlines()
        
    pulos = 0
    for i, linha in enumerate(linhas):
        if "Munic" in linha and ";" in linha: 
            pulos = i
            break
            
    df_temp = pd.read_csv(f, sep=';', encoding='latin1', skiprows=pulos, skipfooter=2, engine='python')
    df_list.append(df_temp)

df_mort_evit = pd.concat(df_list, ignore_index=True)
df_mort_evit.rename(columns={df_mort_evit.columns[0]: 'id_municipio_str', df_mort_evit.columns[1]: 'total_obitos_evitaveis'}, inplace=True)
df_mort_evit['id_chave'] = df_mort_evit['id_municipio_str'].astype(str).str[:6]

print("Mortalidade consolidada com sucesso!")

# ==========================================
# CARREGAMENTO DAS OUTRAS FONTES
# ==========================================
print('Carregando IBGE, ANS e PIB...')

df_pop = pd.read_csv('./datasets/populacao_ibge_2022.csv')
df_pop['id_chave'] = df_pop['id_municipio'].astype(str).str[:6]

df_ans = pd.read_csv('./datasets/beneficiarios.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=2, engine='python')
df_ans.columns = ['id_municipio_str', 'total_beneficiarios']
df_ans['id_chave'] = df_ans['id_municipio_str'].astype(str).str[:6]

# === O TRATAMENTO DO PIB ===
# Lê o novo arquivo que você baixou do SIDRA
df_pib = pd.read_csv('./datasets/pib_municipios_ibge.csv', sep=';', skiprows=3, skipfooter=10, engine='python') 

# O IBGE empurra o valor financeiro (dinheiro) sempre para a ÚLTIMA coluna
coluna_valor = df_pib.columns[-1]

# Varrer a primeira ou segunda coluna para achar o Código de 7 dígitos e fatiar os 6 primeiros
col_codigo = df_pib.columns[0] if 'Cód' in df_pib.columns[0] else df_pib.columns[1]
df_pib['id_chave'] = df_pib[col_codigo].astype(str).str.extract(r'(\d+)')[0].str[:6]

# Pega a última coluna (o dinheiro), limpa possíveis pontos e vírgulas do padrão brasileiro, e converte para número matemático (Float)
df_pib['pib_per_capita'] = pd.to_numeric(
    df_pib[coluna_valor].astype(str).str.replace('.', '').str.replace(',', '.'), 
    errors='coerce'
)

# ==========================================
# MERGE (A GRANDE JUNÇÃO)
# ==========================================
print("Realizando os cruzamentos (Left Joins)...")
df_consol = pd.merge(df_pop, df_mort_evit[['id_chave', 'total_obitos_evitaveis']], on='id_chave', how='left')
df_consol = pd.merge(df_consol, df_ans[['id_chave', 'total_beneficiarios']], on='id_chave', how='left')
df_consol = pd.merge(df_consol, df_pib[['id_chave', 'pib_per_capita']], on='id_chave', how='left')

# ==========================================
#  ENGENHARIA DE FEATURES E EXPORTAÇÃO
# ==========================================
print("Tratando nulos e calculando novas métricas...")

df_consol['total_obitos_evitaveis'] = df_consol['total_obitos_evitaveis'].fillna(0)
df_consol['total_beneficiarios'] = df_consol['total_beneficiarios'].fillna(0)

df_consol['taxa_mortalidade_evitavel'] = (df_consol['total_obitos_evitaveis'] / df_consol['populacao']) * 100000
df_consol['perc_cobertura_saude'] = (df_consol['total_beneficiarios'] / df_consol['populacao']) * 100

# Salva a base 
df_consol.to_csv('./datasets/base_consolidada_saude.csv', index=False)

print('\nPipeline finalizada com sucesso! A Base V2 tá na mão.')
print(df_consol[['id_chave', 'populacao', 'taxa_mortalidade_evitavel', 'perc_cobertura_saude', 'pib_per_capita']].head())