import pandas as pd

# ===================================
# Funções de remover o rodape e afins
# ===================================


def remove_footer(df):
    coluna_zero = df.iloc[:, 0].astype(str)

    filtro_total = coluna_zero.str.contains("Total", case=False, na=False)
    filtro_fonte = coluna_zero.str.contains("Fonte|Nota", case=False, na=False)
    filtro_df = coluna_zero.str.contains("Distrito Federal", case=False, na=False)

    if filtro_total.any():
        df = df.iloc[: filtro_total.idxmax()]
    elif filtro_fonte.any():
        df = df.iloc[: filtro_fonte.idxmax()]
    elif filtro_df.any():
        indice_final = filtro_df[filtro_df].index[-1]
        df = df.loc[:indice_final]

    df = df.dropna(how="all")
    return df


def split_id_name_unidade_federativa(df, nome_coluna):
    campos = df[nome_coluna].astype(str).str.extract(r"^\s*(\d{2})\s*(.*)")
    df["id_unidade_federativa"] = campos[0]
    df["nome_unidade_federativa"] = campos[1]
    return df


def inspecionar_dados(df, nome_dataset):

    # 1. DESLIGA OS LIMITES DO PANDAS
    pd.set_option("display.max_rows", None)  # Mostra todas as linhas
    pd.set_option("display.max_columns", None)  # Mostra todas as colunas
    pd.set_option("display.width", None)  # Expande a largura do terminal
    pd.set_option(
        "display.max_colwidth", None
    )  # Não corta os textos dentro das células

    print(f"\n{'=' * 80}")
    print(f"📊 INSPECIONANDO: {nome_dataset}")
    print(f"{'=' * 80}")

    print("\n🔹 Tipos de Dados (dtypes):")
    print(df.dtypes)

    print("\n🔹 TABELA COMPLETA:")
    print(df)

    print("\n🔹 Informações da Memória e Nulos (Info):")
    df.info()
    print(f"{'=' * 80}\n")

    # 2. RELIGA OS LIMITES DO PANDAS (Boas práticas de segurança)
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")
    pd.reset_option("display.width")
    pd.reset_option("display.max_colwidth")
