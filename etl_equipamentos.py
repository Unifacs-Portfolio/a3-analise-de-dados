import pandas as pd
from functools import reduce
from utils import remove_footer, split_id_name_unidade_federativa, inspecionar_dados

# =====================================================================
# FUNÇÕES DIAGNÓSTICO POR IMAGEM
# =====================================================================

def processar_equip_diagnostico_imagem(caminho_total, caminho_sus):
    # CSV ORIGINAL (NAO SUS)
    df_total = remove_footer(pd.read_csv(caminho_total, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df_total = df_total.drop(columns=['Total'], errors='ignore')
    df_total = df_total.rename(columns={df_total.columns[0]: 'unidade_federativa'})
    df_total = split_id_name_unidade_federativa(df_total, 'unidade_federativa')
    df_total = df_total.drop(columns=['unidade_federativa'])
    df_total = df_total.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_diag_imagem_total')
    df_total['equip_diag_imagem_total'] = pd.to_numeric(df_total['equip_diag_imagem_total'], errors='coerce').fillna(0)

    # CSV SUS 
    df_sus = remove_footer(pd.read_csv(caminho_sus, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df_sus = df_sus.drop(columns=['Total'], errors='ignore')
    df_sus = df_sus.rename(columns={df_sus.columns[0]: 'unidade_federativa'})
    df_sus = split_id_name_unidade_federativa(df_sus, 'unidade_federativa')
    df_sus = df_sus.drop(columns=['unidade_federativa'])
    df_sus = df_sus.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_diag_imagem_sus')
    df_sus['equip_diag_imagem_sus'] = pd.to_numeric(df_sus['equip_diag_imagem_sus'], errors='coerce').fillna(0)

    # Onde acontece a diferença entre os dois
    df_par = pd.merge(df_total, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes'], how='inner')
    df_par['equip_diag_imagem_nao_sus'] = df_par['equip_diag_imagem_total'] - df_par['equip_diag_imagem_sus']
    df_par['ano'] = df_par['ano_mes'].str.split('/').str[0]

    df_agrupado = df_par.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_diag_imagem_nao_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_diag_imagem_nao_sus',
        'median': 'mediana_equip_diag_imagem_nao_sus', 
        'std': 'desvio_padrao_equip_diag_imagem_nao_sus'
    })

    df_agrupado['media_equip_diag_imagem_nao_sus'] = df_agrupado['media_equip_diag_imagem_nao_sus'].round().astype(int)
    df_agrupado['mediana_equip_diag_imagem_nao_sus'] = df_agrupado['mediana_equip_diag_imagem_nao_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_diag_imagem_nao_sus'] = df_agrupado['desvio_padrao_equip_diag_imagem_nao_sus'].fillna(0).round(2)
    return df_agrupado

def processar_equip_diagnostico_imagem_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_diag_imagem_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_diag_imagem_sus'] = pd.to_numeric(df['equip_diag_imagem_sus'], errors='coerce').fillna(0)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_diag_imagem_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_diag_imagem_sus',
        'median': 'mediana_equip_diag_imagem_sus', 
        'std': 'desvio_padrao_equip_diag_imagem_sus'
    })
    
    df_agrupado['media_equip_diag_imagem_sus'] = df_agrupado['media_equip_diag_imagem_sus'].round().astype(int)
    df_agrupado['mediana_equip_diag_imagem_sus'] = df_agrupado['mediana_equip_diag_imagem_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_diag_imagem_sus'] = df_agrupado['desvio_padrao_equip_diag_imagem_sus'].fillna(0).round(2)
    return df_agrupado


# =====================================================================
# FUNÇÕES EQUIPAMENTOS TOTAIS
# =====================================================================

def processar_equip_totais(caminho_total, caminho_sus):
    # CSV ORIGINAL (NAO SUS)
    df_total = remove_footer(pd.read_csv(caminho_total, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df_total = df_total.drop(columns=['Total'], errors='ignore')
    df_total = df_total.rename(columns={df_total.columns[0]: 'unidade_federativa'})
    df_total = split_id_name_unidade_federativa(df_total, 'unidade_federativa')
    df_total = df_total.drop(columns=['unidade_federativa'])
    df_total = df_total.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_totais_total')
    df_total['equip_totais_total'] = pd.to_numeric(df_total['equip_totais_total'], errors='coerce').fillna(0)

    # CSV SUS
    df_sus = remove_footer(pd.read_csv(caminho_sus, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df_sus = df_sus.drop(columns=['Total'], errors='ignore')
    df_sus = df_sus.rename(columns={df_sus.columns[0]: 'unidade_federativa'})
    df_sus = split_id_name_unidade_federativa(df_sus, 'unidade_federativa')
    df_sus = df_sus.drop(columns=['unidade_federativa'])
    df_sus = df_sus.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_totais_sus')
    df_sus['equip_totais_sus'] = pd.to_numeric(df_sus['equip_totais_sus'], errors='coerce').fillna(0)

    # Onde acontece a diferença entre os dois
    df_par = pd.merge(df_total, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes'], how='inner')
    df_par['equip_totais_nao_sus'] = df_par['equip_totais_total'] - df_par['equip_totais_sus']
    df_par['ano'] = df_par['ano_mes'].str.split('/').str[0]

    df_agrupado = df_par.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_totais_nao_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_totais_nao_sus',
        'median': 'mediana_equip_totais_nao_sus', 
        'std': 'desvio_padrao_equip_totais_nao_sus'
    })

    df_agrupado['media_equip_totais_nao_sus'] = df_agrupado['media_equip_totais_nao_sus'].round().astype(int)
    df_agrupado['mediana_equip_totais_nao_sus'] = df_agrupado['mediana_equip_totais_nao_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_totais_nao_sus'] = df_agrupado['desvio_padrao_equip_totais_nao_sus'].fillna(0).round(2)
    return df_agrupado

def processar_equip_totais_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_totais_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_totais_sus'] = pd.to_numeric(df['equip_totais_sus'], errors='coerce').fillna(0)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_totais_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_totais_sus',
        'median': 'mediana_equip_totais_sus', 
        'std': 'desvio_padrao_equip_totais_sus'
    })
    
    df_agrupado['media_equip_totais_sus'] = df_agrupado['media_equip_totais_sus'].round().astype(int)
    df_agrupado['mediana_equip_totais_sus'] = df_agrupado['mediana_equip_totais_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_totais_sus'] = df_agrupado['desvio_padrao_equip_totais_sus'].fillna(0).round(2)
    return df_agrupado


# =====================================================================
# FUNÇÕES MANUTENÇÃO DA VIDA
# =====================================================================

def processar_equip_manutencao_vida(caminho_total, caminho_sus):
    # CSV ORIGINAL (NAO SUS)
    df_total = remove_footer(pd.read_csv(caminho_total, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df_total = df_total.drop(columns=['Total'], errors='ignore')
    df_total = df_total.rename(columns={df_total.columns[0]: 'unidade_federativa'})
    df_total = split_id_name_unidade_federativa(df_total, 'unidade_federativa')
    df_total = df_total.drop(columns=['unidade_federativa'])
    df_total = df_total.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_manut_vida_total')
    df_total['equip_manut_vida_total'] = pd.to_numeric(df_total['equip_manut_vida_total'], errors='coerce').fillna(0)

    # CSV SUS
    df_sus = remove_footer(pd.read_csv(caminho_sus, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df_sus = df_sus.drop(columns=['Total'], errors='ignore')
    df_sus = df_sus.rename(columns={df_sus.columns[0]: 'unidade_federativa'})
    df_sus = split_id_name_unidade_federativa(df_sus, 'unidade_federativa')
    df_sus = df_sus.drop(columns=['unidade_federativa'])
    df_sus = df_sus.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_manut_vida_sus')
    df_sus['equip_manut_vida_sus'] = pd.to_numeric(df_sus['equip_manut_vida_sus'], errors='coerce').fillna(0)

    # Onde acontece a diferença entre os dois
    df_par = pd.merge(df_total, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes'], how='inner')
    df_par['equip_manut_vida_nao_sus'] = df_par['equip_manut_vida_total'] - df_par['equip_manut_vida_sus']
    df_par['ano'] = df_par['ano_mes'].str.split('/').str[0]

    df_agrupado = df_par.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_manut_vida_nao_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_manut_vida_nao_sus',
        'median': 'mediana_equip_manut_vida_nao_sus', 
        'std': 'desvio_padrao_equip_manut_vida_nao_sus'
    })

    df_agrupado['media_equip_manut_vida_nao_sus'] = df_agrupado['media_equip_manut_vida_nao_sus'].round().astype(int)
    df_agrupado['mediana_equip_manut_vida_nao_sus'] = df_agrupado['mediana_equip_manut_vida_nao_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_manut_vida_nao_sus'] = df_agrupado['desvio_padrao_equip_manut_vida_nao_sus'].fillna(0).round(2)
    return df_agrupado

def processar_equip_manutencao_vida_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_manut_vida_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_manut_vida_sus'] = pd.to_numeric(df['equip_manut_vida_sus'], errors='coerce').fillna(0)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_manut_vida_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_manut_vida_sus',
        'median': 'mediana_equip_manut_vida_sus', 
        'std': 'desvio_padrao_equip_manut_vida_sus'
    })
    
    df_agrupado['media_equip_manut_vida_sus'] = df_agrupado['media_equip_manut_vida_sus'].round().astype(int)
    df_agrupado['mediana_equip_manut_vida_sus'] = df_agrupado['mediana_equip_manut_vida_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_manut_vida_sus'] = df_agrupado['desvio_padrao_equip_manut_vida_sus'].fillna(0).round(2)
    return df_agrupado


# =====================================================================
# FUNÇÕES MÉTODOS GRÁFICOS
# =====================================================================

def processar_equip_metodos_graficos(caminho_total, caminho_sus):
    # CSV ORIGINAL (NAO SUS)
    df_total = remove_footer(pd.read_csv(caminho_total, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df_total = df_total.drop(columns=['Total'], errors='ignore')
    df_total = df_total.rename(columns={df_total.columns[0]: 'unidade_federativa'})
    df_total = split_id_name_unidade_federativa(df_total, 'unidade_federativa')
    df_total = df_total.drop(columns=['unidade_federativa'])
    df_total = df_total.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_met_graficos_total')
    df_total['equip_met_graficos_total'] = pd.to_numeric(df_total['equip_met_graficos_total'], errors='coerce').fillna(0)

    # CSV SUS
    df_sus = remove_footer(pd.read_csv(caminho_sus, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df_sus = df_sus.drop(columns=['Total'], errors='ignore')
    df_sus = df_sus.rename(columns={df_sus.columns[0]: 'unidade_federativa'})
    df_sus = split_id_name_unidade_federativa(df_sus, 'unidade_federativa')
    df_sus = df_sus.drop(columns=['unidade_federativa'])
    df_sus = df_sus.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_met_graficos_sus')
    df_sus['equip_met_graficos_sus'] = pd.to_numeric(df_sus['equip_met_graficos_sus'], errors='coerce').fillna(0)

    # Onde acontece a diferença entre os dois
    df_par = pd.merge(df_total, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes'], how='inner')
    df_par['equip_met_graficos_nao_sus'] = df_par['equip_met_graficos_total'] - df_par['equip_met_graficos_sus']
    df_par['ano'] = df_par['ano_mes'].str.split('/').str[0]

    df_agrupado = df_par.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_met_graficos_nao_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_met_graficos_nao_sus',
        'median': 'mediana_equip_met_graficos_nao_sus', 
        'std': 'desvio_padrao_equip_met_graficos_nao_sus'
    })

    df_agrupado['media_equip_met_graficos_nao_sus'] = df_agrupado['media_equip_met_graficos_nao_sus'].round().astype(int)
    df_agrupado['mediana_equip_met_graficos_nao_sus'] = df_agrupado['mediana_equip_met_graficos_nao_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_met_graficos_nao_sus'] = df_agrupado['desvio_padrao_equip_met_graficos_nao_sus'].fillna(0).round(2)
    return df_agrupado

def processar_equip_metodos_graficos_sus(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_met_graficos_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_met_graficos_sus'] = pd.to_numeric(df['equip_met_graficos_sus'], errors='coerce').fillna(0)
    
    df_agrupado = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])['equip_met_graficos_sus'].agg(['mean', 'median', 'std']).reset_index()
    
    df_agrupado = df_agrupado.rename(columns={
        'mean': 'media_equip_met_graficos_sus',
        'median': 'mediana_equip_met_graficos_sus', 
        'std': 'desvio_padrao_equip_met_graficos_sus'
    })
    
    df_agrupado['media_equip_met_graficos_sus'] = df_agrupado['media_equip_met_graficos_sus'].round().astype(int)
    df_agrupado['mediana_equip_met_graficos_sus'] = df_agrupado['mediana_equip_met_graficos_sus'].round().astype(int)
    df_agrupado['desvio_padrao_equip_met_graficos_sus'] = df_agrupado['desvio_padrao_equip_met_graficos_sus'].fillna(0).round(2)
    return df_agrupado

# =====================================================================
# CONSOLIDAÇÃO DO BLOCO DE EQUIPAMENTOS
# =====================================================================

def extrair_bloco_equipamentos(caminhos_arquivos):

    print('\n[Módulo ETL Equipamentos] Extraindo e processando tecnologia hospitalar...')
    
    # As funções que puxavam o Total agora recebem os dois caminhos como argumento!
    df_diag_total = processar_equip_diagnostico_imagem(caminhos_arquivos['diag_imagem'], caminhos_arquivos['diag_imagem_sus'])
    df_diag_sus = processar_equip_diagnostico_imagem_sus(caminhos_arquivos['diag_imagem_sus'])
    
    df_totais_total = processar_equip_totais(caminhos_arquivos['totais'], caminhos_arquivos['totais_sus'])
    df_totais_sus = processar_equip_totais_sus(caminhos_arquivos['totais_sus'])
    
    df_vida_total = processar_equip_manutencao_vida(caminhos_arquivos['manut_vida'], caminhos_arquivos['manut_vida_sus'])
    df_vida_sus = processar_equip_manutencao_vida_sus(caminhos_arquivos['manut_vida_sus'])
    
    df_graf_total = processar_equip_metodos_graficos(caminhos_arquivos['met_graficos'], caminhos_arquivos['met_graficos_sus'])
    df_graf_sus = processar_equip_metodos_graficos_sus(caminhos_arquivos['met_graficos_sus'])

    inspecionar_dados(df_graf_sus, "dataset sus")
    inspecionar_dados(df_graf_total, "dataset nao sus e total")

    dfs_equipamentos = [
        df_diag_total, df_diag_sus,
        df_totais_total, df_totais_sus,
        df_vida_total, df_vida_sus,
        df_graf_total, df_graf_sus
    ]

    print('[Módulo ETL Equipamentos] Consolidando Bloco Tecnológico...')
    df_bloco = reduce(
        lambda esquerda, direita: pd.merge(
            esquerda, 
            direita, 
            on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano'], 
            how='outer'
            ), 
        dfs_equipamentos
    ).fillna(0)
    

    return df_bloco

# ISSO AQUI É SO PRA CASO QUERIA SO RODAR O python ETL_EQUIPAMENTOS.PY PRA VER ESSAS TABELAS sem rodar o main.py
if __name__ == "__main__":

    caminhos_equipamentos = {
        'diag_imagem': './datasets/datasus_cnes/equipamentos/diagnostico_imagem_em_uso.csv',
        'totais': './datasets/datasus_cnes/equipamentos/equipamentos_totais_em_uso.csv',
        'manut_vida': './datasets/datasus_cnes/equipamentos/manutencao_vida_em_uso.csv',
        'met_graficos': './datasets/datasus_cnes/equipamentos/metodos_graficos_em_uso.csv',
        
        'diag_imagem_sus': './datasets/datasus_cnes/equipamentos/somente_em_uso_sus/diagnostico_imagem_em_uso_sus.csv',
        'totais_sus': './datasets/datasus_cnes/equipamentos/somente_em_uso_sus/equipamentos_totais_em_uso_sus.csv',
        'manut_vida_sus': './datasets/datasus_cnes/equipamentos/somente_em_uso_sus/manutencao_vida_em_uso_sus.csv',
        'met_graficos_sus': './datasets/datasus_cnes/equipamentos/somente_em_uso_sus/metodos_graficos_em_uso_sus.csv'
    }

    # Chama o módulo para processar os 8 datasets de equipamentos
    df_blocos_equipamentos = extrair_bloco_equipamentos(caminhos_equipamentos)