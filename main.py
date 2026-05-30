import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from functools import reduce
from etls.etl_equipamentos import (
    extrair_bloco_equipamentos,
    obter_estatisticas_diagnostico_imagem,
    obter_estatisticas_manutencao_vida,
    obter_estatisticas_metodos_graficos,
    obter_estatisticas_totais,
)
from etls.etl_leitos import (
    extrair_bloco_infraestrutura,
    obter_estatisticas_repouso,
    obter_estatisticas_enfermaria,
    obter_estatisticas_uti,
)
from utils.utils import (
    remove_footer,
    split_id_name_unidade_federativa,
    inspecionar_dados,
)

# =============================================
# Função para processar os dados de internações
# ==============================================


def processar_datasus_internacoes(caminho_arquivo):
    df = remove_footer(
        pd.read_csv(caminho_arquivo, encoding="latin1", sep=";", header=3)
    )
    df = df.drop(columns=["Total", "2017", "2019", "2020", "2024", "2025", "2026"])
    df = df.rename(
        columns={
            df.columns[0]: "unidade_federativa",
        }
    )
    colunas_alvo = df.columns[1:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = split_id_name_unidade_federativa(df, "unidade_federativa")
    df = df.drop(columns=["unidade_federativa"])
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="internacoes",
    )
    return df


# =============================================
# Função para processar os dados de permanência
# ==============================================


def processar_datasus_dias_permanencia(caminho_arquivo):
    df = remove_footer(
        pd.read_csv(
            caminho_arquivo,
            encoding="latin1",
            header=3,
            sep=";",
            usecols=["Unidade da Federação", "2018", "2021", "2022", "2023"],
        )
    )
    df = df.rename(
        columns={
            df.columns[0]: "unidade_federativa",
        }
    )
    colunas_alvo = df.columns[1:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = split_id_name_unidade_federativa(df, "unidade_federativa")
    df = df.drop(columns=["unidade_federativa"])
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="dias_internacao",
    )
    return df


# =============================================
# Função para processar os dados de Gini
# ==============================================


def processar_dataset_gini(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, sep=";", header=3, decimal=","))
    df = df.rename(
        columns={
            df.columns[0]: "id_unidade_federativa",
            df.columns[1]: "nome_unidade_federativa",
        }
    )
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="indice_gini",
    )
    return df


# =============================================
# Função para processar os dados de renda per capita
# ==============================================


def processar_dataset_renda_capita(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, header=3, sep=";"))
    df = df.rename(
        columns={
            df.columns[0]: "id_unidade_federativa",
            df.columns[1]: "nome_unidade_federativa",
        }
    )
    colunas_alvo = df.columns[2:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="renda_per_capita",
    )
    return df


# =============================================
# Função para processar os dados do PIB
# ==============================================


def processar_dataset_pib(caminho_arquivo):
    df = remove_footer(pd.read_csv(caminho_arquivo, header=3, sep=";", decimal=","))
    df = df.rename(
        columns={
            df.columns[0]: "id_unidade_federativa",
            df.columns[1]: "nome_unidade_federativa",
        }
    )
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="pib_milhares",
    )
    return df


# =============================================
# Função para processar os dados de Obitos
# ==============================================


def processar_datasus_obitos(caminho_arquivo):
    df = remove_footer(
        pd.read_csv(
            caminho_arquivo,
            encoding="latin1",
            header=3,
            sep=";",
            usecols=["Unidade da Federação", "2018", "2021", "2022", "2023"],
        )
    )
    df = df.rename(
        columns={
            df.columns[0]: "unidade_federativa",
        }
    )
    colunas_alvo = df.columns[1:]
    df[colunas_alvo] = df[colunas_alvo].astype(int)
    df = split_id_name_unidade_federativa(df, "unidade_federativa")
    df = df.drop(columns=["unidade_federativa"])
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="obitos_hospitalares",
    )
    return df


# =============================================
# Função para processar os dados de População
# ==============================================


def processar_dataset_populacao(caminho_arquivo):
    df = remove_footer(
        pd.read_csv(
            caminho_arquivo,
            encoding="latin1",
            sep=";",
            header=3,
            usecols=["Unidade da Federação", "2018", "2021", "2022", "2023"],
            thousands=".",
            decimal=",",
        )
    )
    df = df.rename(columns={df.columns[0]: "unidade_federativa"})
    colunas_alvo = df.columns[1:]

    for col in colunas_alvo:
        df[col] = df[col].astype(int)

    df = split_id_name_unidade_federativa(df, "unidade_federativa")
    df = df.drop(columns=["unidade_federativa"])
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="populacao",
    )
    return df


# =============================================
# Função para processar os dados de Obitos_Evitaveis
# ==============================================


def processar_datasus_obitos_evitaveis(caminho_arquivo):
    df = remove_footer(
        pd.read_csv(
            caminho_arquivo,
            encoding="latin1",
            sep=";",
            header=3,
            usecols=["Unidade da Federação", "2018", "2021", "2022", "2023"],
            thousands=".",
            decimal=",",
            na_values=["-", " - "],
        )
    )
    df = df.rename(columns={df.columns[0]: "unidade_federativa"})
    colunas_alvo = df.columns[1:]

    for col in colunas_alvo:
        df[col] = df[col].astype(int)

    df = split_id_name_unidade_federativa(df, "unidade_federativa")
    df = df.drop(columns=["unidade_federativa"])
    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        var_name="ano",
        value_name="obitos_evitaveis",
    )
    return df


# =============================================
# Função para processar os dados de IDHM
# ==============================================


def processar_dataset_idhm(caminho_arquivo):
    df = pd.read_csv(
        caminho_arquivo,
        encoding="utf-8",
        sep=",",
        header=1,
        usecols=["Código", "Estado", "2018", "2021"],
    )
    df = df.rename(
        columns={"Código": "id_unidade_federativa", "Estado": "nome_unidade_federativa"}
    )

    df["id_unidade_federativa"] = df["id_unidade_federativa"].astype(str)

    # Foward Fill
    df["2022"] = df["2021"]
    df["2023"] = df["2021"]

    df = df.melt(
        id_vars=["id_unidade_federativa", "nome_unidade_federativa"],
        value_vars=["2018", "2021", "2022", "2023"],
        var_name="ano",
        value_name="idhm",
    )
    return df


# =============================================
# Parte Principal do código
# ==============================================

if __name__ == "__main__":
    print("Iniciando processamento das matrizes históricas (Raiz)...")

    # Bases de dados
    df_internacoes = processar_datasus_internacoes(
        "./datasets/morbidade_hospitalar_sus/internacoes.csv"
    )
    df_permanencia = processar_datasus_dias_permanencia(
        "./datasets/morbidade_hospitalar_sus/dias_permanencia.csv"
    )
    df_gini = processar_dataset_gini("./datasets/datasets_juntos/indice_gini.csv")
    df_renda = processar_dataset_renda_capita(
        "./datasets/datasets_juntos/renda_per_capita.csv"
    )
    df_pib = processar_dataset_pib("./datasets/datasets_juntos/pib_corrente.csv")
    df_obitos_hospitalares = processar_datasus_obitos(
        "./datasets/morbidade_hospitalar_sus/obitos_hospitalares.csv"
    )
    df_populacao = processar_dataset_populacao(
        "./datasets/datasets_juntos/populacao_ibge.csv"
    )
    df_obitos_evitaveis = processar_datasus_obitos_evitaveis(
        "./datasets/datasets_juntos/obitos_evitaveis_5_74.csv"
    )
    df_idhm = processar_dataset_idhm(
        "./datasets/datasets_juntos/indice_desenvolvimento_humano.csv"
    )

    # Bases dos leitos para usar unitariamente
    df_rep_fem, df_rep_masc, df_rep_ind, df_rep_ped, df_rep_tot = (
        obter_estatisticas_repouso(
            "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_feminino.csv",
            "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_masculino.csv",
            "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_indiferente.csv",
            "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_pediatria.csv",
        )
    )

    df_uti_total, df_uti_sus, df_uti_nao_sus = obter_estatisticas_uti(
        "./datasets/datasus_cnes/leitos_complementares_nao_sus.csv",
        "./datasets/datasus_cnes/leitos_complementares_sus.csv",
    )

    df_enf_total, df_enf_sus, df_enf_nao_sus = obter_estatisticas_enfermaria(
        "./datasets/datasus_cnes/leitos_enfermaria_nao_sus.csv",
        "./datasets/datasus_cnes/leitos_enfermaria_sus.csv",
    )

    # Bases dos equipamentos para usar unitariamente
    # DIAGNÓSTICO POR IMAGEM
    df_diag_total, df_diag_sus, df_diag_nao_sus = obter_estatisticas_diagnostico_imagem(
        "./datasets/datasus_cnes/equipamentos/diagnostico_imagem_em_uso.csv",
        "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/diagnostico_imagem_em_uso_sus.csv",
    )
    #  EQUIPAMENTOS TOTAIS
    df_equip_totais_total, df_equip_totais_sus, df_equip_totais_nao_sus = (
        obter_estatisticas_totais(
            "./datasets/datasus_cnes/equipamentos/equipamentos_totais_em_uso.csv",
            "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/equipamentos_totais_em_uso_sus.csv",
        )
    )
    #  MANUTENÇÃO DA VIDA
    df_manu_total, df_manu_sus, df_manu_nao_sus = obter_estatisticas_manutencao_vida(
        "./datasets/datasus_cnes/equipamentos/manutencao_vida_em_uso.csv",
        "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/manutencao_vida_em_uso_sus.csv",
    )
    #  MÉTODOS GRÁFICOS
    df_graf_total, df_graf_sus, df_graf_nao_sus = obter_estatisticas_metodos_graficos(
        "./datasets/datasus_cnes/equipamentos/metodos_graficos_em_uso.csv",
        "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/metodos_graficos_em_uso_sus.csv",
    )

    # inspecionar_dados(df_populacao, 'Dados de População')

    # caminhos dos arquivos de leitos
    caminhos_leitos = {
        "repouso_fem": "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_feminino.csv",
        "repouso_ind": "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_indiferente.csv",
        "repouso_masc": "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_masculino.csv",
        "repouso_ped": "./datasets/datasus_cnes/leitos_urgencia/leitos_repouso_observacao_pediatria.csv",
        "comp_nao_sus": "./datasets/datasus_cnes/leitos_complementares_nao_sus.csv",
        "comp_sus": "./datasets/datasus_cnes/leitos_complementares_sus.csv",
        "enf_nao_sus": "./datasets/datasus_cnes/leitos_enfermaria_nao_sus.csv",
        "enf_sus": "./datasets/datasus_cnes/leitos_enfermaria_sus.csv",
    }

    df_blocos_leitos = extrair_bloco_infraestrutura(caminhos_leitos)

    # Caminhos dos arquivos de equipamentos
    caminhos_equipamentos = {
        "diag_imagem": "./datasets/datasus_cnes/equipamentos/diagnostico_imagem_em_uso.csv",
        "totais": "./datasets/datasus_cnes/equipamentos/equipamentos_totais_em_uso.csv",
        "manut_vida": "./datasets/datasus_cnes/equipamentos/manutencao_vida_em_uso.csv",
        "met_graficos": "./datasets/datasus_cnes/equipamentos/metodos_graficos_em_uso.csv",
        "diag_imagem_sus": "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/diagnostico_imagem_em_uso_sus.csv",
        "totais_sus": "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/equipamentos_totais_em_uso_sus.csv",
        "manut_vida_sus": "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/manutencao_vida_em_uso_sus.csv",
        "met_graficos_sus": "./datasets/datasus_cnes/equipamentos/somente_em_uso_sus/metodos_graficos_em_uso_sus.csv",
    }

    # Chama o módulo para processar os 8 datasets de equipamentos
    df_blocos_equipamentos = extrair_bloco_equipamentos(caminhos_equipamentos)

    print("Empilhando os dados para consolida-los")
    dfs = [
        df_internacoes,
        df_permanencia,
        df_gini,
        df_renda,
        df_pib,
        df_obitos_hospitalares,
        df_populacao,
        df_obitos_evitaveis,
        df_idhm,
    ]
    df_consolidado = reduce(
        lambda esquerda, direita: pd.merge(
            esquerda,
            direita,
            on=["id_unidade_federativa", "nome_unidade_federativa", "ano"],
            how="left",
        ),
        dfs,
    )

    inspecionar_dados(df_consolidado, "todos os dados")

    print("Juntando todos os dados dos leitos ao dataset consolidado")
    df_consolidado = pd.merge(
        df_consolidado,
        df_blocos_leitos,
        on=["id_unidade_federativa", "nome_unidade_federativa", "ano"],
        how="left",
    )

    print("Juntando dados dos equipamentos ao dataset consolidado...")
    df_consolidado = pd.merge(
        df_consolidado,
        df_blocos_equipamentos,
        on=["id_unidade_federativa", "nome_unidade_federativa", "ano"],
        how="left",
    )

df_consolidado.to_csv(
    "./datasets/dataset_completo_consolidado.csv", index=False, encoding="utf-8"
)
