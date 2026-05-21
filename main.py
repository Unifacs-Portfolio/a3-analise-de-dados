import pandas as pd
import glob
from functools import reduce

def remove_footer(df):
    filtro_total = df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)
    if filtro_total.any():
        df = df.iloc[:filtro_total.idxmax()]
    return df
def processar_dados_ano(ano):
    """
    Função que extrai, limpa e consolida os dados de um ano específico.
    """
    print(f'\n--- Iniciando processamento do ano: {ano} ---')

    arquivos_estados = glob.glob(f'./datasets/mortalidade_estados_{ano}/*.csv')
    
    lista_dfs = [
        remove_footer(pd.read_csv(
            arquivo, 
            encoding='latin1', 
            sep=';', 
            header=3,
            names=['municipio', 'obitos_por_residencia']
        )) 
        for arquivo in arquivos_estados
    ]
    df_mort_evit = pd.concat(lista_dfs, ignore_index=True)
    df_mort_evit[['id_municipio', 'nome_municipio']] = df_mort_evit['municipio'].astype(str).str.split(r'^\s*(\d{6})\s+', expand=True).iloc[:, 1:3]
    df_mort_evit = df_mort_evit.drop(columns=['municipio'])

    df_pop = pd.read_csv(f'./datasets/datasets{ano}/populacao_ibge_{ano}.csv')
    df_pop['id_municipio'] = df_pop['id_municipio'].astype(str).str[:6]
    
    df_ans = remove_footer(pd.read_csv(
        f'./datasets/datasets{ano}/beneficiarios_{ano}.csv', 
        encoding='latin1', 
        sep=';', 
        header=3, 
        usecols=[0, 1], 
        names=['municipio', 'beneficiarios_ans']
    ))
    df_ans[['id_municipio', 'nome_municipio']] = df_ans['municipio'].astype(str).str.split(r'^\s*(\d{6})\s+', expand=True).iloc[:, 1:3]
    df_ans = df_ans.drop(columns=['municipio'])
    
    df_pib = pd.read_csv(
        f'./datasets/datasets{ano}/pib_municipios_ibge_{ano}.csv', 
        sep=';', 
        header=3, 
        decimal=',',
        names=['id_municipio', 'nome_municipio', 'pib_milhares']
    ) 
    df_pib['id_municipio'] = df_pib['id_municipio'].astype(str).str[:6]
    
    print(df_mort_evit)
    df_mort_evit.info()
    print()
    
    print(df_pop)
    df_pop.info()
    print()
    
    print(df_ans)
    df_ans.info()
    print()
    
    print(df_pib)
    df_pib.info()
    
    print('\nValores Nulos:')
    print(df_mort_evit.isna().sum())
    
    print('\nValores Nulos:')
    print(df_pop.isna().sum())
    
    print('\nValores Nulos:')
    print(df_ans.isna().sum())
    
    print('\nValores Nulos:')
    print(df_pib.isna().sum())

    fila_de_dados = [
        df_pop,
        df_pib[['id_municipio', 'pib_milhares']],
        df_ans[['id_municipio', 'beneficiarios_ans']],
        df_mort_evit[['id_municipio', 'obitos_por_residencia']]
    ]
    df_consolidado = reduce(
        lambda left, right: pd.merge(left, right, on='id_municipio', how='left'), 
        fila_de_dados
    )
    print(df_consolidado)
    df_consolidado.info()
    df_consolidado['beneficiarios_ans'] = df_consolidado['beneficiarios_ans'].fillna(0).astype(int)
    df_consolidado['obitos_por_residencia'] = df_consolidado['obitos_por_residencia'].fillna(0).astype(int)
    df_consolidado.info()
    print("\n--- Verificando o Município sem PIB ---")
    print(df_consolidado[df_consolidado['pib_milhares'].isna()])
    df_consolidado = df_consolidado.dropna(subset=['pib_milhares'])
    
    print(f"Total de municípios consistentes: {len(df_consolidado)}")
    
    df_consolidado['taxa_mortalidade_evitavel'] = (df_consolidado['obitos_por_residencia'] / df_consolidado['populacao']) * 100000
    df_consolidado['perc_cobertura_saude'] = (df_consolidado['beneficiarios_ans'] / df_consolidado['populacao']) * 100
    df_consolidado['ano'] = int(ano)
    print(df_consolidado)
    df_consolidado.info()
    print(f"\n--- ANO {ano} CONSOLIDADO COM SUCESSO! ---")
    return df_consolidado

if __name__ == "__main__":
    print('Iniciando pipeline de dados histórico...')
    
    anos_analise = ['2018', '2020', '2022']
    bases_anuais = []
    
    for ano in anos_analise:
        base_do_ano = processar_dados_ano(ano)
        bases_anuais.append(base_do_ano)
        
    print('\nEmpilhando todos os anos em um dataset mestre...')
    df_historico = pd.concat(bases_anuais, ignore_index=True)
    
    caminho_saida = './datasets/base_consolidada_saude_historico.csv'
    print(df_historico.tail(10))
    df_historico.info()
    print(df_historico.describe(include='all'))
    df_historico.to_csv(caminho_saida, index=False)
    
    print(f'Pipeline finalizada com sucesso! Base histórica salva em: {caminho_saida}')