import pandas as pd
from functools import reduce
from utils.utils import remove_footer, split_id_name_unidade_federativa, inspecionar_dados

# =====================================================================
# FUNÇÕES DIAGNÓSTICO POR IMAGEM
# =====================================================================

def processar_equip_diagnostico_imagem(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_diag_imagem_total')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_diag_imagem_total'] = df['equip_diag_imagem_total'].astype(int)
    return df

def processar_equip_diagnostico_imagem_sus(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_diag_imagem_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_diag_imagem_sus'] = df['equip_diag_imagem_sus'].astype(int)
    return df


# =====================================================================
# FUNÇÕES EQUIPAMENTOS TOTAIS
# =====================================================================

def processar_equip_totais(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_totais_total')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_totais_total'] = df['equip_totais_total'].astype(int)
    return df

def processar_equip_totais_sus(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=3, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_totais_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_totais_sus'] = df['equip_totais_sus'].astype(int)
    return df

# =====================================================================
# FUNÇÕES MANUTENÇÃO DA VIDA
# =====================================================================

def processar_equip_manutencao_vida(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_manut_vida_total')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_manut_vida_total'] = df['equip_manut_vida_total'].astype(int)
    return df

def processar_equip_manutencao_vida_sus(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_manut_vida_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_manut_vida_sus'] = df['equip_manut_vida_sus'].astype(int)
    return df


# =====================================================================
# FUNÇÕES MÉTODOS GRÁFICOS
# =====================================================================

def processar_equip_metodos_graficos(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_met_graficos_total')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_met_graficos_total'] = df['equip_met_graficos_total'].astype(int)
    return df

def processar_equip_metodos_graficos_sus(caminho):
    df = remove_footer(pd.read_csv(caminho, encoding='latin1', sep=';', header=4, na_values=['-', ' - ']))
    df = df.drop(columns=['Total'], errors='ignore')
    df = df.rename(columns={df.columns[0]: 'unidade_federativa'})
    df = split_id_name_unidade_federativa(df, 'unidade_federativa')
    df = df.drop(columns=['unidade_federativa'])
    df = df.melt(id_vars=['id_unidade_federativa', 'nome_unidade_federativa'], var_name='ano_mes', value_name='equip_met_graficos_sus')
    df['ano'] = df['ano_mes'].str.split('/').str[0]
    df['equip_met_graficos_sus'] = df['equip_met_graficos_sus'].astype(int)
    return df

# =====================================================================
# TRANSFORMAÇÃO ESTATÍSTICA
# =====================================================================

def aplicar_logica_estatistica(df, coluna_alvo):
    df_agg = df.groupby(['id_unidade_federativa', 'nome_unidade_federativa', 'ano'])[coluna_alvo].agg(['mean', 'median', 'std']).reset_index()
    
    # Renomeia dinamicamente de acordo com a coluna que entrou
    df_agg = df_agg.rename(columns={
        'mean': f'media_{coluna_alvo}',
        'median': f'mediana_{coluna_alvo}',
        'std': f'desvio_padrao_{coluna_alvo}'
    })

    # Tipagem e Arredondamento
    df_agg[f'media_{coluna_alvo}'] = df_agg[f'media_{coluna_alvo}'].round().astype(int)
    df_agg[f'mediana_{coluna_alvo}'] = df_agg[f'mediana_{coluna_alvo}'].round().astype(int)
    df_agg[f'desvio_padrao_{coluna_alvo}'] = df_agg[f'desvio_padrao_{coluna_alvo}'].round(2)

    return df_agg

# =====================================================================
#  MÓDULOS DE DOMÍNIO (Retornando as Variáveis Isoladas)
# =====================================================================

def obter_estatisticas_diagnostico_imagem(caminho_total, caminho_sus):
    df_tot = processar_equip_diagnostico_imagem(caminho_total)
    df_sus = processar_equip_diagnostico_imagem_sus(caminho_sus)
    
    # Merge para achar a diferença mês a mês
    df_par = pd.merge(df_tot, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    df_par['equip_diag_imagem_nao_sus'] = df_par['equip_diag_imagem_total'] - df_par['equip_diag_imagem_sus']

    # TABELAS TOTALMENTE INDEPENDENTES E LIMPAS
    df_est_total = aplicar_logica_estatistica(df_par, 'equip_diag_imagem_total')
    df_est_sus = aplicar_logica_estatistica(df_par, 'equip_diag_imagem_sus')
    df_est_nao_sus = aplicar_logica_estatistica(df_par, 'equip_diag_imagem_nao_sus')

    return df_est_total, df_est_sus, df_est_nao_sus

def obter_estatisticas_totais(caminho_total, caminho_sus):
    df_tot = processar_equip_totais(caminho_total)
    df_sus = processar_equip_totais_sus(caminho_sus)
    
    df_par = pd.merge(df_tot, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    df_par['equip_totais_nao_sus'] = df_par['equip_totais_total'] - df_par['equip_totais_sus']

    df_est_total = aplicar_logica_estatistica(df_par, 'equip_totais_total')
    df_est_sus = aplicar_logica_estatistica(df_par, 'equip_totais_sus')
    df_est_nao_sus = aplicar_logica_estatistica(df_par, 'equip_totais_nao_sus')

    return df_est_total, df_est_sus, df_est_nao_sus

def obter_estatisticas_manutencao_vida(caminho_total, caminho_sus):
    df_tot = processar_equip_manutencao_vida(caminho_total)
    df_sus = processar_equip_manutencao_vida_sus(caminho_sus)
    
    df_par = pd.merge(df_tot, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    df_par['equip_manut_vida_nao_sus'] = df_par['equip_manut_vida_total'] - df_par['equip_manut_vida_sus']

    df_est_total = aplicar_logica_estatistica(df_par, 'equip_manut_vida_total')
    df_est_sus = aplicar_logica_estatistica(df_par, 'equip_manut_vida_sus')
    df_est_nao_sus = aplicar_logica_estatistica(df_par, 'equip_manut_vida_nao_sus')

    return df_est_total, df_est_sus, df_est_nao_sus

def obter_estatisticas_metodos_graficos(caminho_total, caminho_sus):
    df_tot = processar_equip_metodos_graficos(caminho_total)
    df_sus = processar_equip_metodos_graficos_sus(caminho_sus)
    
    df_par = pd.merge(df_tot, df_sus, on=['id_unidade_federativa', 'nome_unidade_federativa', 'ano_mes', 'ano'], how='inner')
    df_par['equip_met_graficos_nao_sus'] = df_par['equip_met_graficos_total'] - df_par['equip_met_graficos_sus']

    df_est_total = aplicar_logica_estatistica(df_par, 'equip_met_graficos_total')
    df_est_sus = aplicar_logica_estatistica(df_par, 'equip_met_graficos_sus')
    df_est_nao_sus = aplicar_logica_estatistica(df_par, 'equip_met_graficos_nao_sus')

    return df_est_total, df_est_sus, df_est_nao_sus


# =====================================================================
# CONSOLIDAÇÃO DO BLOCO DE EQUIPAMENTOS
# =====================================================================

def extrair_bloco_equipamentos(caminhos_arquivos):

    print('\n[Módulo ETL Equipamentos] Extraindo e processando tecnologia hospitalar...')
    
    # As funções mandam os dados pro obter_estatisticas e la na função de obter_estatistica ele limpa e aplica o calculo
    df_diag_total, df_diag_sus, df_diag_nao_sus = obter_estatisticas_diagnostico_imagem(caminhos_arquivos['diag_imagem'], caminhos_arquivos['diag_imagem_sus'])
    df_totais_total, df_totais_sus, df_totais_nao_sus = obter_estatisticas_totais(caminhos_arquivos['totais'], caminhos_arquivos['totais_sus'])
    df_vida_total, df_vida_sus, df_vida_nao_sus = obter_estatisticas_manutencao_vida(caminhos_arquivos['manut_vida'], caminhos_arquivos['manut_vida_sus'])
    df_graf_total, df_graf_sus, df_graf_nao_sus = obter_estatisticas_metodos_graficos(caminhos_arquivos['met_graficos'], caminhos_arquivos['met_graficos_sus'])

    inspecionar_dados(df_totais_sus, "dataset sus")
    inspecionar_dados(df_totais_total, "dataset total")
    inspecionar_dados(df_totais_nao_sus, "dataset nao sus")

    dfs_equipamentos = [
        df_diag_total, df_diag_sus, df_diag_nao_sus,
        df_totais_total, df_totais_sus, df_totais_nao_sus,
        df_vida_total, df_vida_sus, df_vida_nao_sus,
        df_graf_total, df_graf_sus, df_graf_nao_sus
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
    )
    

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