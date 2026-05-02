import pandas as pd
import glob

def processar_dados_ano(ano):
    """
    Função que extrai, limpa e consolida os dados de um ano específico.
    """
    print(f'\n--- Iniciando processamento do ano: {ano} ---')

    # ==========================================
    # 1. CONSOLIDAÇÃO DO DATASUS
    # ==========================================
    arquivos_estados = glob.glob(f'./datasets/mortalidade_estados_{ano}/*.csv')
    
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

    # ==========================================
    # 2. CARREGAMENTO DAS OUTRAS FONTES
    # ==========================================
    # Lendo os arquivos das pastas baseadas no ano
    df_pop = pd.read_csv(f'./datasets/datasets{ano}/populacao_ibge_{ano}.csv')
    df_pop['id_chave'] = df_pop['id_municipio'].astype(str).str[:6]

    # Lendo ANS
    df_ans = pd.read_csv(f'./datasets/datasets{ano}/beneficiarios_{ano}.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=2, engine='python')
    
    # Pega estritamente as duas primeiras colunas (ignorando colunas extras fantasmas)
    df_ans = df_ans.iloc[:, :2] 
    
    # Agora podemos renomear com segurança
    df_ans.columns = ['id_municipio_str', 'total_beneficiarios']
    df_ans['id_chave'] = df_ans['id_municipio_str'].astype(str).str[:6]

    df_pib = pd.read_csv(f'./datasets/datasets{ano}/pib_municipios_ibge_{ano}.csv', sep=';', skiprows=3, skipfooter=10, engine='python') 
    
    coluna_valor = df_pib.columns[-1]
    col_codigo = df_pib.columns[0] if 'Cód' in df_pib.columns[0] else df_pib.columns[1]
    df_pib['id_chave'] = df_pib[col_codigo].astype(str).str.extract(r'(\d+)')[0].str[:6]
    
    df_pib['pib_per_capita'] = pd.to_numeric(
        df_pib[coluna_valor].astype(str).str.replace('.', '').str.replace(',', '.'), 
        errors='coerce'
    )

    # ==========================================
    # 3. MERGE (A GRANDE JUNÇÃO)
    # ==========================================
    df_consol = pd.merge(df_pop, df_mort_evit[['id_chave', 'total_obitos_evitaveis']], on='id_chave', how='left')
    df_consol = pd.merge(df_consol, df_ans[['id_chave', 'total_beneficiarios']], on='id_chave', how='left')
    df_consol = pd.merge(df_consol, df_pib[['id_chave', 'pib_per_capita']], on='id_chave', how='left')

    # ==========================================
    # 4. ENGENHARIA DE FEATURES
    # ==========================================
    df_consol['total_obitos_evitaveis'] = df_consol['total_obitos_evitaveis'].fillna(0)
    df_consol['total_beneficiarios'] = df_consol['total_beneficiarios'].fillna(0)

    df_consol['taxa_mortalidade_evitavel'] = (df_consol['total_obitos_evitaveis'] / df_consol['populacao']) * 100000
    df_consol['perc_cobertura_saude'] = (df_consol['total_beneficiarios'] / df_consol['populacao']) * 100
    
    # CRIANDO A COLUNA DO ANO (Crucial para o EDA)
    df_consol['ano'] = ano
    
    return df_consol

# ==========================================
# EXECUÇÃO PRINCIPAL DO PIPELINE
# ==========================================
if __name__ == "__main__":
    print('Iniciando pipeline de dados histórico...')
    
    # Lista de anos que queremos analisar
    anos_analise = ['2018', '2020', '2022']
    bases_anuais = []
    
    # Roda a nossa função para cada ano e guarda o resultado
    for ano in anos_analise:
        base_do_ano = processar_dados_ano(ano)
        bases_anuais.append(base_do_ano)
        
    print('\nEmpilhando todos os anos em um dataset mestre...')
    df_historico = pd.concat(bases_anuais, ignore_index=True)
    
    # Salva a super base histórica
    caminho_saida = './datasets/base_consolidada_saude_historico.csv'
    df_historico.to_csv(caminho_saida, index=False)
    
    print(f'Pipeline finalizada com sucesso! Base histórica salva em: {caminho_saida}')