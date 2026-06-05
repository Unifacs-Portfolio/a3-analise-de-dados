import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from functools import reduce
from utils.utils import (
    remove_footer,
    split_id_name_unidade_federativa,
    inspecionar_dados,
)


# =====================================================================
# FUNÇÃO GENÉRICA PARA LER ARQUIVOS DIVIDIDOS POR ANO
# =====================================================================


def processar_arquivos_anuais(dicionario_caminhos):
    dfs = []
    for ano, caminho in dicionario_caminhos.items():
        df = remove_footer(
            pd.read_csv(
                caminho, encoding="latin1", sep=";", header=3, na_values=["-", " - "]
            )
        )
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)
        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)

    colunas_metricas = df_final.columns.difference(
        ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
    )

    for col in colunas_metricas:
        df_final[col] = df_final[col].fillna(0).astype(int)

    return df_final


# ====================
# MÓDULOS DE DOMÍNIO
# ====================


def obter_mortes_por_causa(dicionario_caminhos):
    return processar_arquivos_anuais(dicionario_caminhos)


def obter_mortes_por_cid10(dicionario_caminhos):
    return processar_arquivos_anuais(dicionario_caminhos)


def obter_mortes_por_local(dicionario_caminhos):
    df = processar_arquivos_anuais(dicionario_caminhos)
    # Renomeando para facilitar no EDA
    df = df.rename(
        columns={
            "Hospital": "obitos_hospital",
            "Outro estabelecimento de saúde": "obitos_outro_estab_saude",
            "Domicílio": "obitos_domicilio",
            "Via pública": "obitos_via_publica",
        }
    )
    return df


# =====================================================================
# EXTRAÇÃO DO IDHM-LONGEVIDADE
# =====================================================================


def obter_idhm_longevidade(caminho_arquivo):
    print(
        "\n[ETL Mortalidade] Convertendo Excel para CSV para garantir a pureza dos Dtypes..."
    )

    df_excel = pd.read_excel(
        caminho_arquivo, engine="openpyxl", sheet_name="Base de Dados"
    )
    caminho_csv = caminho_arquivo.replace(".xlsx", "_convertido.csv")
    df_excel.to_csv(caminho_csv, index=False, encoding="utf-8")

    print(f"[ETL Mortalidade] CSV gerado com sucesso em: {caminho_csv}")
    print("[ETL Mortalidade] Lendo o novo CSV e processando...")
    df = pd.read_csv(caminho_csv, encoding="utf-8")

    # Filtra apenas os Estados (UF)
    if "AGREGACAO" in df.columns:
        df = df[df["AGREGACAO"] == "UF"]

    # Fica apenas com as colunas que importam
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
    df["ano"] = df["ano"].astype(str)

    # Filtra apenas os anos que temos base
    df = df[df["ano"].isin(["2018", "2021"])]

    # Pivota os dados
    df = df.pivot_table(
        index=["id_unidade_federativa", "nome_unidade_federativa"],
        columns="ano",
        values="idhm_l",
        aggfunc="first",
    ).reset_index()

    # Limpando o nome da coluna de índice
    df.columns.name = None

    # Foward Fill
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
# Caminhos para os arquivos
# ===========================

if __name__ == "__main__":
    print("Carregando dados para a segunda fase de etl!")

    caminhos_mortes_local = {
        "2018": "./datasets_v2/mortes_evitaveis_local_ocorrencia/mortes_evitaveis_5_74_local_ocorrencia_2018.csv",
        "2021": "./datasets_v2/mortes_evitaveis_local_ocorrencia/mortes_evitaveis_5_74_local_ocorrencia_2021.csv",
        "2022": "./datasets_v2/mortes_evitaveis_local_ocorrencia/mortes_evitaveis_5_74_local_ocorrencia_2022.csv",
        "2023": "./datasets_v2/mortes_evitaveis_local_ocorrencia/mortes_evitaveis_5_74_local_ocorrencia_2023.csv",
    }
    df_mortes_local = obter_mortes_por_local(caminhos_mortes_local)

    caminhos_mortes_cid10 = {
        "2018": "./datasets_v2/mortes_evitaveis_cid10/mortes_evitaveis_5_74_cid10_2018.csv",
        "2021": "./datasets_v2/mortes_evitaveis_cid10/mortes_evitaveis_5_74_cid10_2021.csv",
        "2022": "./datasets_v2/mortes_evitaveis_cid10/mortes_evitaveis_5_74_cid10_2022.csv",
        "2023": "./datasets_v2/mortes_evitaveis_cid10/mortes_evitaveis_5_74_cid10_2023.csv",
    }
    df_mortes_cid10 = obter_mortes_por_cid10(caminhos_mortes_cid10)

    caminhos_mortes_causas = {
        "2018": "./datasets_v2/mortes_evitaveis_causa/mortes_evitaveis_5_74_causa_2018.csv",
        "2021": "./datasets_v2/mortes_evitaveis_causa/mortes_evitaveis_5_74_causa_2021.csv",
        "2022": "./datasets_v2/mortes_evitaveis_causa/mortes_evitaveis_5_74_causa_2022.csv",
        "2023": "./datasets_v2/mortes_evitaveis_causa/mortes_evitaveis_5_74_causa_2023.csv",
    }
    df_mortes_causas = obter_mortes_por_causa(caminhos_mortes_causas)

    df_idhml = obter_idhm_longevidade("./datasets_v2/outros/base_de_dados.xlsx")

    dfs_v2_final = [df_mortes_causas, df_mortes_cid10, df_idhml, df_mortes_local]

    inspecionar_dados(df_mortes_causas, "dados mortes causas")
    inspecionar_dados(df_mortes_cid10, "dados mortes cid10")
    inspecionar_dados(df_mortes_local, "dados mortes local")
    inspecionar_dados(df_idhml, "dados idhm-L")

    # =======================
    # Juntando os dados novos
    # =======================

    print("\n[ETL V2] Lendo o Golden Record V1...")
    df_consolidado_v1 = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

    df_consolidado_v1["id_unidade_federativa"] = df_consolidado_v1[
        "id_unidade_federativa"
    ].astype(str)
    df_consolidado_v1["ano"] = df_consolidado_v1["ano"].astype(str)

    dfs_para_mesclar = [df_consolidado_v1] + dfs_v2_final

    print("[ETL V2] Enriquecendo a base com dados de Mortalidade e Longevidade...")
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
