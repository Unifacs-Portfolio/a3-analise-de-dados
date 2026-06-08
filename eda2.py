import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm

# ==============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS (Roda apenas uma vez)
# ==============================================================================
print("\n[1/2] A carregar e a preparar a Tabela Mestra Consolidada...")
df = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

df["ano"] = df["ano"].astype(str)

# Corrigir o formato do Gini, IDHM e Renda
for col in ["indice_gini", "idhm", "renda_per_capita"]:
    if col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(",", ".", regex=False).astype(float)

colunas_numericas = [
    "renda_per_capita",
    "media_leitos_uti_sus",
    "media_equip_manut_vida_sus",
    "populacao",
    "media_leitos_uti_nao_sus",
    "idhm",
    "pib_milhares",
    "obitos_evitaveis",
    "internacoes",
    "media_leitos_enf_sus",
]

for col in colunas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

colunas_vitais = [c for c in colunas_numericas if c in df.columns] + [
    "indice_gini",
    "ano",
    "nome_unidade_federativa",
]
df = df.dropna(subset=colunas_vitais)
df = df[
    (df["populacao"] > 0)
    & (df["media_leitos_uti_sus"] >= 0)
    & (df["media_leitos_uti_nao_sus"] >= 0)
]
df = df.sort_values(by=["ano", "nome_unidade_federativa"])

# Mapeamento Espacial
regioes = {
    "Acre": "Norte",
    "Amapá": "Norte",
    "Amazonas": "Norte",
    "Pará": "Norte",
    "Rondônia": "Norte",
    "Roraima": "Norte",
    "Tocantins": "Norte",
    "Alagoas": "Nordeste",
    "Bahia": "Nordeste",
    "Ceará": "Nordeste",
    "Maranhão": "Nordeste",
    "Paraíba": "Nordeste",
    "Pernambuco": "Nordeste",
    "Piauí": "Nordeste",
    "Rio Grande do Norte": "Nordeste",
    "Sergipe": "Nordeste",
    "Espírito Santo": "Sudeste",
    "Minas Gerais": "Sudeste",
    "Rio de Janeiro": "Sudeste",
    "São Paulo": "Sudeste",
    "Paraná": "Sul",
    "Rio Grande do Sul": "Sul",
    "Santa Catarina": "Sul",
    "Distrito Federal": "Centro-Oeste",
    "Goiás": "Centro-Oeste",
    "Mato Grosso": "Centro-Oeste",
    "Mato Grosso do Sul": "Centro-Oeste",
}
df["regiao_ibge"] = df["nome_unidade_federativa"].map(regioes)

# Feature Engineering
df["leitos_uti_sus_100k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 100000
df["leitos_uti_sus_1k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 1000
df["leitos_enf_sus_1k"] = (df["media_leitos_enf_sus"] / df["populacao"]) * 1000
df["mortalidade_evitavel_100k"] = (df["obitos_evitaveis"] / df["populacao"]) * 100000
df["internacoes_100k"] = (df["internacoes"] / df["populacao"]) * 100000
df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]
df["pct_uti_sus"] = np.where(
    df["total_uti"] > 0, (df["media_leitos_uti_sus"] / df["total_uti"]) * 100, 0
)

# Limites Globais para os Eixos (Animações)
LIMITES = {
    "max_mort": df["mortalidade_evitavel_100k"].max() * 1.1,
    "max_uti_1k": df["leitos_uti_sus_1k"].max() * 1.1,
    "max_uti_100k": df["leitos_uti_sus_100k"].max() * 1.1,
    "max_int": df["internacoes_100k"].max() * 1.1,
    "max_enf": df["leitos_enf_sus_1k"].max() * 1.1,
    "min_idhm": df["idhm"].min() * 0.95,
    "max_idhm": df["idhm"].max() * 1.05,
}

print("[2/2] Dados processados com sucesso!\n")


# ==============================================================================
# 2. FUNÇÕES GERADORAS DE GRÁFICOS
# ==============================================================================


def graf_alocacao_reativa():
    print("A gerar Gráfico 1...")
    fig = px.scatter(
        df,
        x="leitos_uti_sus_1k",
        y="mortalidade_evitavel_100k",
        color="regiao_ibge",
        animation_frame="ano",
        animation_group="nome_unidade_federativa",
        hover_name="nome_unidade_federativa",
        trendline="ols",
        range_x=[0, LIMITES["max_uti_1k"]],
        range_y=[0, LIMITES["max_mort"]],
        title="<b>[ANIMADO] Alocação Reativa: Maior mortalidade induz mais UTIs</b>",
        labels={
            "leitos_uti_sus_1k": "Leitos UTI SUS (por 1k hab.)",
            "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
            "regiao_ibge": "Região",
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig.update_layout(template="plotly_white")
    fig.show()


def graf_fator_protecao():
    print("A gerar Gráfico 2...")
    fig = px.scatter(
        df,
        x="internacoes_100k",
        y="mortalidade_evitavel_100k",
        color="regiao_ibge",
        animation_frame="ano",
        animation_group="nome_unidade_federativa",
        hover_name="nome_unidade_federativa",
        trendline="ols",
        range_x=[0, LIMITES["max_int"]],
        range_y=[0, LIMITES["max_mort"]],
        title="<b>[ANIMADO] Acesso Hospitalar Estruturado previne Mortes Agudas</b>",
        labels={
            "internacoes_100k": "Taxa de Internações (por 100k)",
            "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
        },
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(template="plotly_white")
    fig.show()


def graf_enfermaria():
    print("A gerar Gráfico 3...")
    fig = px.scatter(
        df,
        x="leitos_enf_sus_1k",
        y="mortalidade_evitavel_100k",
        animation_frame="ano",
        animation_group="nome_unidade_federativa",
        hover_name="nome_unidade_federativa",
        trendline="ols",
        range_x=[0, LIMITES["max_enf"]],
        range_y=[0, LIMITES["max_mort"]],
        title="<b>[ANIMADO] A Necessidade de Especialização (Sem correlação com Enfermaria)</b>",
        labels={
            "leitos_enf_sus_1k": "Enfermaria SUS (por 1k hab.)",
            "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
        },
        color_discrete_sequence=["#7F8C8D"],
    )
    fig.update_layout(template="plotly_white")
    fig.show()


def graf_paradoxo_regioes():
    print("A gerar Gráfico 4...")
    fig = px.scatter(
        df,
        x="leitos_uti_sus_100k",
        y="mortalidade_evitavel_100k",
        color="regiao_ibge",
        size="populacao",
        animation_frame="ano",
        animation_group="nome_unidade_federativa",
        hover_name="nome_unidade_federativa",
        trendline="ols",
        range_x=[0, LIMITES["max_uti_100k"]],
        range_y=[0, LIMITES["max_mort"]],
        size_max=50,
        title="<b>[ANIMADO] O Paradoxo Reativo: Blocos regionais sofrendo cargas diferentes</b>",
        labels={
            "leitos_uti_sus_100k": "Leitos UTI SUS (por 100k)",
            "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
        },
        color_discrete_sequence=px.colors.qualitative.Prism,
    )
    fig.update_layout(template="plotly_white")
    fig.show()


def graf_vies_confundimento():
    print("A gerar Gráfico 5...")
    fig = px.scatter(
        df,
        x="idhm",
        y="mortalidade_evitavel_100k",
        color="regiao_ibge",
        size="leitos_uti_sus_100k",
        animation_frame="ano",
        animation_group="nome_unidade_federativa",
        hover_name="nome_unidade_federativa",
        trendline="ols",
        range_x=[LIMITES["min_idhm"], LIMITES["max_idhm"]],
        range_y=[0, LIMITES["max_mort"]],
        size_max=40,
        title="<b>[ANIMADO] Viés Socioeconômico: Mortalidade vs Desenvolvimento (Tamanho = UTIs)</b>",
        labels={
            "idhm": "IDHM",
            "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
        },
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_layout(template="plotly_white")
    fig.show()


def graf_mix_publico_privado():
    print("A gerar Gráfico 6...")
    df_mix = df.sort_values(by=["ano", "regiao_ibge", "pct_uti_sus"])
    fig = px.bar(
        df_mix,
        x="pct_uti_sus",
        y="nome_unidade_federativa",
        color="regiao_ibge",
        animation_frame="ano",
        animation_group="nome_unidade_federativa",
        orientation="h",
        range_x=[0, 100],
        title="<b>[ANIMADO] Assimetria do Mix Público-Privado (Corrida da Dependência do SUS)</b>",
        labels={
            "pct_uti_sus": "UTIs pertencentes ao SUS (%)",
            "nome_unidade_federativa": "Estado",
        },
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.add_vline(x=50, line_dash="dash", line_color="black")
    fig.update_layout(
        template="plotly_white", yaxis=dict(autorange="reversed"), height=750
    )
    fig.show()


def rodar_regressao_ols():
    print("\n" + "=" * 50)
    print("RESULTADO DO MODELO DE REGRESSÃO (OLS)")
    print("=" * 50)
    try:
        X = df[["leitos_uti_sus_100k", "idhm", "indice_gini"]]
        X = sm.add_constant(X)
        Y = df["mortalidade_evitavel_100k"]
        modelo_ols = sm.OLS(Y, X).fit()
        print(modelo_ols.summary())
    except Exception as e:
        print(f"Erro ao rodar regressão: {e}")
    print("=" * 50 + "\n")


# ==============================================================================
# 3. MENU INTERATIVO NO TERMINAL (VERSÃO REMODELADA)
# ==============================================================================


def limpar_tela():
    # Limpa o terminal dependendo do sistema operacional (Windows ou Linux/Mac)
    os.system("cls" if os.name == "nt" else "clear")


def menu_principal():
    while True:
        limpar_tela()
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║        SISTEMA DE ANÁLISE: INFRAESTRUTURA E SAÚDE PÚBLICA          ║")
        print("╠════════════════════════════════════════════════════════════════════╣")
        print("║                                                                    ║")
        print("║  [1]  Alocação Reativa (UTIs vs Mortalidade)                       ║")
        print("║  [2]  Fator de Proteção (Internações vs Mortalidade)               ║")
        print("║  [3]  Especialização do Cuidado (Enfermaria vs Mortalidade)        ║")
        print("║  [4]  Paradoxo Regional (Bolhas por População)                     ║")
        print("║  [5]  Viés de Confundimento (Mortalidade vs IDHM)                  ║")
        print("║  [6]  Mix Público/Privado (Corrida de Barras % SUS)                ║")
        print("║                                                                    ║")
        print("╠════════════════════════════════════════════════════════════════════╣")
        print("║  [7]  Rodar Análise Estatística (Regressão OLS no Terminal)        ║")
        print("║  [8]  Abrir TODOS os Gráficos Animados (Consome muita RAM!)        ║")
        print("║                                                                    ║")
        print("║  [0]  Sair do Programa                                             ║")
        print("║                                                                    ║")
        print("╚════════════════════════════════════════════════════════════════════╝")

        try:
            escolha = input("\nDigite o número da opção desejada » ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nPrograma interrompido. Até logo!")
            sys.exit()

        print("\n" + "─" * 70)
        if escolha == "1":
            graf_alocacao_reativa()
        elif escolha == "2":
            graf_fator_protecao()
        elif escolha == "3":
            graf_enfermaria()
        elif escolha == "4":
            graf_paradoxo_regioes()
        elif escolha == "5":
            graf_vies_confundimento()
        elif escolha == "6":
            graf_mix_publico_privado()
        elif escolha == "7":
            limpar_tela()
            rodar_regressao_ols()
            input("\nPressione [ENTER] para voltar ao menu principal...")
        elif escolha == "8":
            print("A inicializar todas as instâncias do Plotly no navegador...")
            graf_alocacao_reativa()
            graf_fator_protecao()
            graf_enfermaria()
            graf_paradoxo_regioes()
            graf_vies_confundimento()
            graf_mix_publico_privado()
        elif escolha == "0":
            limpar_tela()
            print("\n[INFO] Programa encerrado com sucesso. Até à próxima!\n")
            sys.exit()
        else:
            print("[ERRO] Opção inválida! Por favor, escolha um número de 0 a 8.")
            input("\nPressione [ENTER] para tentar novamente...")


# Ponto de entrada do programa
if __name__ == "__main__":
    menu_principal()
