import pandas as pd

# ===================================
# Funções de remover o rodape e afins
# ===================================

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