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
    return df

def processar_leitos_repouso_masculino(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_masc')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_masc'] = df['leitos_repouso_masc'].fillna(0).astype(int)
    return df

def processar_leitos_repouso_indiferente(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_ind')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_ind'] = df['leitos_repouso_ind'].astype(int)
    return df

def processar_leitos_repouso_pediatria(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_repouso_ped')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_repouso_ped'] = df['leitos_repouso_ped'].astype(int)
    return df

def processar_leitos_complementares_nao_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_uti_nao_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_uti_nao_sus'] = df['leitos_uti_nao_sus'].astype(int)
    return df

def processar_leitos_complementares_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_uti_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_uti_sus'] = df['leitos_uti_sus'].astype(int)
    return df

def processar_leitos_enfermaria_nao_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_enf_nao_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_enf_nao_sus'] = df['leitos_enf_nao_sus'].astype(int)
    return df

def processar_leitos_enfermaria_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='leitos_enf_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['leitos_enf_sus'] = df['leitos_enf_sus'].astype(int)
    return df

# =====================================================================
# TRANSFORMAÇÃO ESTATÍSTICA
# =====================================================================

def aplicar_logica_estatistica(df, coluna_alvo):
    df_agg = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])[coluna_alvo].agg(['mean', 'median', 'std']).reset_index()
    
    df_agg = df_agg.rename(columns={
        'mean': f'media_{coluna_alvo}',
        'median': f'mediana_{coluna_alvo}',
        'std': f'desvio_padrao_{coluna_alvo}'
    })
    
    df_agg[f'media_{coluna_alvo}'] = df_agg[f'media_{coluna_alvo}'].round(2)
    df_agg[f'mediana_{coluna_alvo}'] = df_agg[f'mediana_{coluna_alvo}'].astype(int)
    df_agg[f'desvio_padrao_{coluna_alvo}'] = df_agg[f'desvio_padrao_{coluna_alvo}'].round(2)
    
    return df_agg


# =====================================================================
# MÓDULOS DE DOMÍNIO (Engenharia de Features Mensal)
# =====================================================================

def obter_estatisticas_repouso(caminho_fem, caminho_masc, caminho_ind, caminho_ped):
    df_fem = processar_leitos_repouso_feminino(caminho_fem)
    df_masc = processar_leitos_repouso_masculino(caminho_masc)
    df_ind = processar_leitos_repouso_indiferente(caminho_ind)
    df_ped = processar_leitos_repouso_pediatria(caminho_ped)

    # Junta os 4 Dataframes mês a mês
    df_merge1 = pd.merge(df_fem, df_masc, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    df_merge2 = pd.merge(df_merge1, df_ind, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    df_par = pd.merge(df_merge2, df_ped, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')

    #  Soma os leitos mensalmente ANTES de extrair a estatística
    df_par['total_leitos_repouso'] = df_par['leitos_repouso_fem'] + df_par['leitos_repouso_masc'] + df_par['leitos_repouso_ind'] + df_par['leitos_repouso_ped']

    # Gera as tabelas isoladas
    est_fem = aplicar_logica_estatistica(df_par, 'leitos_repouso_fem')
    est_masc = aplicar_logica_estatistica(df_par, 'leitos_repouso_masc')
    est_ind = aplicar_logica_estatistica(df_par, 'leitos_repouso_ind')
    est_ped = aplicar_logica_estatistica(df_par, 'leitos_repouso_ped')
    est_tot = aplicar_logica_estatistica(df_par, 'total_leitos_repouso')

    return est_fem, est_masc, est_ind, est_ped, est_tot

def obter_estatisticas_internacao_nao_sus(caminho_uti, caminho_enf):
    df_uti = processar_leitos_complementares_nao_sus(caminho_uti)
    df_enf = processar_leitos_enfermaria_nao_sus(caminho_enf)

    df_par = pd.merge(df_uti, df_enf, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    
    # Resolvendo o problema de nomenclatura
    df_par['leitos_internacao_nao_sus'] = df_par['leitos_uti_nao_sus'] + df_par['leitos_enf_nao_sus']

    est_uti = aplicar_logica_estatistica(df_par, 'leitos_uti_nao_sus')
    est_enf = aplicar_logica_estatistica(df_par, 'leitos_enf_nao_sus')
    est_tot = aplicar_logica_estatistica(df_par, 'leitos_internacao_nao_sus')

    return est_uti, est_enf, est_tot

def obter_estatisticas_internacao_sus(caminho_uti, caminho_enf):
    df_uti = processar_leitos_complementares_sus(caminho_uti)
    df_enf = processar_leitos_enfermaria_sus(caminho_enf)

    df_par = pd.merge(df_uti, df_enf, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    
    # Resolvendo o problema de nomenclatura 
    df_par['leitos_internacao_sus'] = df_par['leitos_uti_sus'] + df_par['leitos_enf_sus']

    est_uti = aplicar_logica_estatistica(df_par, 'leitos_uti_sus')
    est_enf = aplicar_logica_estatistica(df_par, 'leitos_enf_sus')
    est_tot = aplicar_logica_estatistica(df_par, 'leitos_internacao_sus')

    return est_uti, est_enf, est_tot


# =====================================================================
# CONSOLIDAÇÃO DO BLOCO DE LEITOS
# =====================================================================

def extrair_bloco_infraestrutura(caminhos_arquivos):
    print('\n[Módulo ETL Leitos] Extraindo e processando infraestrutura...')
    
    df_rep_fem, df_rep_masc, df_rep_ind, df_rep_ped, df_rep_tot = obter_estatisticas_repouso(
        caminhos_arquivos['repouso_fem'],
        caminhos_arquivos['repouso_masc'],
        caminhos_arquivos['repouso_ind'],
        caminhos_arquivos['repouso_ped']
    )
    
    df_uti_nao_sus, df_enf_nao_sus, df_int_nao_sus = obter_estatisticas_internacao_nao_sus(
        caminhos_arquivos['comp_nao_sus'],
        caminhos_arquivos['enf_nao_sus']
    )
    
    df_uti_sus, df_enf_sus, df_int_sus = obter_estatisticas_internacao_sus(
        caminhos_arquivos['comp_sus'],
        caminhos_arquivos['enf_sus']
    )

    dfs_leitos = [
        df_rep_fem, df_rep_masc, df_rep_ind, df_rep_ped, df_rep_tot,
        df_uti_nao_sus, df_enf_nao_sus, df_int_nao_sus,
        df_uti_sus, df_enf_sus, df_int_sus
    ]

    print('[Módulo ETL Leitos] Consolidando Bloco Físico...')
    df_bloco = reduce(
        lambda esquerda, direita: pd.merge(
            esquerda, direita, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano'], how='outer'
        ), dfs_leitos 
    )
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

    