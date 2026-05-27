import pandas as pd
from functools import reduce
from utils import remove_footer, split_id_name_unidade_federativa

def processar_leitos_mensais(caminho_arquivo, nome_valor):
    df = remove_footer(pd.read_csv(
        caminho_arquivo, 
        encoding='latin1', 
        sep=';', 
        header=3
    ))
    
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano_mes',
        value_name=nome_valor
    )
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df[nome_valor] = pd.to_numeric(df[nome_valor].replace('-', '0'), errors='coerce').fillna(0)
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'], as_index=False)[nome_valor].mean()
    df_agrupado[nome_valor] = df_agrupado[nome_valor].round().astype(int)
    
    return df_agrupado


def extrair_bloco_infraestrutura(caminhos_arquivos):

    print('\n[Módulo ETL Leitos] Extraindo e processando infraestrutura...')
    
    df_rep_fem = processar_leitos_mensais(caminhos_arquivos['repouso_fem'], 'leitos_repouso_fem')
    df_rep_masc = processar_leitos_mensais(caminhos_arquivos['repouso_masc'], 'leitos_repouso_masc')
    df_rep_ind = processar_leitos_mensais(caminhos_arquivos['repouso_ind'], 'leitos_repouso_ind')
    df_rep_ped = processar_leitos_mensais(caminhos_arquivos['repouso_ped'], 'leitos_repouso_ped')
    df_comp_nao_sus = processar_leitos_mensais(caminhos_arquivos['comp_nao_sus'], 'leitos_uti_nao_sus')
    df_comp_sus = processar_leitos_mensais(caminhos_arquivos['comp_sus'], 'leitos_uti_sus')
    df_enf_nao_sus = processar_leitos_mensais(caminhos_arquivos['enf_nao_sus'], 'leitos_enf_nao_sus')
    df_enf_sus = processar_leitos_mensais(caminhos_arquivos['enf_sus'], 'leitos_enf_sus')

    dfs_leitos = [
        df_rep_fem, df_rep_ind, df_rep_masc, df_rep_ped,
        df_comp_nao_sus, df_comp_sus, df_enf_nao_sus, df_enf_sus
    ]

    print('[Módulo ETL Leitos] Consolidando Bloco Físico...')
    df_bloco = reduce(
        lambda esquerda, direita: pd.merge(
            esquerda, 
            direita, 
            on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano'], 
            how='left'
            ), 
        dfs_leitos
    )

    return df_bloco
