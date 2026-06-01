import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIGURAÇÃO
# =========================
sns.set_theme(style="whitegrid", palette="muted")

print("\nCarregando Tabela Mestra...")

df = pd.read_csv("./datasets/dataset_completo_consolidado.csv")

# =========================
# LIMPEZA
# =========================

df["ano"] = df["ano"].astype(str)

df["indice_gini"] = (
    df["indice_gini"].astype(str).str.replace(",", ".", regex=False).astype(float)
)

colunas_numericas = [
    "obitos_evitaveis",
    "renda_per_capita",
    "media_leitos_uti_sus",
    "media_equip_manut_vida_sus",
]

for col in colunas_numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

df = df[df["obitos_evitaveis"] > 0]

# =========================
# 1. EVOLUÇÃO DOS ÓBITOS EVITÁVEIS
# =========================

print("\nGerando evolução temporal...")

evolucao = df.groupby("ano")["obitos_evitaveis"].sum().reset_index()

plt.figure(figsize=(10, 5))

sns.lineplot(
    data=evolucao,
    x="ano",
    y="obitos_evitaveis",
    marker="o",
    color="darkred",
    linewidth=2,
)

plt.title(
    "Evolução dos Óbitos Evitáveis no Brasil",
    fontsize=14,
    weight="bold",
)

plt.ylabel("Óbitos Evitáveis")
plt.xlabel("Ano")

plt.tight_layout()
plt.show()

# =========================
# 2. DESIGUALDADE VS ÓBITOS EVITÁVEIS
# =========================

print("\nGerando gráfico de Desigualdade vs Mortalidade...")

plt.figure(figsize=(12, 7))

sns.scatterplot(
    data=df,
    x="indice_gini",
    y="obitos_evitaveis",
    hue="ano",
    palette="viridis",
    s=120,
    alpha=0.8,
    edgecolor="white",
)

sns.regplot(
    data=df,
    x="indice_gini",
    y="obitos_evitaveis",
    scatter=False,
    color="gray",
    line_kws={
        "linestyle": "--",
        "alpha": 0.6,
    },
)

plt.title(
    "Desigualdade e Óbitos Evitáveis",
    fontsize=15,
    weight="bold",
)

plt.xlabel("Índice de Gini")
plt.ylabel("Óbitos Evitáveis")

plt.legend(
    title="Ano",
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)

plt.grid(True, linestyle=":", alpha=0.7)

plt.tight_layout()
plt.show()

# =========================
# 3. INFRAESTRUTURA HOSPITALAR VS MORTALIDADE
# =========================

print("\nGerando gráfico de UTI vs Mortalidade...")

plt.figure(figsize=(10, 6))

sns.regplot(
    data=df,
    x="media_leitos_uti_sus",
    y="obitos_evitaveis",
    scatter_kws={"alpha": 0.6, "color": "gray"},
    line_kws={"color": "red"},
)

plt.title(
    "Leitos de UTI SUS e Óbitos Evitáveis",
    fontsize=14,
    weight="bold",
)

plt.xlabel("Média de Leitos UTI SUS")
plt.ylabel("Óbitos Evitáveis")

plt.tight_layout()
plt.show()

# =========================
# 4. EQUIPAMENTOS CRÍTICOS VS MORTALIDADE
# =========================

print("\nGerando gráfico de Equipamentos vs Mortalidade...")

plt.figure(figsize=(10, 6))

sns.regplot(
    data=df,
    x="media_equip_manut_vida_sus",
    y="obitos_evitaveis",
    scatter_kws={"alpha": 0.6, "color": "gray"},
    line_kws={"color": "darkred"},
)

plt.title(
    "Equipamentos de Manutenção da Vida e Óbitos Evitáveis",
    fontsize=14,
    weight="bold",
)

plt.xlabel("Equipamentos SUS de Manutenção da Vida")
plt.ylabel("Óbitos Evitáveis")

plt.tight_layout()
plt.show()

# =========================
# 5. QUARTIS DE RENDA
# =========================

print("\nGerando análise por renda...")

df["nivel_renda"] = pd.qcut(
    df["renda_per_capita"], q=4, labels=["Baixa", "Média-Baixa", "Média-Alta", "Alta"]
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=df,
    x="nivel_renda",
    y="obitos_evitaveis",
    hue="ano",
    palette="Reds",
)

plt.title(
    "Renda Per Capita e Óbitos Evitáveis",
    fontsize=14,
    weight="bold",
)

plt.xlabel("Quartis de Renda")
plt.ylabel("Óbitos Evitáveis")

plt.legend(title="Ano", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()

print("\nAnálise Exploratória Concluída!")
