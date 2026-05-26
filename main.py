import pandas as pd
import glob
import os
from functools import reduce

def remove_footer(df):
    filtro_total = df.iloc[:, 0].astype(str).str.contains('Total', case=False, na=False)
    indices = df[df[df.columns[1]] == 'Distrito Federal'].index
    if filtro_total.any():
        df = df.iloc[:filtro_total.idxmax()]
    elif not indices.empty:
        indice_final = indices[0]
        df = df.loc[:indice_final]
    return df
def split_id_name_unidade_federativa(df, nome_coluna):
    campos = df[nome_coluna].astype(str).str.extract(r'^\s*(\d{2})\s*(.*)')
    df['id_unidade_federativa'] = campos[0]
    df['nome_unidade_federativa'] = campos[1]
    return df
def processar_datasus_internacoes(caminho_arquivo):
    df = remove_footer(pd.read_csv(
        caminho_arquivo, 
        encoding='latin1', 
        sep=';', 
        header=3
    ))
    df = df.drop(columns=['Total', '2017', '2019', '2020', '2024', '2025', '2026'])
    df = df.rename(columns={
        df.columns[0]: 'unidade_federativa',
    })
    colunas_alvo = df.columns[1:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano',
        value_name='internacoes'
    )
    return df
def processar_datasus_dias_permanencia(caminho_arquivo):
    df = remove_footer(pd.read_csv(
        caminho_arquivo, 
        encoding='latin1', 
        header=3, 
        sep=';',
        usecols=['Unidade da Federação', '2018', '2021', '2022', '2023']
    ))
    df = df.rename(columns={
        df.columns[0]: 'unidade_federativa',
    })
    colunas_alvo = df.columns[1:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano',
        value_name='dias_internacao'
    )
    return df
def processar_dataset_gini(caminho_arquivo):
    df = remove_footer(pd.read_csv(
        caminho_arquivo, 
        sep=';', 
        header=3,
        decimal=','
    ))
    df = df.rename(columns={
        df.columns[0]: 'id_unidade_federativa',
        df.columns[1]: 'nome_unidade_federativa'
    })
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano',
        value_name='indice_gini'
    )
    return df
def processar_dataset_renda_capita(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, header=3, sep=';'))
    df = df.rename(columns={
        df.columns[0]: 'id_unidade_federativa',
        df.columns[1]: 'nome_unidade_federativa'
    })
    colunas_alvo = df.columns[2:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano',
        value_name='renda_per_capita'
    )
    return df
def processar_dataset_pib(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, header=3, sep=';', decimal=','))
    df = df.rename(columns={
        df.columns[0]: 'id_unidade_federativa',
        df.columns[1]: 'nome_unidade_federativa'
    })
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano',
        value_name='pib_milhares'
    )
    return df
def processar_datasus_obitos(caminho_arquivo):
    df = remove_footer(pd.read_csv(
        caminho_arquivo, 
        encoding='latin1', 
        header=3, 
        sep=';',
        usecols=['Unidade da Federação', '2018', '2021', '2022', '2023']
    ))
    df = df.rename(columns={
        df.columns[0]: 'unidade_federativa',
    })
    colunas_alvo = df.columns[1:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(
        id_vars=['id_unidade_federativa', 'nome_unidade_federativa'],
        var_name='ano',
        value_name='obitos_hospitalares'
    )
    return df
print('Iniciando processamento das matrizes históricas (Raiz)...')
df_internacoes = processar_datasus_internacoes('./datasets/morbidade_hospitalar_sus/internacoes.csv')
df_permanencia = processar_datasus_dias_permanencia('./datasets/morbidade_hospitalar_sus/dias_permanencia.csv')
df_gini = processar_dataset_gini('./datasets/datasets_juntos/indice_gini.csv')
df_renda = processar_dataset_renda_capita('./datasets/datasets_juntos/renda_per_capita.csv')
df_pib = processar_dataset_pib('./datasets/datasets_juntos/pib_corrente.csv')
df_obitos_hospitalares = processar_datasus_obitos('./datasets/morbidade_hospitalar_sus/obitos_hospitalares.csv')

dfs = [df_permanencia, df_gini, df_renda, df_pib, df_internacoes, df_obitos_hospitalares]
df_consolidado = reduce(
    lambda esquerda, direita: pd.merge(
        esquerda, 
        direita, 
        on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano'], 
        how='left'
    ), 
    dfs
)
print(df_consolidado.dtypes)