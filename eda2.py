import pandas as pd
import numpy as np
import plotly.express as px

# ==============================================================================
# CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==============================================================================
print("\nA carregar a Tabela Mestra Consolidada...")
df = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

# Tipagem das chaves de cruzamento
df["ano"] = df["ano"].astype(str)
if "id_unidade_federativa" in df.columns:
    df["id_unidade_federativa"] = df["id_unidade_federativa"].astype(str)

# Correção do formato do Gini
if df["indice_gini"].dtype == object:
    df["indice_gini"] = (
        df["indice_gini"].str.replace(",", ".", regex=False).astype(float)
    )

# Colunas numéricas essenciais (incluindo as geradas pelo etlv2.py)
colunas_numericas = [
    "obitos_evitaveis",
    "renda_per_capita",
    "media_leitos_uti_sus",
    "media_equip_manut_vida_sus",
    "populacao",
    "media_leitos_uti_nao_sus",
    "obitos_hospitalares",
    "dias_internacao",
    "internacoes",
    "idhm",
    "pib_milhares",
    "idhm_l",
    "obitos_hospital",
    "obitos_outro_estab_saude",
    "obitos_domicilio",
    "obitos_via_publica",
]

# Forçar conversão numérica e tratar erros
for col in colunas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Limpeza de nulos apenas nas colunas vitais para a análise base
colunas_vitais = [
    "obitos_evitaveis",
    "populacao",
    "obitos_hospitalares",
    "internacoes",
    "media_leitos_uti_sus",
    "media_leitos_uti_nao_sus",
    "indice_gini",
    "ano",
    "nome_unidade_federativa",
]
colunas_analise = [c for c in colunas_vitais if c in df.columns]
df = df.dropna(subset=colunas_analise)

# Filtros lógicos para evitar distorções ou divisões por zero
df = df[
    (df["obitos_evitaveis"] > 0)
    & (df["populacao"] > 0)
    & (df["obitos_hospitalares"] > 0)
    & (df["internacoes"] > 0)
    & (df["media_leitos_uti_sus"] >= 0)
    & (df["media_leitos_uti_nao_sus"] >= 0)
]

# ==============================================================================
# FEATURE ENGINEERING
# ==============================================================================
print("A calcular métricas avançadas...")

df["taxa_obitos_100k"] = (df["obitos_evitaveis"] / df["populacao"]) * 100000
df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]

# Vetorização (muito mais rápido que usar df.apply)
df["pct_uti_sus"] = np.where(
    df["total_uti"] > 0, (df["media_leitos_uti_sus"] / df["total_uti"]) * 100, 0
)

df["pct_mortes_evitaveis"] = (df["obitos_evitaveis"] / df["obitos_hospitalares"]) * 100
df["dias_por_internacao"] = df["dias_internacao"] / df["internacoes"]
df["pib_per_capita_absoluto"] = (df["pib_milhares"] * 1000) / df["populacao"]

# Normalização de Infraestrutura (Parte 4 antecipada no Feature Engineering)
df["leitos_uti_sus_100k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 100000
df["leitos_uti_nao_sus_100k"] = (
    df["media_leitos_uti_nao_sus"] / df["populacao"]
) * 100000
if "media_equip_manut_vida_sus" in df.columns:
    df["equip_vida_sus_100k"] = (
        df["media_equip_manut_vida_sus"] / df["populacao"]
    ) * 100000


# ==============================================================================
# VISUALIZAÇÕES: PARTE I - MACROECONOMIA
# ==============================================================================
print("\nA gerar gráficos da Parte I...")

# 1. EVOLUÇÃO NACIONAL
evolucao = df.groupby("ano")[["obitos_evitaveis", "populacao"]].sum().reset_index()
evolucao["taxa_obitos_100k"] = (
    evolucao["obitos_evitaveis"] / evolucao["populacao"]
) * 100000
evolucao = evolucao.sort_values("ano")

fig_evolucao = px.line(
    evolucao,
    x="ano",
    y="taxa_obitos_100k",
    markers=True,
    title="<b>Evolução da Taxa de Óbitos Evitáveis no Brasil (por 100k hab.)</b>",
    labels={"ano": "Ano", "taxa_obitos_100k": "Taxa de Óbitos Evitáveis"},
    color_discrete_sequence=["darkred"],
)
fig_evolucao.update_traces(line=dict(width=3), marker=dict(size=10))
fig_evolucao.update_layout(xaxis_type="category", template="plotly_white")
fig_evolucao.show()

# 2. GINI vs ÓBITOS (Usando cor qualitativa para diferenciar anos)
fig_gini = px.scatter(
    df,
    x="indice_gini",
    y="taxa_obitos_100k",
    color="ano",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    title="<b>Desigualdade (Gini) vs Taxa de Óbitos Evitáveis</b>",
    labels={
        "indice_gini": "Índice de Gini",
        "taxa_obitos_100k": "Taxa de Óbitos Evitáveis (por 100k)",
    },
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig_gini.update_traces(
    marker=dict(size=10, opacity=0.8, line=dict(width=1, color="DarkSlateGrey"))
)
fig_gini.update_layout(template="plotly_white")
fig_gini.show()

# 3. PIB vs MORTALIDADE
fig_pib = px.scatter(
    df,
    x="pib_per_capita_absoluto",
    y="taxa_obitos_100k",
    size="idhm",
    color="ano",
    hover_name="nome_unidade_federativa",
    size_max=40,
    title="<b>PIB per capita vs Mortalidade (Tamanho da bolha = IDHM)</b>",
    labels={"pib_per_capita_absoluto": "PIB per Capita (R$)"},
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig_pib.update_traces(
    marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey"))
)
fig_pib.update_layout(template="plotly_white")
fig_pib.show()


# ==============================================================================
# VISUALIZAÇÕES: PARTE II - INFRAESTRUTURA E EFICIÊNCIA
# ==============================================================================
print("\nA gerar gráficos da Parte II...")

# 4. DISPARIDADE UTI SUS
fig_uti = px.scatter(
    df,
    x="pct_uti_sus",
    y="taxa_obitos_100k",
    color="ano",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    title="<b>Proporção de UTIs do SUS vs Mortalidade</b>",
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
fig_uti.update_traces(
    marker=dict(size=10, opacity=0.7, line=dict(width=1, color="DarkSlateGrey"))
)
fig_uti.update_layout(template="plotly_white")
fig_uti.show()

# 5. SATURAÇÃO HOSPITALAR
fig_internacao = px.scatter(
    df,
    x="dias_por_internacao",
    y="taxa_obitos_100k",
    color="ano",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    title="<b>Tempo Médio de Internação vs Mortalidade</b>",
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
fig_internacao.update_traces(
    marker=dict(size=10, opacity=0.7, line=dict(width=1, color="DarkSlateGrey"))
)
fig_internacao.update_layout(template="plotly_white")
fig_internacao.show()

# 6. EQUIPAMENTOS CRÍTICOS POR CATEGORIA
categorias_equip = {
    "media_equip_manut_vida_sus": "Manutenção da Vida (SUS)",
    "media_equip_diag_imagem_sus": "Diagnóstico por Imagem (SUS)",
    "media_equip_met_graficos_sus": "Métodos Gráficos (SUS)",
}

for col, nome in categorias_equip.items():
    if col in df.columns:
        fig_eq = px.scatter(
            df,
            x=col,
            y="taxa_obitos_100k",
            color="ano",
            hover_name="nome_unidade_federativa",
            trendline="ols",
            title=f"<b>Equipamentos de {nome} vs Mortalidade</b>",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        fig_eq.update_traces(
            marker=dict(size=10, opacity=0.7, line=dict(width=1, color="DarkSlateGrey"))
        )
        fig_eq.update_layout(template="plotly_white")
        fig_eq.show()

# 7. IDHM E IDHM-L
for col, nome in {"idhm": "IDHM (Geral)", "idhm_l": "IDHM (Longevidade)"}.items():
    if col in df.columns:
        fig_idh = px.scatter(
            df,
            x=col,
            y="pct_mortes_evitaveis",
            color="ano",
            hover_name="nome_unidade_federativa",
            trendline="ols",
            title=f"<b>{nome} vs Proporção de Mortes Evitáveis</b>",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_idh.update_traces(
            marker=dict(size=12, opacity=0.8, line=dict(width=1, color="black"))
        )
        fig_idh.update_layout(template="plotly_white")
        fig_idh.show()

# 8. LOCAIS E CID10
colunas_locais = [
    "obitos_hospital",
    "obitos_outro_estab_saude",
    "obitos_domicilio",
    "obitos_via_publica",
]
if all(col in df.columns for col in colunas_locais):
    df_locais = df[colunas_locais].sum().reset_index()
    df_locais.columns = ["Local", "Total"]
    df_locais["Local"] = df_locais["Local"].map(
        {
            "obitos_hospital": "Hospital",
            "obitos_outro_estab_saude": "Outro Estabelecimento",
            "obitos_domicilio": "Domicílio",
            "obitos_via_publica": "Via Pública",
        }
    )

    fig_locais = px.bar(
        df_locais.sort_values("Total"),
        x="Total",
        y="Local",
        orientation="h",
        title="<b>Mortalidade por Local de Ocorrência</b>",
        text_auto=".2s",
        color="Total",
        color_continuous_scale="Magma",
    )
    fig_locais.update_layout(template="plotly_white")
    fig_locais.show()

# CID 10 (Extração dinâmica segura)
colunas_base = list(df.columns)
colunas_cid10 = [
    col
    for col in df.columns
    if col not in colunas_numericas
    and col
    not in ["ano", "nome_unidade_federativa", "id_unidade_federativa", "indice_gini"]
    and pd.api.types.is_numeric_dtype(df[col])
]

if colunas_cid10:
    df_cid = df[colunas_cid10].sum().reset_index()
    df_cid.columns = ["Causa", "Total"]
    fig_cid = px.bar(
        df_cid.nlargest(10, "Total").sort_values("Total"),
        x="Total",
        y="Causa",
        orientation="h",
        title="<b>Top 10 Causas de Mortalidade (CID10)</b>",
        text_auto=".2s",
        color="Total",
        color_continuous_scale="Viridis",
    )
    fig_cid.update_layout(template="plotly_white", yaxis=dict(autorange="reversed"))
    fig_cid.show()


# ==============================================================================
# VISUALIZAÇÕES: PARTE III - REGIONAL E CORRELAÇÃO
# ==============================================================================
print("\nA gerar gráficos da Parte III...")

# 1. HEATMAP DE UF
pivot = df.pivot_table(
    index="nome_unidade_federativa",
    columns="ano",
    values="taxa_obitos_100k",
    aggfunc="mean",
)
fig_hm = px.imshow(
    pivot,
    title="<b>Heatmap: Evolução da Taxa de Óbitos por UF</b>",
    color_continuous_scale="YlOrRd",
    aspect="auto",
)
fig_hm.show()

# 2. TOP & BOTTOM 10
df_rank = df.groupby("nome_unidade_federativa")["taxa_obitos_100k"].mean().reset_index()

fig_top = px.bar(
    df_rank.nlargest(10, "taxa_obitos_100k"),
    x="taxa_obitos_100k",
    y="nome_unidade_federativa",
    orientation="h",
    title="<b>Top 10: Maiores Taxas</b>",
    color="taxa_obitos_100k",
    color_continuous_scale="Reds",
)
fig_top.update_layout(yaxis=dict(autorange="reversed"))
fig_top.show()

fig_bot = px.bar(
    df_rank.nsmallest(10, "taxa_obitos_100k"),
    x="taxa_obitos_100k",
    y="nome_unidade_federativa",
    orientation="h",
    title="<b>Bottom 10: Menores Taxas</b>",
    color="taxa_obitos_100k",
    color_continuous_scale="Greens",
)
fig_bot.update_layout(yaxis=dict(autorange="reversed"))
fig_bot.show()

# 3. BOXPLOT
fig_box = px.box(
    df,
    x="nome_unidade_federativa",
    y="taxa_obitos_100k",
    color="nome_unidade_federativa",
    title="<b>Distribuição da Mortalidade por Estado</b>",
)
fig_box.update_layout(showlegend=False, template="plotly_white")
fig_box.show()

# 4. PAIRPLOT E MATRIZ DE CORRELAÇÃO
cols_pair = ["taxa_obitos_100k", "pib_per_capita_absoluto", "pct_uti_sus"]
if "idhm_l" in df.columns:
    cols_pair.append("idhm_l")

fig_pair = px.scatter_matrix(
    df,
    dimensions=cols_pair,
    color="ano",
    title="<b>Pairplot de Variáveis Críticas</b>",
    opacity=0.6,
    color_discrete_sequence=px.colors.qualitative.Set1,
)
fig_pair.update_traces(diagonal_visible=False)
fig_pair.show()

fig_corr = px.imshow(
    df[cols_pair + ["indice_gini", "dias_por_internacao"]].corr(),
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="<b>Matriz de Correlação</b>",
)
fig_corr.show()


# ==============================================================================
# VISUALIZAÇÕES: PARTE IV - NORMALIZAÇÃO
# ==============================================================================
print("\nA gerar gráficos da Parte IV...")

df_infra = (
    df.groupby("nome_unidade_federativa")[
        ["leitos_uti_sus_100k", "leitos_uti_nao_sus_100k"]
    ]
    .mean()
    .reset_index()
)

fig_l_sus = px.bar(
    df_infra.sort_values("leitos_uti_sus_100k"),
    x="leitos_uti_sus_100k",
    y="nome_unidade_federativa",
    orientation="h",
    title="<b>Leitos UTI SUS por 100k hab.</b>",
    color="leitos_uti_sus_100k",
    color_continuous_scale="Teal",
)
fig_l_sus.update_layout(template="plotly_white")
fig_l_sus.show()

fig_l_nsus = px.bar(
    df_infra.sort_values("leitos_uti_nao_sus_100k"),
    x="leitos_uti_nao_sus_100k",
    y="nome_unidade_federativa",
    orientation="h",
    title="<b>Leitos UTI Não-SUS por 100k hab.</b>",
    color="leitos_uti_nao_sus_100k",
    color_continuous_scale="Oranges",
)
fig_l_nsus.update_layout(template="plotly_white")
fig_l_nsus.show()

if "equip_vida_sus_100k" in df.columns:
    df_eq = (
        df.groupby("nome_unidade_federativa")["equip_vida_sus_100k"]
        .mean()
        .reset_index()
        .sort_values("equip_vida_sus_100k")
    )
    fig_eq100 = px.bar(
        df_eq,
        x="equip_vida_sus_100k",
        y="nome_unidade_federativa",
        orientation="h",
        title="<b>Equipamentos de Vida SUS por 100k hab.</b>",
        color="equip_vida_sus_100k",
        color_continuous_scale="Purp",
    )
    fig_eq100.update_layout(template="plotly_white")
    fig_eq100.show()

fig_final = px.scatter(
    df,
    x="leitos_uti_sus_100k",
    y="taxa_obitos_100k",
    size="pib_per_capita_absoluto",
    color="pct_mortes_evitaveis",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    title="<b>Infraestrutura vs Mortalidade Evitável</b>",
    color_continuous_scale="RdBu_r",
)
fig_final.update_traces(
    marker=dict(opacity=0.8, line=dict(width=1, color="DarkSlateGrey"))
)
fig_final.update_layout(template="plotly_white")
fig_final.show()
