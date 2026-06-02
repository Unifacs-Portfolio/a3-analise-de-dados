import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ==============================================================================
# CONFIGURAÇÃO VISUAL
# ==============================================================================
sns.set_theme(style="whitegrid", palette="muted")

print("\nA carregar a Tabela Mestra...")
df = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

# ==============================================================================
# LIMPEZA E PREPARAÇÃO DOS DADOS
# ==============================================================================
df["ano"] = df["ano"].astype(str)

# Corrigir o formato do Gini (tratamento de strings com vírgula)
df["indice_gini"] = (
    df["indice_gini"].astype(str).str.replace(",", ".", regex=False).astype(float)
)

# Colunas necessárias para todas as análises
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
]

for col in colunas_numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remoção de valores nulos apenas nas colunas essenciais
colunas_analise = colunas_numericas + ["indice_gini", "ano", "nome_unidade_federativa"]
df = df.dropna(subset=colunas_analise)

# Filtrar registos inválidos para evitar divisões por zero ou erros matemáticos
df = df[
    (df["obitos_evitaveis"] > 0)
    & (df["populacao"] > 0)
    & (df["obitos_hospitalares"] > 0)
    & (df["internacoes"] > 0)
    & (df["media_leitos_uti_sus"] >= 0)
    & (df["media_leitos_uti_nao_sus"] >= 0)
]

# ==============================================================================
# CRIAÇÃO DE NOVAS MÉTRICAS (FEATURE ENGINEERING)
# ==============================================================================
print("A calcular métricas avançadas...")

# 1. Taxa Padronizada de Óbitos (Base da análise)
df["taxa_obitos_100k"] = (df["obitos_evitaveis"] / df["populacao"]) * 100000

# 2. Disparidade Público-Privada (% de UTIs pertencentes ao SUS)
df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]
df["pct_uti_sus"] = df.apply(
    lambda r: (
        (r["media_leitos_uti_sus"] / r["total_uti"]) * 100 if r["total_uti"] > 0 else 0
    ),
    axis=1,
)

# 3. Taxa de Evitabilidade (% de óbitos hospitalares que eram evitáveis)
df["pct_mortes_evitaveis"] = (df["obitos_evitaveis"] / df["obitos_hospitalares"]) * 100

# 4. Tempo Médio de Internação (Indicador de carga hospitalar)
df["dias_por_internacao"] = df["dias_internacao"] / df["internacoes"]

# 5. PIB per capita Absoluto (Ajuste da escala original que está em milhares)
df["pib_per_capita_absoluto"] = (df["pib_milhares"] * 1000) / df["populacao"]


# ==============================================================================
# PARTE I: MACROECONOMIA E TENDÊNCIAS GERAIS
# ==============================================================================
print("\nA gerar gráficos da Parte I...")

# 1. EVOLUÇÃO DOS ÓBITOS EVITÁVEIS (TAXA NACIONAL CORRIGIDA)
evolucao = df.groupby("ano")[["obitos_evitaveis", "populacao"]].sum().reset_index()
evolucao["taxa_obitos_100k"] = (
    evolucao["obitos_evitaveis"] / evolucao["populacao"]
) * 100000

plt.figure(figsize=(10, 5))
sns.lineplot(
    data=evolucao,
    x="ano",
    y="taxa_obitos_100k",
    marker="o",
    color="darkred",
    linewidth=2,
)
plt.title(
    "Evolução da Taxa de Óbitos Evitáveis no Brasil (por 100k hab.)",
    fontsize=14,
    weight="bold",
)
plt.ylabel("Taxa de Óbitos Evitáveis")
plt.xlabel("Ano")
plt.tight_layout()
plt.show()

# 2. DESIGUALDADE (GINI) VS ÓBITOS EVITÁVEIS
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=df,
    x="indice_gini",
    y="taxa_obitos_100k",
    hue="ano",
    palette="viridis",
    s=120,
    alpha=0.8,
    edgecolor="white",
)
sns.regplot(
    data=df,
    x="indice_gini",
    y="taxa_obitos_100k",
    scatter=False,
    color="gray",
    line_kws={"linestyle": "--", "alpha": 0.6},
)
plt.title(
    "Desigualdade e Taxa de Óbitos Evitáveis",
    fontsize=15,
    weight="bold",
)
plt.xlabel("Índice de Gini")
plt.ylabel("Taxa de Óbitos Evitáveis (por 100k)")
plt.legend(title="Ano", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True, linestyle=":", alpha=0.7)
plt.tight_layout()
plt.show()

# 3. RIQUEZA x DESENVOLVIMENTO (BUBBLE CHART)
plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=df,
    x="pib_per_capita_absoluto",
    y="taxa_obitos_100k",
    size="idhm",
    sizes=(50, 500),
    hue="ano",
    palette="viridis",
    alpha=0.7,
    edgecolor="black",
)
plt.title(
    "PIB per capita vs Mortalidade (Tamanho da bolha = IDHM)",
    fontsize=14,
    weight="bold",
)
plt.xlabel("PIB per Capita (R$)")
plt.ylabel("Taxa de Óbitos Evitáveis (por 100k)")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()


# ==============================================================================
# PARTE II: INFRAESTRUTURA E EFICIÊNCIA HOSPITALAR
# ==============================================================================
print("A gerar gráficos da Parte II...")

# 4. DISPARIDADE PÚBLICO-PRIVADA (% UTI SUS)
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="pct_uti_sus",
    y="taxa_obitos_100k",
    scatter_kws={"alpha": 0.6, "color": "teal"},
    line_kws={"color": "darkred"},
)
plt.title("Proporção de UTIs do SUS vs Mortalidade", fontsize=14, weight="bold")
plt.xlabel("Proporção de Leitos de UTI do SUS (%)")
plt.ylabel("Taxa de Óbitos Evitáveis (por 100k)")
plt.tight_layout()
plt.show()

# 5. SATURAÇÃO HOSPITALAR (TEMPO DE INTERNAÇÃO) VS MORTALIDADE
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="dias_por_internacao",
    y="taxa_obitos_100k",
    scatter_kws={"alpha": 0.6, "color": "purple"},
    line_kws={"color": "orange"},
)
plt.title("Tempo Médio de Internação vs Mortalidade", fontsize=14, weight="bold")
plt.xlabel("Dias Médios por Internação")
plt.ylabel("Taxa de Óbitos Evitáveis (por 100k)")
plt.tight_layout()
plt.show()

# 6. EQUIPAMENTOS CRÍTICOS VS MORTALIDADE
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="media_equip_manut_vida_sus",
    y="taxa_obitos_100k",
    scatter_kws={"alpha": 0.6, "color": "gray"},
    line_kws={"color": "darkred"},
)
plt.title(
    "Equipamentos de Manutenção da Vida SUS e Mortalidade",
    fontsize=14,
    weight="bold",
)
plt.xlabel("Equipamentos SUS de Manutenção da Vida")
plt.ylabel("Taxa de Óbitos Evitáveis (por 100k)")
plt.tight_layout()
plt.show()

# 7. IDHM VS TAXA DE EVITABILIDADE (% DE MORTES EVITÁVEIS)
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="idhm",
    y="pct_mortes_evitaveis",
    hue="ano",
    palette="magma",
    s=100,
    alpha=0.8,
)
sns.regplot(
    data=df,
    x="idhm",
    y="pct_mortes_evitaveis",
    scatter=False,
    color="gray",
    line_kws={
        "linestyle": "--",
        "alpha": 0.7,
        "linewidth": 2,
    },
)
plt.title("IDHM vs Proporção de Mortes Evitáveis", fontsize=14, weight="bold")
plt.xlabel("IDHM (Índice de Desenvolvimento Humano)")
plt.ylabel("% de Óbitos que eram Evitáveis")
plt.legend(title="Ano", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True, linestyle=":", alpha=0.7)
plt.tight_layout()
plt.show()


# ==============================================================================
# PARTE III: VISÃO REGIONAL DISTRIBUÍDA
# ==============================================================================
print("A gerar Mapa de Calor (Heatmap)...")

# 8. HEATMAP DE EVOLUÇÃO REGIONAL POR UF
pivot_obitos = df.pivot_table(
    index="nome_unidade_federativa",
    columns="ano",
    values="taxa_obitos_100k",
    aggfunc="mean",
)

plt.figure(figsize=(12, 10))
sns.heatmap(pivot_obitos, cmap="YlOrRd", linewidths=0.5, annot=True, fmt=".1f")
plt.title(
    "Mapa de Calor: Taxa de Óbitos Evitáveis (por 100k hab.) por Unidade Federativa",
    fontsize=14,
    weight="bold",
)
plt.xlabel("Ano")
plt.ylabel("Unidade Federativa")
plt.tight_layout()
plt.show()

# 9. MATRIZ DE CORRELAÇÃO GLOBAL (Métricas Socioeconômicas vs Saúde)
print("A gerar o Mapa de Correlação Linear...")

colunas_corr = [
    "taxa_obitos_100k",
    "indice_gini",
    "idhm",
    "pib_per_capita_absoluto",
    "pct_uti_sus",
    "pct_mortes_evitaveis",
    "dias_por_internacao",
    "media_equip_manut_vida_sus",
]

matriz_correlacao = df[colunas_corr].corr()

nomes_amigaveis = {
    "taxa_obitos_100k": "Taxa Óbitos (100k)",
    "indice_gini": "Índice de Gini",
    "idhm": "IDHM",
    "pib_per_capita_absoluto": "PIB per Capita",
    "pct_uti_sus": "% UTI SUS",
    "pct_mortes_evitaveis": "% Mortes Evitáveis",
    "dias_por_internacao": "Dias por Internação",
    "media_equip_manut_vida_sus": "Equipamentos SUS",
}

matriz_correlacao = matriz_correlacao.rename(
    index=nomes_amigaveis, columns=nomes_amigaveis
)

plt.figure(figsize=(11, 9))
sns.heatmap(
    matriz_correlacao,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    annot=True,
    fmt=".2f",
    linewidths=0.5,
    square=True,
)
plt.title(
    "Matriz de Correlação entre Indicadores Sócioeconômicos e de Saúde",
    fontsize=14,
    weight="bold",
    pad=20,
)
plt.tight_layout()
plt.show()


# ==============================================================================
# PARTE IV: ANÁLISE VISUAL DE INFRAESTRUTURA (LEITOS E EQUIPAMENTOS CRÍTICOS)
# ==============================================================================
print("A gerar gráficos estruturais de Infraestrutura...")

# Agrupamento e preparação de dados por UF ordenados pela taxa de óbitos
df_uf_infra = (
    df.groupby("nome_unidade_federativa")[
        [
            "taxa_obitos_100k",
            "media_leitos_uti_sus",
            "media_leitos_uti_nao_sus",
            "media_equip_manut_vida_sus",
        ]
    ]
    .mean()
    .sort_values(by="taxa_obitos_100k", ascending=True)
    .reset_index()
)

# 10. COMPARAÇÃO REGIONAL: DISTRIBUIÇÃO DE LEITOS UTI (SUS VS NÃO-SUS)
df_melted_leitos = df_uf_infra.melt(
    id_vars=["nome_unidade_federativa", "taxa_obitos_100k"],
    value_vars=["media_leitos_uti_sus", "media_leitos_uti_nao_sus"],
    var_name="Tipo de Leito",
    value_name="Quantidade Média de Leitos",
)

df_melted_leitos["Tipo de Leito"] = df_melted_leitos["Tipo de Leito"].map(
    {
        "media_leitos_uti_sus": "Leitos UTI SUS",
        "media_leitos_uti_nao_sus": "Leitos UTI Não-SUS",
    }
)

plt.figure(figsize=(14, 10))
sns.barplot(
    data=df_melted_leitos,
    y="nome_unidade_federativa",
    x="Quantidade Média de Leitos",
    hue="Tipo de Leito",
    palette=["#008080", "#E67E22"],  # Teal para SUS, Laranja para Não-SUS
    edgecolor="black",
    alpha=0.85,
)
plt.title(
    "Disponibilidade Média de Leitos de UTI (SUS vs Não-SUS) por Unidade Federativa\n"
    "(Ordenado de forma crescente pela Taxa de Óbitos)",
    fontsize=14,
    weight="bold",
    pad=15,
)
plt.ylabel("Unidade Federativa")
plt.xlabel("Capacidade Média de Leitos Hospitalares (Unidades)")
plt.legend(title="Segmento Hospitalar", loc="lower right")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.show()


# 11. PANORAMA TEMPORAL: EXPANSÃO DE INFRAESTRUTURA VS TAXA DE ÓBITOS EVITÁVEIS
evolucao_infra = (
    df.groupby("ano")[
        [
            "taxa_obitos_100k",
            "media_leitos_uti_sus",
            "media_leitos_uti_nao_sus",
            "media_equip_manut_vida_sus",
        ]
    ]
    .mean()
    .reset_index()
)

fig, ax1 = plt.subplots(figsize=(13, 6))

# Eixo da Esquerda (ax1) - Infraestrutura
ln1 = ax1.plot(
    evolucao_infra["ano"],
    evolucao_infra["media_leitos_uti_sus"],
    marker="s",
    color="#008080",
    linewidth=2.5,
    label="Média Leitos UTI SUS",
)
ln2 = ax1.plot(
    evolucao_infra["ano"],
    evolucao_infra["media_leitos_uti_nao_sus"],
    marker="^",
    color="#E67E22",
    linewidth=2.5,
    label="Média Leitos UTI Não-SUS",
)
ln3 = ax1.plot(
    evolucao_infra["ano"],
    evolucao_infra["media_equip_manut_vida_sus"],
    marker="x",
    color="#7F8C8D",
    linestyle=":",
    linewidth=2,
    label="Média Equipamentos SUS",
)

ax1.set_xlabel("Ano", fontsize=11)
ax1.set_ylabel(
    "Volume de Infraestrutura Hospitalar (Média por Estado)",
    color="black",
    fontsize=11,
)
ax1.tick_params(axis="y", labelcolor="black")

# Garante o grid apenas para o eixo principal
ax1.grid(True, linestyle=":", alpha=0.5)

# Eixo da Direita (ax2) - Mortalidade
ax2 = ax1.twinx()
ln4 = ax2.plot(
    evolucao_infra["ano"],
    evolucao_infra["taxa_obitos_100k"],
    marker="o",
    color="darkred",
    linewidth=3,
    linestyle="-.",
    label="Taxa Óbitos/100k",
)
ax2.set_ylabel("Taxa de Óbitos Evitáveis (por 100k hab.)", color="darkred", fontsize=11)
ax2.tick_params(axis="y", labelcolor="darkred")

# CORREÇÃO DO ERRO: Desativa as linhas de grade do segundo eixo Y
ax2.grid(False)

# CORREÇÃO DA LEGENDA: Combina todas as linhas em uma única caixa de legenda
reuniao_linhas = ln1 + ln2 + ln3 + ln4
rotulos = [l.get_label() for l in reuniao_linhas]
ax1.legend(reuniao_linhas, rotulos, loc="upper left", frameon=True)

plt.title(
    "Evolução Histórica Nacional: Expansão de Infraestrutura vs Redução de Mortalidade",
    fontsize=14,
    weight="bold",
    pad=15,
)
fig.tight_layout()
plt.show()

print("\nAnálise Exploratória Completa Finalizada!")
