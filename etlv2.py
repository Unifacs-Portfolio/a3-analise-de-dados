import sys
import os
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from functools import reduce
from utils.utils import (
    remove_footer,
    split_id_name_unidade_federativa,
    inspecionar_dados,
)


def extrair_dados_causa_geral(diretorio):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=3, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]

        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    return pd.concat(dfs, ignore_index=True)


def extrair_dados_grupo1_local(diretorio):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=4, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]

        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

    if not dfs:
        return pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    return pd.concat(dfs, ignore_index=True)


# ==============================================================
# SUBGRUPOS CID10
# ==============================================================


def extrair_dados_grupo1_cid10_total(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=4, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        # Conversão numérica segura
        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeia as colunas com o sufixo, mantendo as metadados intactas
    colunas_para_renomear = {
        col: f"{col}_{sufixo}"
        for col in df_final.columns
        if col not in colunas_metadata
    }
    df_final = df_final.rename(columns=colunas_para_renomear)

    return df_final


def extrair_dados_grupo1_cid10_domicilio(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=5, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeia as colunas com o sufixo, mantendo as metadados intactas
    colunas_para_renomear = {
        col: f"{col}_{sufixo}"
        for col in df_final.columns
        if col not in colunas_metadata
    }
    df_final = df_final.rename(columns=colunas_para_renomear)

    return df_final


def extrair_dados_grupo1_cid10_hospital(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=5, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeia as colunas com o sufixo, mantendo as metadados intactas
    colunas_para_renomear = {
        col: f"{col}_{sufixo}"
        for col in df_final.columns
        if col not in colunas_metadata
    }
    df_final = df_final.rename(columns=colunas_para_renomear)

    return df_final


def extrair_dados_grupo1_cid10_ignorado(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    # Lista mestra de todas as 27 UFs do Brasil
    lista_ufs = [
        ("11", "Rondônia"),
        ("12", "Acre"),
        ("13", "Amazonas"),
        ("14", "Roraima"),
        ("15", "Pará"),
        ("16", "Amapá"),
        ("17", "Tocantins"),
        ("21", "Maranhão"),
        ("22", "Piauí"),
        ("23", "Ceará"),
        ("24", "Rio Grande do Norte"),
        ("25", "Paraíba"),
        ("26", "Pernambuco"),
        ("27", "Alagoas"),
        ("28", "Sergipe"),
        ("29", "Bahia"),
        ("31", "Minas Gerais"),
        ("32", "Espírito Santo"),
        ("33", "Rio de Janeiro"),
        ("35", "São Paulo"),
        ("41", "Paraná"),
        ("42", "Santa Catarina"),
        ("43", "Rio Grande do Sul"),
        ("50", "Mato Grosso do Sul"),
        ("51", "Mato Grosso"),
        ("52", "Goiás"),
        ("53", "Distrito Federal"),
    ]
    df_modelo = pd.DataFrame(
        lista_ufs, columns=["id_unidade_federativa", "nome_unidade_federativa"]
    )

    colunas_finais = [
        "Cap I",
        "Cap II",
        "Cap IV",
        "Cap V",
        "Cap VI",
        "Cap IX",
        "Cap X",
        "Cap XI",
        "Cap XII",
        "Cap XIV",
        "Cap XV",
        "Cap XX",
    ]

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=5, na_values=["-", " - "]
            )
        )

        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "coluna_tmp"})
        df = split_id_name_unidade_federativa(df, "coluna_tmp")
        df = df.drop(columns=["coluna_tmp"])
        df["ano"] = str(ano)

        df = pd.merge(
            df_modelo,
            df,
            on=["id_unidade_federativa", "nome_unidade_federativa"],
            how="left",
        )
        df["ano"] = str(ano)

        df = df.reindex(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
            + colunas_finais,
            fill_value=0,
        )

        # Conversão numérica segura
        for col in colunas_finais:
            df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeação com sufixo
    colunas_para_renomear = {col: f"{col}_{sufixo}" for col in colunas_finais}
    return df_final.rename(columns=colunas_para_renomear)


def extrair_dados_grupo1_cid10_outro_estabelecimento(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=5, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeia as colunas com o sufixo, mantendo as metadados intactas
    colunas_para_renomear = {
        col: f"{col}_{sufixo}"
        for col in df_final.columns
        if col not in colunas_metadata
    }
    df_final = df_final.rename(columns=colunas_para_renomear)

    return df_final


def extrair_dados_grupo1_cid10_outros(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=5, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeia as colunas com o sufixo, mantendo as metadados intactas
    colunas_para_renomear = {
        col: f"{col}_{sufixo}"
        for col in df_final.columns
        if col not in colunas_metadata
    }
    df_final = df_final.rename(columns=colunas_para_renomear)

    return df_final


def extrair_dados_grupo1_cid10_via_publica(diretorio, sufixo):
    anos_permitidos = ["2018", "2021", "2022", "2023"]
    arquivos = glob.glob(os.path.join(diretorio, "*.csv"))
    dfs = []

    for caminho in arquivos:
        ano = os.path.basename(caminho).replace(".csv", "")
        if ano not in anos_permitidos:
            continue

        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", skiprows=5, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)

        colunas_metadata = ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        for col in df.columns:
            if col not in colunas_metadata:
                df[col] = df[col].fillna(0).astype(int)

        dfs.append(df)

        pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)

    # Renomeia as colunas com o sufixo, mantendo as metadados intactas
    colunas_para_renomear = {
        col: f"{col}_{sufixo}"
        for col in df_final.columns
        if col not in colunas_metadata
    }
    df_final = df_final.rename(columns=colunas_para_renomear)

    return df_final


# =====================================================================
# FUNÇÕES EXPLÍCITAS
# =====================================================================


def processar_mortes_causa_geral(diretorio):
    return extrair_dados_causa_geral(diretorio)


def processar_mortes_local_ocorrencia(diretorio):
    df = extrair_dados_grupo1_local(diretorio)
    df = df.rename(
        columns={
            "Hospital": "obitos_hospital",
            "Outro estabelecimento de saúde": "obitos_outro_estab_saude",
            "Domicílio": "obitos_domicilio",
            "Via pública": "obitos_via_publica",
            "Outros": "obitos_outros",
            "Ignorado": "obitos_ignorado",
        }
    )
    return df


def processar_mortes_cid10_geral(diretorio):
    return extrair_dados_grupo1_cid10_total(diretorio, sufixo="geral")


def processar_mortes_cid10_domicilio(diretorio):
    return extrair_dados_grupo1_cid10_domicilio(diretorio, sufixo="domicilio")


def processar_mortes_cid10_hospital(diretorio):
    return extrair_dados_grupo1_cid10_hospital(diretorio, sufixo="hospital")


def processar_mortes_cid10_ignorado(diretorio):
    return extrair_dados_grupo1_cid10_ignorado(diretorio, sufixo="ignorado")


def processar_mortes_cid10_outro_estab(diretorio):
    return extrair_dados_grupo1_cid10_outro_estabelecimento(
        diretorio, sufixo="outro_estab"
    )


def processar_mortes_cid10_outros(diretorio):
    return extrair_dados_grupo1_cid10_outros(diretorio, sufixo="outros")


def processar_mortes_cid10_via_publica(diretorio):
    return extrair_dados_grupo1_cid10_via_publica(diretorio, sufixo="via_publica")


# =====================================================================
# EXTRAÇÃO DO IDHM-LONGEVIDADE
# =====================================================================


def obter_idhm_longevidade(caminho_arquivo):
    print("\n[ETL V2] Convertendo Excel para CSV para garantir a pureza dos Dtypes...")
    df_excel = pd.read_excel(
        caminho_arquivo, engine="openpyxl", sheet_name="Base de Dados"
    )
    caminho_csv = caminho_arquivo.replace(".xlsx", "_convertido.csv")
    df_excel.to_csv(caminho_csv, index=False, encoding="utf-8")

    df = pd.read_csv(caminho_csv, encoding="utf-8")

    if "AGREGACAO" in df.columns:
        df = df[df["AGREGACAO"] == "UF"]

    df = df[["CODIGO", "NOME", "ANO", "IDHM_L"]]
    df = df.rename(
        columns={
            "CODIGO": "id_unidade_federativa",
            "NOME": "nome_unidade_federativa",
            "ANO": "ano",
            "IDHM_L": "idhm_l",
        }
    )
    df["id_unidade_federativa"] = df["id_unidade_federativa"].astype(int).astype(str)
    df["ano"] = df["ano"].astype(int).astype(str)
    df = df[df["ano"].isin(["2018", "2021"])]

    df = df.pivot_table(
        index=["id_unidade_federativa", "nome_unidade_federativa"],
        columns="ano",
        values="idhm_l",
        aggfunc="first",
    ).reset_index()

    df.columns.name = None
    df["2022"] = df["2021"]
    df["2023"] = df["2021"]

    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        value_vars=["2018", "2021", "2022", "2023"],
        var_name="ano",
        value_name="idhm_l",
    )
    return df


# ===========================
# ORQUESTRAÇÃO DOS ARQUIVOS
# ===========================

if __name__ == "__main__":
    print("🚀 Carregando dados para a segunda fase de ETL!")

    # Processamento explícito por blocos
    df_mortes_geral = processar_mortes_causa_geral("./datasets/mortalidade_geral_5_74/")
    df_mortes_local = processar_mortes_local_ocorrencia(
        "./datasets/mortalidade_geral_5_74/grupo_1/local_ocorrencia/"
    )

    # Processamento dos subgrupos CID-10
    df_mortes_cid10 = processar_mortes_cid10_geral(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/"
    )
    df_cid10_domicilio = processar_mortes_cid10_domicilio(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/domicilio/"
    )
    df_cid10_hospital = processar_mortes_cid10_hospital(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/hospital/"
    )
    df_cid10_ignorado = processar_mortes_cid10_ignorado(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/ignorado/"
    )
    df_cid10_outro_estab = processar_mortes_cid10_outro_estab(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/outro_estabelecimento_saude/"
    )
    df_cid10_outros = processar_mortes_cid10_outros(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/outros/"
    )
    df_cid10_via_publica = processar_mortes_cid10_via_publica(
        "./datasets/mortalidade_geral_5_74/grupo_1/cid10/via_publica/"
    )

    df_idhml = obter_idhm_longevidade("./datasets/datasets_juntos/base_de_dados.xlsx")

    # LISTA FINAL
    dfs_v2_final = [
        df_mortes_geral,
        df_mortes_local,
        df_mortes_cid10,
        df_cid10_domicilio,
        df_cid10_hospital,
        df_cid10_ignorado,
        df_cid10_outro_estab,
        df_cid10_outros,
        df_cid10_via_publica,
        df_idhml,
    ]

    # =======================
    # JUNTANDO COM O PRIMEIRO DATASET COMPLETO
    # =======================

    print("\n[ETL V2] Lendo o Dataset completo...")
    df_consolidado_v1 = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

    # Padronização de tipos de chaves para o merge
    df_consolidado_v1["id_unidade_federativa"] = df_consolidado_v1[
        "id_unidade_federativa"
    ].astype(str)
    df_consolidado_v1["ano"] = df_consolidado_v1["ano"].astype(str)

    # 1. Descobrimos o nome de todas as colunas que o ETL V2 gera (ignorando as chaves)
    colunas_novas_v2 = set()
    for df_novo in dfs_v2_final:
        for col in df_novo.columns:
            if col not in ["id_unidade_federativa", "nome_unidade_federativa", "ano"]:
                colunas_novas_v2.add(col)

    # 2. Apagamos essas colunas do arquivo antigo (se elas já existirem de uma rodada anterior)
    df_consolidado_v1 = df_consolidado_v1.drop(
        columns=list(colunas_novas_v2), errors="ignore"
    )
    # -------------------------------------------------------------------------

    dfs_para_mesclar = [df_consolidado_v1] + dfs_v2_final

    print(
        "[ETL V2] Enriquecendo a base com dados Detalhados de Mortalidade (CID-10)..."
    )
    df_consolidado_final = reduce(
        lambda esquerda, direita: pd.merge(
            esquerda,
            direita,
            on=["id_unidade_federativa", "nome_unidade_federativa", "ano"],
            how="left",
        ),
        dfs_para_mesclar,
    )

    caminho_saida = "./datasets/dataset_completo_consolidado.csv"
    df_consolidado_final.to_csv(caminho_saida, index=False, encoding="utf-8")
    print(f"\nDataset complementado gerado com sucesso!: {caminho_saida}")
