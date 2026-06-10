import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm

# ==============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==============================================================================
print("\n[1/2] A carregar e a preparar a Tabela Mestra Consolidada...")
df = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

df["ano"] = df["ano"].astype(str)

# Corrigir o formato do Gini, IDHM e Renda
for col in ["indice_gini", "idhm", "renda_per_capita"]:
    if col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(",", ".", regex=False).astype(float)

# Lista completa de colunas numéricas
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
    "internacoes_sus_total",
    "obitos_domicilio_geral",
    "Cap IX_geral",
    "obitos_hospital_geral",
    "dias_internacao_sus_total",
    "obitos_hospitalares",
    "dias_internacao",
]

for col in colunas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Limpeza Básica
colunas_vitais = ["populacao", "ano", "nome_unidade_federativa"]
df = df.dropna(subset=[c for c in colunas_vitais if c in df.columns])
df = df[(df["populacao"] > 0)]
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

# ------------------------------------------------------------------------------
# FEATURE ENGINEERING & LIMITES DE EIXO
# ------------------------------------------------------------------------------
LIMITES = {}

if "media_leitos_uti_sus" in df.columns:
    df["leitos_uti_sus_100k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 100000
    df["leitos_uti_sus_1k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 1000
    LIMITES["max_uti_1k"] = df["leitos_uti_sus_1k"].max() * 1.1
    LIMITES["max_uti_100k"] = df["leitos_uti_sus_100k"].max() * 1.1

if "media_leitos_uti_nao_sus" in df.columns:
    df["leitos_uti_privado_100k"] = (
        df["media_leitos_uti_nao_sus"] / df["populacao"]
    ) * 100000

if "media_leitos_enf_sus" in df.columns:
    df["leitos_enf_sus_1k"] = (df["media_leitos_enf_sus"] / df["populacao"]) * 1000
    LIMITES["max_enf"] = df["leitos_enf_sus_1k"].max() * 1.1

if "obitos_evitaveis" in df.columns:
    df["mortalidade_evitavel_100k"] = (
        df["obitos_evitaveis"] / df["populacao"]
    ) * 100000
    LIMITES["max_mort"] = df["mortalidade_evitavel_100k"].max() * 1.1

if "internacoes" in df.columns:
    df["internacoes_100k"] = (df["internacoes"] / df["populacao"]) * 100000
    LIMITES["max_int"] = df["internacoes_100k"].max() * 1.1

if "media_equip_manut_vida_sus" in df.columns:
    df["equip_vida_sus_100k"] = (
        df["media_equip_manut_vida_sus"] / df["populacao"]
    ) * 100000
    LIMITES["max_equip"] = df["equip_vida_sus_100k"].max() * 1.1

if "obitos_hospitalares" in df.columns and "obitos_evitaveis" in df.columns:
    df["pct_mortes_evitaveis"] = (
        df["obitos_evitaveis"] / df["obitos_hospitalares"]
    ) * 100
    LIMITES["max_pct_evit"] = df["pct_mortes_evitaveis"].max() * 1.1

if "dias_internacao" in df.columns and "internacoes" in df.columns:
    df["dias_por_internacao"] = df["dias_internacao"] / df["internacoes"]
    LIMITES["max_dias_por_int"] = df["dias_por_internacao"].max() * 1.1

if "pib_milhares" in df.columns:
    df["pib_per_capita_absoluto"] = (df["pib_milhares"] * 1000) / df["populacao"]
    LIMITES["max_pib"] = df["pib_per_capita_absoluto"].max() * 1.1

if "media_leitos_uti_sus" in df.columns and "media_leitos_uti_nao_sus" in df.columns:
    df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]
    df["pct_uti_sus"] = np.where(
        df["total_uti"] > 0, (df["media_leitos_uti_sus"] / df["total_uti"]) * 100, 0
    )

if "internacoes_sus_total" in df.columns:
    df["internacoes_sus_100k"] = (
        df["internacoes_sus_total"] / df["populacao"]
    ) * 100000
    LIMITES["max_int_sus"] = df["internacoes_sus_100k"].max() * 1.1

if "obitos_domicilio_geral" in df.columns:
    df["obitos_domicilio_100k"] = (
        df["obitos_domicilio_geral"] / df["populacao"]
    ) * 100000
    LIMITES["max_obitos_dom"] = df["obitos_domicilio_100k"].max() * 1.1

if "Cap IX_geral" in df.columns:
    df["cap_ix_100k"] = (df["Cap IX_geral"] / df["populacao"]) * 100000
    LIMITES["max_cap_ix"] = df["cap_ix_100k"].max() * 1.1

if "obitos_hospital_geral" in df.columns:
    df["obitos_hospital_100k"] = (
        df["obitos_hospital_geral"] / df["populacao"]
    ) * 100000
    LIMITES["max_obitos_hosp"] = df["obitos_hospital_100k"].max() * 1.1

if "dias_internacao_sus_total" in df.columns:
    df["dias_internacao_sus_100k"] = (
        df["dias_internacao_sus_total"] / df["populacao"]
    ) * 100000
    LIMITES["max_dias_int"] = df["dias_internacao_sus_100k"].max() * 1.1

if "idhm" in df.columns:
    LIMITES["min_idhm"] = df["idhm"].min() * 0.95
    LIMITES["max_idhm"] = df["idhm"].max() * 1.05

if "indice_gini" in df.columns:
    LIMITES["min_gini"] = df["indice_gini"].min() * 0.95
    LIMITES["max_gini"] = df["indice_gini"].max() * 1.05

print("[2/2] Dados processados com sucesso!\n")


# ==============================================================================
# 2. FUNÇÕES GERADORAS DE GRÁFICOS DINÂMICOS
# ==============================================================================


def gerador_grafico(
    df_dados,
    x_col,
    y_col,
    modo,
    titulo_animado,
    titulo_consol,
    color="regiao_ibge",
    size=None,
    max_x=None,
    max_y=None,
    min_x=0,
    min_y=0,
    discrete_colors=px.colors.qualitative.Safe,
):
    """Função mestre adaptada para animar a Linha Nacional corretamente"""
    if x_col not in df_dados.columns or y_col not in df_dados.columns:
        print(f"\n[ERRO] Variáveis '{x_col}' ou '{y_col}' não encontradas no dataset.")
        return

    print("A renderizar gráfico...")

    # Criamos uma cópia para não alterar o DataFrame original
    data = df_dados.copy()
    cor_grafico = color
    escopo_tendencia = "trace"

    if modo == "consolidado":
        data = (
            data.groupby(["nome_unidade_federativa", "regiao_ibge"])
            .mean(numeric_only=True)
            .reset_index()
        )
        kwargs = {}
        titulo = titulo_consol
        escopo_tendencia = "overall"
    else:
        kwargs = {
            "animation_frame": "ano",
            "animation_group": "nome_unidade_federativa",
        }
        if max_x:
            kwargs["range_x"] = [min_x, max_x]
        if max_y:
            kwargs["range_y"] = [min_y, max_y]

        if modo == "animado_nacional":
            titulo = (
                titulo_animado
                + " <br><sup>(Tendência Nacional Dinâmica Ano a Ano)</sup>"
            )
            # O TRUQUE: Unificamos todos os estados numa única categoria para o Plotly animar a linha
            data["Visão Nacional"] = "Brasil (Todos os Estados)"
            cor_grafico = "Visão Nacional"
            discrete_colors = ["#2C3E50"]  # Um azul escuro elegante e neutro
            # Como agora só existe 1 categoria, a linha será geral e vai mover-se a cada ano!

        else:  # "animado_regional"
            titulo = (
                titulo_animado + " <br><sup>(Com Linhas de Tendência Regionais)</sup>"
            )
            cor_grafico = color  # Mantém as cores separadas por região

    if size and size in data.columns:
        kwargs["size"] = size
        kwargs["size_max"] = 45

    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=cor_grafico,
        hover_name="nome_unidade_federativa",
        trendline="ols",
        trendline_scope=escopo_tendencia,
        title=titulo,
        color_discrete_sequence=discrete_colors,
        **kwargs,
    )
    fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="black")))
    fig.update_layout(template="plotly_white")
    fig.show()


# --- BLOCO A: CLÍNICAS ---
def graf_alocacao_reativa(modo):
    gerador_grafico(
        df,
        "leitos_uti_sus_1k",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Alocação Reativa: Maior mortalidade induz mais UTIs</b>",
        "<b>[MÉDIA GERAL] Alocação Reativa: Maior mortalidade induz mais UTIs</b>",
        max_x=LIMITES.get("max_uti_1k"),
        max_y=LIMITES.get("max_mort"),
    )


def graf_fator_protecao(modo):
    gerador_grafico(
        df,
        "internacoes_100k",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Acesso Hospitalar Estruturado previne Mortes Agudas</b>",
        "<b>[MÉDIA GERAL] Acesso Hospitalar Estruturado previne Mortes Agudas</b>",
        max_x=LIMITES.get("max_int"),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=px.colors.qualitative.Vivid,
    )


def graf_enfermaria(modo):
    gerador_grafico(
        df,
        "leitos_enf_sus_1k",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Especialização: Sem correlação com Enfermaria</b>",
        "<b>[MÉDIA GERAL] Especialização: Sem correlação com Enfermaria</b>",
        max_x=LIMITES.get("max_enf"),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=["#7F8C8D"],
    )


# --- BLOCO B: VIESES SOCIAIS E MACROECONOMIA ---
def graf_paradoxo_regioes(modo):
    gerador_grafico(
        df,
        "leitos_uti_sus_100k",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Paradoxo Regional: Cargas diferentes</b>",
        "<b>[MÉDIA GERAL] Paradoxo Regional: Cargas diferentes</b>",
        size="populacao",
        max_x=LIMITES.get("max_uti_100k"),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=px.colors.qualitative.Prism,
    )


def graf_vies_confundimento(modo):
    gerador_grafico(
        df,
        "idhm",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Viés Socioeconômico: Mortalidade vs IDHM (Tamanho = UTIs)</b>",
        "<b>[MÉDIA GERAL] Viés Socioeconômico: Mortalidade vs IDHM (Tamanho = UTIs)</b>",
        size="leitos_uti_sus_100k",
        min_x=LIMITES.get("min_idhm", 0),
        max_x=LIMITES.get("max_idhm", 1),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=px.colors.qualitative.Bold,
    )


def graf_gini_mortalidade(modo):
    gerador_grafico(
        df,
        "indice_gini",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Desigualdade vs Mortalidade (GINI)</b>",
        "<b>[MÉDIA GERAL] Desigualdade vs Mortalidade (GINI)</b>",
        min_x=LIMITES.get("min_gini", 0),
        max_x=LIMITES.get("max_gini", 1),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=px.colors.qualitative.Pastel,
    )


def graf_pib_mortalidade(modo):
    gerador_grafico(
        df,
        "pib_per_capita_absoluto",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] Riqueza Absoluta vs Mortalidade (Tamanho = IDHM)</b>",
        "<b>[MÉDIA GERAL] Riqueza Absoluta vs Mortalidade (Tamanho = IDHM)</b>",
        size="idhm",
        max_x=LIMITES.get("max_pib"),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=px.colors.qualitative.Vivid,
    )


def graf_taxa_evitabilidade(modo):
    gerador_grafico(
        df,
        "idhm",
        "pct_mortes_evitaveis",
        modo,
        "<b>[ANIMADO] IDHM vs Taxa de Evitabilidade (% de Óbitos)</b>",
        "<b>[MÉDIA GERAL] IDHM vs Taxa de Evitabilidade (% de Óbitos)</b>",
        min_x=LIMITES.get("min_idhm", 0),
        max_x=LIMITES.get("max_idhm", 1),
        max_y=LIMITES.get("max_pct_evit", 100),
        discrete_colors=px.colors.qualitative.Prism,
    )


# --- BLOCO C: COLAPSO E GRAVIDADE ---
def graf_prova_colapso(modo):
    gerador_grafico(
        df,
        "internacoes_sus_100k",
        "obitos_domicilio_100k",
        modo,
        "<b>[ANIMADO] Prova do Colapso: Internações vs Mortes em Casa</b>",
        "<b>[MÉDIA GERAL] Prova do Colapso: Internações vs Mortes em Casa</b>",
        max_x=LIMITES.get("max_int_sus"),
        max_y=LIMITES.get("max_obitos_dom"),
        discrete_colors=px.colors.qualitative.Pastel,
    )


def graf_corrida_relogio(modo):
    gerador_grafico(
        df,
        "equip_vida_sus_100k",
        "cap_ix_100k",
        modo,
        "<b>[ANIMADO] Equipamentos de Vida vs Infartos/AVCs</b>",
        "<b>[MÉDIA GERAL] Equipamentos de Vida vs Infartos/AVCs</b>",
        size="populacao",
        max_x=LIMITES.get("max_equip"),
        max_y=LIMITES.get("max_cap_ix"),
        discrete_colors=px.colors.qualitative.Vivid,
    )


def graf_gargalo_gravidade(modo):
    df_temp = df.copy()
    if "leitos_uti_sus_100k" in df_temp.columns:
        df_temp["tamanho_bolha"] = df_temp["leitos_uti_sus_100k"].fillna(0) + 1
    gerador_grafico(
        df_temp,
        "dias_internacao_sus_100k",
        "obitos_hospital_100k",
        modo,
        "<b>[ANIMADO] O Gargalo: Dias Internação vs Letalidade</b>",
        "<b>[MÉDIA GERAL] O Gargalo: Tempo Espera e Mortalidade (Tamanho = UTIs)</b>",
        size="tamanho_bolha" if "tamanho_bolha" in df_temp.columns else None,
        max_x=LIMITES.get("max_dias_int"),
        max_y=LIMITES.get("max_obitos_hosp"),
        discrete_colors=px.colors.qualitative.Prism,
    )


# --- BLOCO D: VISÕES GLOBAIS PANORÂMICAS ---
def graf_evolucao_nacional_linha():
    evolucao = df.groupby("ano")[["obitos_evitaveis", "populacao"]].sum().reset_index()
    evolucao["taxa_obitos_100k"] = (
        evolucao["obitos_evitaveis"] / evolucao["populacao"]
    ) * 100000
    fig = px.line(
        evolucao,
        x="ano",
        y="taxa_obitos_100k",
        markers=True,
        title="<b>Evolução Nacional da Taxa de Óbitos Evitáveis (por 100k hab.)</b>",
    )
    fig.update_traces(line=dict(color="darkred", width=4), marker=dict(size=12))
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Ano",
        yaxis_title="Taxa Nacional de Óbitos Evitáveis",
    )
    fig.show()


def graf_mix_publico_privado(modo):
    if "pct_uti_sus" not in df.columns:
        return print("[ERRO] Variável não encontrada.")
    if modo == "consolidado":
        data = (
            df.groupby(["nome_unidade_federativa", "regiao_ibge"])[["pct_uti_sus"]]
            .mean(numeric_only=True)
            .reset_index()
            .sort_values(by="pct_uti_sus")
        )
        kwargs, titulo = {}, "<b>[MÉDIA GERAL] Assimetria do Mix Público-Privado</b>"
    else:
        data, kwargs, titulo = (
            df.sort_values(by=["ano", "regiao_ibge", "pct_uti_sus"]),
            {"animation_frame": "ano", "animation_group": "nome_unidade_federativa"},
            "<b>[ANIMADO] Mix Público-Privado: Corrida da Dependência</b>",
        )
    fig = px.bar(
        data,
        x="pct_uti_sus",
        y="nome_unidade_federativa",
        color="regiao_ibge",
        orientation="h",
        range_x=[0, 100],
        title=titulo,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        **kwargs,
    )
    fig.add_vline(x=50, line_dash="dash", line_color="black")
    fig.update_layout(
        template="plotly_white", yaxis=dict(autorange="reversed"), height=750
    )
    fig.show()


def graf_heatmap_regional():
    pivot_obitos = df.pivot_table(
        index="nome_unidade_federativa",
        columns="ano",
        values="mortalidade_evitavel_100k",
        aggfunc="mean",
    )
    fig = px.imshow(
        pivot_obitos,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="YlOrRd",
        title="<b>Mapa de Calor: Taxa de Óbitos Evitáveis por UF e Ano</b>",
    )
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Unidade Federativa",
        template="plotly_white",
        height=700,
    )
    fig.show()


def graf_matriz_correlacao():
    cols = [
        "mortalidade_evitavel_100k",
        "indice_gini",
        "idhm",
        "pib_per_capita_absoluto",
        "pct_uti_sus",
        "pct_mortes_evitaveis",
        "dias_por_internacao",
        "equip_vida_sus_100k",
    ]
    corr = df[[c for c in cols if c in df.columns]].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="<b>Matriz de Correlação Global</b>",
    )
    fig.update_layout(template="plotly_white", height=700)
    fig.show()


def graf_eixo_duplo_historico():
    evolucao = (
        df.groupby("ano")[
            [
                "populacao",
                "obitos_evitaveis",
                "media_leitos_uti_sus",
                "media_leitos_uti_nao_sus",
            ]
        ]
        .sum()
        .reset_index()
    )
    evolucao["taxa_mort"] = (
        evolucao["obitos_evitaveis"] / evolucao["populacao"]
    ) * 100000
    evolucao["uti_sus"] = (
        evolucao["media_leitos_uti_sus"] / evolucao["populacao"]
    ) * 100000
    evolucao["uti_privado"] = (
        evolucao["media_leitos_uti_nao_sus"] / evolucao["populacao"]
    ) * 100000

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=evolucao["ano"],
            y=evolucao["uti_sus"],
            name="UTIs SUS/100k",
            line=dict(color="#008080", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=evolucao["ano"],
            y=evolucao["uti_privado"],
            name="UTIs Privadas/100k",
            line=dict(color="#E67E22", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=evolucao["ano"],
            y=evolucao["taxa_mort"],
            name="Taxa Mortalidade/100k",
            line=dict(color="darkred", width=4, dash="dot"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="<b>Evolução Histórica Nacional Real</b>",
        template="plotly_white",
        hovermode="x unified",
    )
    fig.show()


# --- ESTATÍSTICA ---
def rodar_regressao_ols():
    print("\n" + "=" * 50 + "\nRESULTADO DO MODELO DE REGRESSÃO (OLS)\n" + "=" * 50)
    try:
        df_reg = df.dropna(
            subset=[
                "leitos_uti_sus_100k",
                "idhm",
                "indice_gini",
                "mortalidade_evitavel_100k",
            ]
        )
        X = sm.add_constant(df_reg[["leitos_uti_sus_100k", "idhm", "indice_gini"]])
        print(sm.OLS(df_reg["mortalidade_evitavel_100k"], X).fit().summary())
    except Exception as e:
        print(f"Erro: {e}")
    print("=" * 50 + "\n")


def graf_ranking_cid10():
    print("A renderizar o Ranking de Causas (CID-10)...")

    # 1. Encontrar as colunas do CID-10:
    # - Que começam com 'Cap '
    # - Que NÃO terminam em '_y' (remove duplicados)
    # - Que NÃO contêm a palavra 'ignorado'
    cols_cid = [
        c
        for c in df.columns
        if c.startswith("Cap ") and not c.endswith("_y") and "ignorado" not in c.lower()
    ]

    if not cols_cid:
        print("\n[ERRO] Não foram encontradas colunas do CID-10 válidas.")
        return

    # 2. Agrupar por ano e somar os valores para o Brasil inteiro
    df_cid = df.groupby("ano")[cols_cid].sum().reset_index()

    # 3. Transformar as colunas em linhas (Melt) para o Plotly entender
    df_melt = df_cid.melt(
        id_vars=["ano"],
        value_vars=cols_cid,
        var_name="Capitulo",
        value_name="Total_Obitos",
    )

    # 4. Limpeza da Legenda: Remove o '_x' e o '_geral' para o gráfico ficar elegante
    df_melt["Capitulo"] = df_melt["Capitulo"].str.replace("_x", "", regex=False)
    df_melt["Capitulo"] = df_melt["Capitulo"].str.replace("_geral", "", regex=False)

    # [OPCIONAL MAS RECOMENDADO]: Remover também as linhas onde o total de óbitos é zero
    # Isso evita que categorias vazias fiquem empilhadas lá no fundo do eixo Y
    df_melt = df_melt[df_melt["Total_Obitos"] > 0]

    # 5. Ordenar os dados para a animação fluir corretamente
    df_melt = df_melt.sort_values(by=["ano", "Total_Obitos"], ascending=[True, True])

    # Descobrir o limite do eixo X para a barra não sair da tela
    limite_max = df_melt["Total_Obitos"].max() * 1.15

    # 6. Gerar a Corrida de Barras
    fig = px.bar(
        df_melt,
        x="Total_Obitos",
        y="Capitulo",
        animation_frame="ano",
        orientation="h",
        title="<b>Ranking de Causas: Evolução dos Óbitos por Capítulo (CID-10)</b>",
        labels={"Total_Obitos": "Volume Total de Óbitos", "Capitulo": "CID-10"},
        color="Capitulo",
        text="Total_Obitos",
    )

    # Formatação visual: números fora da barra e abreviados
    fig.update_traces(texttemplate="%{text:.3s}", textposition="outside")
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        height=800,
        xaxis=dict(range=[0, limite_max]),  # Eixo X fixo para a corrida funcionar
        yaxis=dict(categoryorder="total ascending"),  # Mantém o maior no topo
    )
    fig.show()


# ==============================================================================
# 3. INTERFACE DE TERMINAL
# ==============================================================================
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def perguntar_modo_dispersao():
    print("\n   \033[93mComo deseja visualizar as Linhas de Correlação?\033[0m")
    print(
        "   [1] \033[96mAnimado (Linha Geral)\033[0m       - Evolução com a tendência do Brasil"
    )
    print(
        "   [2] \033[96mAnimado (Linhas Regionais)\033[0m  - Evolução com a tendência de cada Região"
    )
    print(
        "   [3] \033[95mVisão Geral Consolidada\033[0m     - Média Histórica Congelada (Todos os anos)"
    )
    while True:
        resp = input("   👉 Escolha (1, 2 ou 3) » ")
        if resp == "1":
            return "animado_nacional"
        if resp == "2":
            return "animado_regional"
        if resp == "3":
            return "consolidado"
        print("   Opção inválida.")


def perguntar_modo_simples():
    print("\n   \033[93mComo deseja visualizar este gráfico?\033[0m")
    print("   [1] \033[96mAnimado\033[0m     - Evolução Ano a Ano")
    print("   [2] \033[95mVisão Geral\033[0m - Média Consolidada de Todos os Anos")
    while True:
        resp = input("   👉 Escolha (1 ou 2) » ")
        if resp == "1":
            return "animado"
        if resp == "2":
            return "consolidado"
        print("   Opção inválida.")


def menu_principal():
    COR_TITULO, COR_SECCAO, COR_OPCAO, COR_RESET = (
        "\033[95m",
        "\033[96m",
        "\033[92m",
        "\033[0m",
    )

    while True:
        limpar_tela()
        print(
            f"{COR_TITULO}╔════════════════════════════════════════════════════════════╗\n║     PAINEL DE ANÁLISE: SAÚDE PÚBLICA E MORTALIDADE         ║\n╚════════════════════════════════════════════════════════════╝{COR_RESET}"
        )
        print(
            f"\n {COR_SECCAO}📊 [BLOCO A] STORYTELLING & RELAÇÕES CLÍNICAS{COR_RESET}"
        )
        print(
            f"   {COR_OPCAO}1.{COR_RESET} Alocação Reativa     --> UTIs vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}2.{COR_RESET} Fator de Proteção    --> Internações vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}3.{COR_RESET} Nível Complexidade   --> Enfermaria vs Mortalidade"
        )

        print(f"\n {COR_SECCAO}🌍 [BLOCO B] MACROECONOMIA & VIÉS SOCIAL{COR_RESET}")
        print(
            f"   {COR_OPCAO}4.{COR_RESET} Paradoxo Regional    --> Carga Epidemiológica por População"
        )
        print(
            f"   {COR_OPCAO}5.{COR_RESET} Viés IDHM            --> IDHM vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}6.{COR_RESET} Viés Desigualdade    --> Índice de GINI vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}7.{COR_RESET} Viés Riqueza (PIB)   --> PIB per Capita vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}8.{COR_RESET} Evitabilidade        --> IDHM vs % de Mortes Evitáveis"
        )

        print(f"\n {COR_SECCAO}🚨 [BLOCO C] COLAPSO E LETALIDADE{COR_RESET}")
        print(
            f"   {COR_OPCAO}9.{COR_RESET} Prova do Colapso     --> Internações vs Morte em Domicílio"
        )
        print(
            f"   {COR_OPCAO}10.{COR_RESET} Corrida p/ Vida     --> Equipamentos vs Doenças Cap IX"
        )
        print(
            f"   {COR_OPCAO}11.{COR_RESET} O Gargalo da Fila   --> Dias Internados vs Morte Hospitalar"
        )

        print(f"\n {COR_SECCAO}📈 [BLOCO D] VISÕES GLOBAIS PANORÂMICAS{COR_RESET}")
        print(
            f"   {COR_OPCAO}12.{COR_RESET} Evolução Nacional   --> Linha do Tempo (Taxa Brasil)"
        )
        print(
            f"   {COR_OPCAO}13.{COR_RESET} Mix Público/Privado --> Corrida de Barras (% de UTI SUS)"
        )
        print(
            f"   {COR_OPCAO}14.{COR_RESET} Mapa de Calor       --> Evolução Regional por Ano"
        )
        print(
            f"   {COR_OPCAO}15.{COR_RESET} Matriz de Correlação--> Interação Global de Variáveis"
        )
        print(
            f"   {COR_OPCAO}16.{COR_RESET} Eixo Duplo Histórico--> Infraestrutura vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}17.{COR_RESET} Ranking Causas Morte--> Corrida de Capítulos do CID-10"
        )

        print(f"\n {COR_SECCAO}⚙️  [BLOCO E] MODELAÇÃO MATEMÁTICA{COR_RESET}")
        print(
            f"   {COR_OPCAO}18.{COR_RESET} Executar Regressão OLS (Sumário Estatístico)"
        )
        print(
            f"{COR_TITULO}────────────────────────────────────────────────────────────\n   {COR_OPCAO}0. Sair do Programa{COR_RESET}\n────────────────────────────────────────────────────────────{COR_RESET}"
        )

        try:
            escolha = input(f"\n👉 Selecione o Gráfico/Ação: {COR_OPCAO}")
            print(f"{COR_RESET}", end="")
        except:
            sys.exit()

        if escolha in [str(i) for i in range(1, 12)]:
            modo = perguntar_modo_dispersao()
            if escolha == "1":
                graf_alocacao_reativa(modo)
            elif escolha == "2":
                graf_fator_protecao(modo)
            elif escolha == "3":
                graf_enfermaria(modo)
            elif escolha == "4":
                graf_paradoxo_regioes(modo)
            elif escolha == "5":
                graf_vies_confundimento(modo)
            elif escolha == "6":
                graf_gini_mortalidade(modo)
            elif escolha == "7":
                graf_pib_mortalidade(modo)
            elif escolha == "8":
                graf_taxa_evitabilidade(modo)
            elif escolha == "9":
                graf_prova_colapso(modo)
            elif escolha == "10":
                graf_corrida_relogio(modo)
            elif escolha == "11":
                graf_gargalo_gravidade(modo)
            input("\nPressione [ENTER] para voltar...")

        elif escolha in ["12", "13", "14", "15", "16", "17"]:
            if escolha == "12":
                graf_evolucao_nacional_linha()
            elif escolha == "13":
                graf_mix_publico_privado(perguntar_modo_simples())
            elif escolha == "14":
                graf_heatmap_regional()
            elif escolha == "15":
                graf_matriz_correlacao()
            elif escolha == "16":
                graf_eixo_duplo_historico()
            elif escolha == "17":
                graf_ranking_cid10()
            input("\nPressione [ENTER] para voltar...")

        elif escolha == "18":
            limpar_tela()
            rodar_regressao_ols()
            input("\nPressione [ENTER] para voltar...")
        elif escolha == "0":
            limpar_tela()
            print("\nPrograma encerrado!\n")
            sys.exit()
        else:
            input("\nOpção inválida! Pressione [ENTER] para tentar novamente...")


if __name__ == "__main__":
    menu_principal()
