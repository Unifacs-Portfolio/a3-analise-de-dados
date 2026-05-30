import pandas as pd
from functools import reduce
from utils.utils import remove_footer, split_id_name_unidade_federativa, inspecionar_dados

# =====================================================================
# FUNÇÕES DE ETL INDIVIDUAIS PARA CADA TIPO DE LEITO
# =====================================================================

def processar_leitos_repouso_feminino(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_fem')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_fem'] = df['leitos_repouso_fem'].fillna(0).astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_repouso_fem'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_repouso_fem',
        'median': 'mediana_leitos_repouso_fem', 
        'std': 'desvio_padrao_leitos_repouso_fem'
        })
    
    df_agrupado['media_leitos_repouso_fem'] = df_agrupado['media_leitos_repouso_fem'].round().astype(int)
    df_agrupado['mediana_leitos_repouso_fem'] = df_agrupado['mediana_leitos_repouso_fem'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_repouso_fem'] = df_agrupado['desvio_padrao_leitos_repouso_fem'].round(2)
    return df_agrupado

def processar_leitos_repouso_masculino(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_masc')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_masc'] = df['leitos_repouso_masc'].fillna(0).astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_repouso_masc'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_repouso_masc',
        'median': 'mediana_leitos_repouso_masc', 
        'std': 'desvio_padrao_leitos_repouso_masc'
        })
    
    df_agrupado['media_leitos_repouso_masc'] = df_agrupado['media_leitos_repouso_masc'].round().astype(int)
    df_agrupado['mediana_leitos_repouso_masc'] = df_agrupado['mediana_leitos_repouso_masc'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_repouso_masc'] = df_agrupado['desvio_padrao_leitos_repouso_masc'].round(2)
    return df_agrupado

def processar_leitos_repouso_indiferente(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_ind')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_ind'] = df['leitos_repouso_ind'].astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_repouso_ind'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_repouso_ind',
        'median': 'mediana_leitos_repouso_ind', 
        'std': 'desvio_padrao_leitos_repouso_ind'
        })
    
    df_agrupado['media_leitos_repouso_ind'] = df_agrupado['media_leitos_repouso_ind'].round().astype(int)
    df_agrupado['mediana_leitos_repouso_ind'] = df_agrupado['mediana_leitos_repouso_ind'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_repouso_ind'] = df_agrupado['desvio_padrao_leitos_repouso_ind'].round(2)
    return df_agrupado

def processar_leitos_repouso_pediatria(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_ped')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_ped'] = df['leitos_repouso_ped'].astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_repouso_ped'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_repouso_ped', 
        'median': 'mediana_leitos_repouso_ped',
        'std': 'desvio_padrao_leitos_repouso_ped'
        })
    
    df_agrupado['media_leitos_repouso_ped'] = df_agrupado['media_leitos_repouso_ped'].round().astype(int)
    df_agrupado['mediana_leitos_repouso_ped'] = df_agrupado['mediana_leitos_repouso_ped'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_repouso_ped'] = df_agrupado['desvio_padrao_leitos_repouso_ped'].round(2)
    return df_agrupado

def processar_leitos_complementares_nao_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_uti_nao_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_uti_nao_sus'] = df['leitos_uti_nao_sus'].astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_uti_nao_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_uti_nao_sus',
        'median': 'mediana_leitos_uti_nao_sus', 
        'std': 'desvio_padrao_leitos_uti_nao_sus'
        })
    
    df_agrupado['media_leitos_uti_nao_sus'] = df_agrupado['media_leitos_uti_nao_sus'].round().astype(int)
    df_agrupado['mediana_leitos_uti_nao_sus'] = df_agrupado['mediana_leitos_uti_nao_sus'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_uti_nao_sus'] = df_agrupado['desvio_padrao_leitos_uti_nao_sus'].round(2)
    return df_agrupado

def processar_leitos_complementares_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_uti_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_uti_sus'] = df['leitos_uti_sus'].astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_uti_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_uti_sus',
        'median': 'mediana_leitos_uti_sus', 
        'std': 'desvio_padrao_leitos_uti_sus'
        })
    
    df_agrupado['media_leitos_uti_sus'] = df_agrupado['media_leitos_uti_sus'].round().astype(int)
    df_agrupado['mediana_leitos_uti_sus'] = df_agrupado['mediana_leitos_uti_sus'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_uti_sus'] = df_agrupado['desvio_padrao_leitos_uti_sus'].round(2)
    return df_agrupado

def processar_leitos_enfermaria_nao_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_enf_nao_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_enf_nao_sus'] = df['leitos_enf_nao_sus'].astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_enf_nao_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_enf_nao_sus', 
        'median': 'mediana_leitos_enf_nao_sus',
        'std': 'desvio_padrao_leitos_enf_nao_sus'
        })
    
    df_agrupado['media_leitos_enf_nao_sus'] = df_agrupado['media_leitos_enf_nao_sus'].round().astype(int)
    df_agrupado['mediana_leitos_enf_nao_sus'] = df_agrupado['mediana_leitos_enf_nao_sus'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_enf_nao_sus'] = df_agrupado['desvio_padrao_leitos_enf_nao_sus'].round(2)
    return df_agrupado

def processar_leitos_enfermaria_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_enf_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_enf_sus'] = df['leitos_enf_sus'].astype(int)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['leitos_enf_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_leitos_enf_sus', 
        'median': 'mediana_leitos_enf_sus',
        'std': 'desvio_padrao_leitos_enf_sus'
        })
    
    df_agrupado['media_leitos_enf_sus'] = df_agrupado['media_leitos_enf_sus'].round().astype(int)
    df_agrupado['mediana_leitos_enf_sus'] = df_agrupado['mediana_leitos_enf_sus'].round().astype(int)
    df_agrupado['desvio_padrao_leitos_enf_sus'] = df_agrupado['desvio_padrao_leitos_enf_sus'].round(2)
    return df_agrupado


# =====================================================================
# CONSOLIDAÇÃO DO BLOCO DE LEITOS
# =====================================================================

def extrair_bloco_infraestrutura(caminhos_arquivos):
    print('\n[Módulo ETL Leitos] Extraindo e processando infraestrutura...')
    
    df_rep_fem = processar_leitos_repouso_feminino(caminhos_arquivos['repouso_fem'])
    df_rep_masc = processar_leitos_repouso_masculino(caminhos_arquivos['repouso_masc'])
    df_rep_ind = processar_leitos_repouso_indiferente(caminhos_arquivos['repouso_ind'])
    df_rep_ped = processar_leitos_repouso_pediatria(caminhos_arquivos['repouso_ped'])
    
    df_comp_nao_sus = processar_leitos_complementares_nao_sus(caminhos_arquivos['comp_nao_sus'])
    df_comp_sus = processar_leitos_complementares_sus(caminhos_arquivos['comp_sus'])
    
    df_enf_nao_sus = processar_leitos_enfermaria_nao_sus(caminhos_arquivos['enf_nao_sus'])
    df_enf_sus = processar_leitos_enfermaria_sus(caminhos_arquivos['enf_sus'])


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
            how='outer'
            ), 
        dfs_leitos 
    )
    
    # ENGENHARIA DE FEATURES: Cálculo das Médias
    df_bloco['media_total_leitos_repouso'] = df_bloco['media_leitos_repouso_fem'] + df_bloco['media_leitos_repouso_ind'] + df_bloco['media_leitos_repouso_masc'] + df_bloco['media_leitos_repouso_ped']
    df_bloco['media_total_leitos_sus'] = df_bloco['media_leitos_uti_sus'] + df_bloco['media_leitos_enf_sus']
    df_bloco['media_total_leitos_nao_sus'] = df_bloco['media_leitos_uti_nao_sus'] + df_bloco['media_leitos_enf_nao_sus']

    # ENGENHARIA DE FEATURES: Cálculo das Medianas 
    df_bloco['mediana_total_leitos_repouso'] = df_bloco['mediana_leitos_repouso_fem'] + df_bloco['mediana_leitos_repouso_ind'] + df_bloco['mediana_leitos_repouso_masc'] + df_bloco['mediana_leitos_repouso_ped']
    df_bloco['mediana_total_leitos_sus'] = df_bloco['mediana_leitos_uti_sus'] + df_bloco['mediana_leitos_enf_sus']
    df_bloco['mediana_total_leitos_nao_sus'] = df_bloco['mediana_leitos_uti_nao_sus'] + df_bloco['mediana_leitos_enf_nao_sus']

    # ENGENHARIA DE FEATURES: Cálculo dos Desvios Padrão (Raiz Quadrada da Soma das Variâncias)
    df_bloco['desvio_padrao_total_leitos_repouso'] = ((df_bloco['desvio_padrao_leitos_repouso_fem']**2 + df_bloco['desvio_padrao_leitos_repouso_ind']**2 + df_bloco['desvio_padrao_leitos_repouso_masc']**2 + df_bloco['desvio_padrao_leitos_repouso_ped']**2) ** 0.5).round(2)
    df_bloco['desvio_padrao_total_leitos_sus'] = ((df_bloco['desvio_padrao_leitos_uti_sus']**2 + df_bloco['desvio_padrao_leitos_enf_sus']**2) ** 0.5).round(2)
    df_bloco['desvio_padrao_total_leitos_nao_sus'] = ((df_bloco['desvio_padrao_leitos_uti_nao_sus']**2 + df_bloco['desvio_padrao_leitos_enf_nao_sus']**2) ** 0.5).round(2)

    return df_bloco


# ISSO AQUI É SO PRA CASO QUERIA SO RODAR O python ETL_LEITOS.PY PRA VER ESSAS TABELAS sem rodar o main.py
if __name__ == "__main__": 
    #caminhos dos arquivos de leitos
    caminhos_leitos = {
        'repouso_fem': './datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_feminino.csv',
        'repouso_ind': './datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_indiferente.csv',
        'repouso_masc': './datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_masculino.csv',
        'repouso_ped': './datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_pediatria.csv',

        'comp_nao_sus': './datasets/datasus_cnes/leitos_complementares_nao_sus.csv',
        'comp_sus': './datasets/datasus_cnes/leitos_complementares_sus.csv',
        'enf_nao_sus': './datasets/datasus_cnes/leitos_enfermaria_nao_sus.csv',
        'enf_sus': './datasets/datasus_cnes/leitos_enfermaria_sus.csv'
    }

    df_blocos_leitos = extrair_bloco_infraestrutura(caminhos_leitos)

    