import pandas as pd
import numpy as np
import plotly.express as px

# ==============================================================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==============================================================================
print("\n[1/4] A carregar a Tabela Mestra Consolidada...")
df = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

df["ano"] = df["ano"].astype(str)

# Corrigir o formato do Gini, IDHM e Renda (tratamento de strings com vírgula)
for col in ["indice_gini", "idhm", "renda_per_capita"]:
    if col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(",", ".", regex=False).astype(float)

# Colunas numéricas esperadas
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

# Limpeza de nulos e filtro
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

# ORDENAÇÃO OBRIGATÓRIA PARA ANIMAÇÕES FLUIDAS
df = df.sort_values(by=["ano", "nome_unidade_federativa"])


# ==============================================================================
# 2. FEATURE ENGINEERING E LIMITES DOS EIXOS
# ==============================================================================
print("[2/4] A calcular métricas avançadas e mapear regiões...")

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

# Taxas
df["leitos_uti_sus_100k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 100000
df["leitos_uti_sus_1k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 1000
df["leitos_enf_sus_1k"] = (df["media_leitos_enf_sus"] / df["populacao"]) * 1000
df["mortalidade_evitavel_100k"] = (df["obitos_evitaveis"] / df["populacao"]) * 100000
df["internacoes_100k"] = (df["internacoes"] / df["populacao"]) * 100000

df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]
df["pct_uti_sus"] = np.where(
    df["total_uti"] > 0, (df["media_leitos_uti_sus"] / df["total_uti"]) * 100, 0
)

# --- CÁLCULO DOS LIMITES GLOBAIS PARA FIXAR OS EIXOS DAS ANIMAÇÕES ---
max_mort = df["mortalidade_evitavel_100k"].max() * 1.1
max_uti_1k = df["leitos_uti_sus_1k"].max() * 1.1
max_uti_100k = df["leitos_uti_sus_100k"].max() * 1.1
max_int = df["internacoes_100k"].max() * 1.1
max_enf = df["leitos_enf_sus_1k"].max() * 1.1
min_idhm = df["idhm"].min() * 0.95
max_idhm = df["idhm"].max() * 1.05


# ==============================================================================
# 3. GRÁFICOS ANIMADOS - STORYTELLING CLÍNICO
# ==============================================================================
print("[3/4] A gerar Gráficos Animados Clínicos (Clique no Play no navegador)...")

# Gráfico 1: UTI vs Mortalidade (Alocação Reativa)
fig1 = px.scatter(
    df,
    x="leitos_uti_sus_1k",
    y="mortalidade_evitavel_100k",
    color="regiao_ibge",
    animation_frame="ano",
    animation_group="nome_unidade_federativa",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    range_x=[0, max_uti_1k],
    range_y=[0, max_mort],
    title="<b>[ANIMADO] Alocação Reativa: Maior mortalidade induz mais UTIs</b>",
    labels={
        "leitos_uti_sus_1k": "Leitos UTI SUS (por 1k hab.)",
        "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
        "regiao_ibge": "Região",
    },
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig1.update_layout(template="plotly_white")
fig1.show()

# Gráfico 2: Internações vs Mortalidade (Fator de Proteção)
fig2 = px.scatter(
    df,
    x="internacoes_100k",
    y="mortalidade_evitavel_100k",
    color="regiao_ibge",
    animation_frame="ano",
    animation_group="nome_unidade_federativa",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    range_x=[0, max_int],
    range_y=[0, max_mort],
    title="<b>[ANIMADO] Acesso Hospitalar Estruturado previne Mortes Agudas</b>",
    labels={
        "internacoes_100k": "Taxa de Internações (por 100k)",
        "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
    },
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
fig2.update_layout(template="plotly_white")
fig2.show()

# Gráfico 3: Enfermaria vs Mortalidade (Baixa Complexidade)
fig3 = px.scatter(
    df,
    x="leitos_enf_sus_1k",
    y="mortalidade_evitavel_100k",
    animation_frame="ano",
    animation_group="nome_unidade_federativa",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    range_x=[0, max_enf],
    range_y=[0, max_mort],
    title="<b>[ANIMADO] A Necessidade de Especialização (Sem correlação com Enfermaria)</b>",
    labels={
        "leitos_enf_sus_1k": "Enfermaria SUS (por 1k hab.)",
        "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
    },
    color_discrete_sequence=["#7F8C8D"],
)
fig3.update_layout(template="plotly_white")
fig3.show()


# ==============================================================================
# 4. GRÁFICOS ANIMADOS - MITIGAÇÃO DE VIÉS
# ==============================================================================
print("[4/4] A gerar Gráficos Animados de Mitigação de Viés...")

# Gráfico 4: O Paradoxo Reativo por Tamanho de População
fig_paradoxo = px.scatter(
    df,
    x="leitos_uti_sus_100k",
    y="mortalidade_evitavel_100k",
    color="regiao_ibge",
    size="populacao",
    animation_frame="ano",
    animation_group="nome_unidade_federativa",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    range_x=[0, max_uti_100k],
    range_y=[0, max_mort],
    size_max=50,
    title="<b>[ANIMADO] O Paradoxo Reativo: Blocos regionais sofrendo cargas diferentes</b>",
    labels={
        "leitos_uti_sus_100k": "Leitos UTI SUS (por 100k)",
        "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)",
    },
    color_discrete_sequence=px.colors.qualitative.Prism,
)
fig_paradoxo.update_layout(template="plotly_white")
fig_paradoxo.show()

# Gráfico 5: O Viés de Confundimento (IDHM)
fig_confundimento = px.scatter(
    df,
    x="idhm",
    y="mortalidade_evitavel_100k",
    color="regiao_ibge",
    size="leitos_uti_sus_100k",
    animation_frame="ano",
    animation_group="nome_unidade_federativa",
    hover_name="nome_unidade_federativa",
    trendline="ols",
    range_x=[min_idhm, max_idhm],
    range_y=[0, max_mort],
    size_max=40,
    title="<b>[ANIMADO] Viés Socioeconômico: Mortalidade vs Desenvolvimento (Tamanho = UTIs)</b>",
    labels={"idhm": "IDHM", "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k)"},
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig_confundimento.update_layout(template="plotly_white")
fig_confundimento.show()

# Gráfico 6: Corrida de Barras Animada (Mix Público-Privado)
# Ordenamos também por região para as barras ficarem agrupadas logicamente durante a animação
df_mix = df.sort_values(by=["ano", "regiao_ibge", "pct_uti_sus"])
fig_mix = px.bar(
    df_mix,
    x="pct_uti_sus",
    y="nome_unidade_federativa",
    color="regiao_ibge",
    animation_frame="ano",
    animation_group="nome_unidade_federativa",
    orientation="h",
    range_x=[0, 100],  # Fixo de 0 a 100%
    title="<b>[ANIMADO] Assimetria do Mix Público-Privado (Corrida da Dependência do SUS)</b>",
    labels={
        "pct_uti_sus": "UTIs pertencentes ao SUS (%)",
        "nome_unidade_federativa": "Estado",
    },
    color_discrete_sequence=px.colors.qualitative.Vivid,
)
fig_mix.add_vline(x=50, line_dash="dash", line_color="black")
fig_mix.update_layout(
    template="plotly_white", yaxis=dict(autorange="reversed"), height=750
)
fig_mix.show()

print("\nConcluído! Todos os gráficos são agora animações temporais interativas.")
