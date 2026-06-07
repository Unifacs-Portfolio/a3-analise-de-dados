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


def ler_datasus_dinamico(caminho):
    with open(caminho, "r", encoding="latin1") as f:
        linhas = f.readlines()

    linha_cabecalho = 0
    # Procura a linha que começa a tabela
    for i, linha in enumerate(linhas):
        # Remove as aspas duplas e espaços para facilitar a busca
        linha_limpa = linha.replace('"', "").strip()
        if linha_limpa.startswith("Unidade da Federa"):
            linha_cabecalho = i
            break
    df = pd.read_csv(
        caminho,
        encoding="latin1",
        sep=";",
        skiprows=linha_cabecalho,
        na_values=["-", " - "],
        on_bad_lines="skip",
    )

    return remove_footer(df)


# =====================================================================
# FUNÇÃO GENÉRICA PARA LER ARQUIVOS DIVIDIDOS POR ANO
# =====================================================================


def processar_arquivos_anuais(dicionario_caminhos, sufixo=""):
    dfs = []
    print(f"\n🔍 Lendo {len(dicionario_caminhos)} arquivos para o grupo '{sufixo}'...")

    for ano, caminho in dicionario_caminhos.items():
        if not os.path.exists(caminho):
            print(f"  ❌ ALERTA: Ficheiro NÃO ENCONTRADO -> {caminho}")
            continue

        df = ler_datasus_dinamico(caminho)
        df = df.drop(columns=["Total"], errors="ignore")
        df = df.rename(columns={df.columns[0]: "unidade_federativa"})
        df = split_id_name_unidade_federativa(df, "unidade_federativa")
        df = df.drop(columns=["unidade_federativa"])
        df["ano"] = str(ano)
        dfs.append(df)

    if not dfs:
        print(
            f"🚨 ERRO: Nenhum arquivo processado para '{sufixo}'. Retornando DataFrame vazio."
        )
        return pd.DataFrame(
            columns=["id_unidade_federativa", "nome_unidade_federativa", "ano"]
        )

    df_final = pd.concat(dfs, ignore_index=True)
    colunas_metricas = df_final.columns.difference(
        ["id_unidade_federativa", "nome_unidade_federativa", "ano"]
    )

    for col in colunas_metricas:
        df_final[col] = df_final[col].fillna(0).astype(int)
        if sufixo:
            df_final = df_final.rename(columns={col: f"{col}_{sufixo}"})

    return df_final


# =====================================================================
# FUNÇÃO PARA OS DATASETS DE MORTES SUS (Anos nas Colunas)
# =====================================================================


def processar_sus_anos_colunas(caminho_arquivo, nome_valor):
    if not os.path.exists(caminho_arquivo):
        print(f"❌ ALERTA: Ficheiro NÃO ENCONTRADO -> {caminho_arquivo}")
        return pd.DataFrame(
            columns=[
                "id_unidade_federativa",
                "nome_unidade_federativa",
                "ano",
                nome_valor,
            ]
        )

    df = ler_datasus_dinamico(caminho_arquivo)
    df = df.rename(columns={df.columns[0]: "unidade_federativa"})

    anos_interesse = ["2018", "2021", "2022", "2023"]
    colunas_presentes = [ano for ano in anos_interesse if ano in df.columns]

    df = split_id_name_unidade_federativa(df, "unidade_federativa")
    df = df[["id_unidade_federativa", "nome_unidade_federativa"] + colunas_presentes]

    for col in colunas_presentes:
        df[col] = df[col].fillna(0).astype(int)

    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        value_vars=colunas_presentes,
        var_name="ano",
        value_name=nome_valor,
    )
    return df


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

    # Criei uma lista de anos para facilitar se você quiser adicionar 2019, 2020 depois.
    anos = ["2018", "2021", "2022", "2023"]

    caminhos_mortes_geral = {
        ano: f"./datasets/mortalidade_geral_5_74/{ano}.csv" for ano in anos
    }
    caminhos_mortes_local = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/local_ocorrencia/{ano}.csv"
        for ano in anos
    }
    caminhos_mortes_cid10 = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/{ano}.csv"
        for ano in anos
    }

    # Subgrupos CID-10
    caminhos_cid10_domicilio = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/domicilio/{ano}.csv"
        for ano in anos
    }
    caminhos_cid10_hospital = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/hospital/{ano}.csv"
        for ano in anos
    }
    caminhos_cid10_ignorado = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/ignorado/{ano}.csv"
        for ano in anos
    }
    caminhos_cid10_outro_estab = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/outro_estabelecimento_saude/{ano}.csv"
        for ano in anos
    }
    caminhos_cid10_outros = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/outros/{ano}.csv"
        for ano in anos
    }
    caminhos_cid10_via_publica = {
        ano: f"./datasets/mortalidade_geral_5_74/grupo_1/cid10/via_publica/{ano}.csv"
        for ano in anos
    }

    # PROCESSANDO TUDO
    df_mortes_geral = processar_arquivos_anuais(caminhos_mortes_geral)

    # Renomeando o agrupamento local de ocorrência
    df_mortes_local = processar_arquivos_anuais(caminhos_mortes_local)
    df_mortes_local = df_mortes_local.rename(
        columns={
            "Hospital": "obitos_hospital",
            "Outro estabelecimento de saúde": "obitos_outro_estab_saude",
            "Domicílio": "obitos_domicilio",
            "Via pública": "obitos_via_publica",
            "Outros": "obitos_outros",
            "Ignorado": "obitos_ignorado",
        }
    )

    df_mortes_cid10 = processar_arquivos_anuais(caminhos_mortes_cid10, sufixo="geral")
    df_cid10_domicilio = processar_arquivos_anuais(
        caminhos_cid10_domicilio, sufixo="domicilio"
    )
    df_cid10_hospital = processar_arquivos_anuais(
        caminhos_cid10_hospital, sufixo="hospital"
    )
    df_cid10_ignorado = processar_arquivos_anuais(
        caminhos_cid10_ignorado, sufixo="ignorado"
    )
    df_cid10_outro_estab = processar_arquivos_anuais(
        caminhos_cid10_outro_estab, sufixo="outro_estab"
    )
    df_cid10_outros = processar_arquivos_anuais(caminhos_cid10_outros, sufixo="outros")
    df_cid10_via_publica = processar_arquivos_anuais(
        caminhos_cid10_via_publica, sufixo="via_publica"
    )

    # PROCESSANDO OS 3 NOVOS DATASETS
    df_dias_permanencia = processar_sus_anos_colunas(
        "./datasets/datasets_juntos/dias_permanencia_sus.csv",
        "dias_permanencia_sus_total",
    )
    df_internacoes_sus = processar_sus_anos_colunas(
        "./datasets/datasets_juntos/internacoes_sus.csv", "internacoes_sus_total"
    )
    df_obitos_sus = processar_sus_anos_colunas(
        "./datasets/datasets_juntos/obitos_sus.csv", "obitos_sus_total"
    )

    df_idhml = obter_idhm_longevidade("./datasets/datasets_juntos/base_de_dados.xlsx")

    # LISTA FINAL COM TODAS AS NOVAS VARIÁVEIS
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
        df_dias_permanencia,
        df_internacoes_sus,
        df_obitos_sus,
        df_idhml,
    ]

    inspecionar_dados(df_mortes_geral, "dataset mortes")
    inspecionar_dados(df_mortes_local, "dataset mortes local")
    inspecionar_dados(df_mortes_cid10, "dataset mortes cid10")
    inspecionar_dados(df_cid10_domicilio, "dataset cid10 domicilio")
    inspecionar_dados(df_cid10_hospital, "dataset cid10 hospital")
    inspecionar_dados(df_cid10_ignorado, "dataset cid10 ignorado")
    inspecionar_dados(df_cid10_outro_estab, "dataset cid10 outro estabelecimento")
    inspecionar_dados(df_cid10_outros, "dataset cid10 outros")
    inspecionar_dados(df_cid10_via_publica, "dataset cid10 via publica")
    inspecionar_dados(df_dias_permanencia, "dataset dias permanencia")
    inspecionar_dados(df_internacoes_sus, "dataset internações sus")
    inspecionar_dados(df_obitos_sus, "dataset obitos sus")
    inspecionar_dados(df_idhml, "dataset idhml")

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

    dfs_para_mesclar = [df_consolidado_v1] + dfs_v2_final

    print(
        "[ETL V2] Enriquecendo a base com dados Detalhados de Mortalidade (CID-10) e SUS..."
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
    print(
        f"\n✅ SUCESSO! O seu Mega Dataset foi atualizado sem duplicar nomes de colunas e salvo em: {caminho_saida}"
    )
