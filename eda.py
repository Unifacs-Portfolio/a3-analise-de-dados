import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIGURAÇÃO
# =========================
sns.set_theme(style="whitegrid", palette="muted")

print("\nCarregando Tabela Mestra...")
df = pd.read_csv("./datasets/base_consolidada_saude_historico.csv")
df["ano"] = df["ano"].astype(str)

# Limpeza de outliers nulos ou zerados
df = df[df["taxa_mortalidade_evitavel_100k"] > 0]

# =========================
# 1. A LINHA DO TEMPO (A Prova do Represamento)
# =========================
plt.figure(figsize=(10, 5))
sns.lineplot(
    data=df,
    x="ano",
    y="taxa_mortalidade_evitavel_100k",
    marker="o",
    color="darkred",
    errorbar=None,
    linewidth=2,
)
plt.title(
    "A Fatura da Pandemia: Evolução da Mortalidade Evitável (Brasil)",
    fontsize=14,
    weight="bold",
)
plt.ylabel("Óbitos Evitáveis (por 100 mil hab.)")
plt.xlabel("Ano")
plt.tight_layout()
plt.show()

# =========================
# 2. A CAUSA RAIZ: DESIGUALDADE vs PRESSÃO NO POSTO DE SAÚDE
# =========================
print("Gerando gráfico de Desigualdade vs ICSAP...")

# O HACK DA VÍRGULA: Força o Índice de Gini a virar número matemático contínuo
df["indice_gini"] = df["indice_gini"].astype(str).str.replace(",", ".").astype(float)
df["taxa_icsap_100k"] = df["taxa_icsap_100k"].astype(float)

# Cria a figura um pouco mais larga para dar respiro aos dados
plt.figure(figsize=(12, 7))

# Cria o gráfico de dispersão com bolhas maiores e bordas brancas para dar contraste
sns.scatterplot(
    data=df,
    x="indice_gini",
    y="taxa_icsap_100k",
    hue="ano",
    palette="viridis",
    s=120,
    alpha=0.8,
    edgecolor="white",
)

# Adiciona uma linha de tendência pontilhada (Regressão Linear) para provar a correlação
sns.regplot(
    data=df,
    x="indice_gini",
    y="taxa_icsap_100k",
    scatter=False,
    color="gray",
    line_kws={"linestyle": "--", "alpha": 0.6},
)

plt.title(
    "A Raiz do Problema: Desigualdade (Gini) vs Pressão na Atenção Primária (ICSAP)",
    fontsize=15,
    weight="bold",
)
plt.xlabel("Índice de Gini (Maior = Mais Desigualdade)", fontsize=12)
plt.ylabel("Taxa de Internações Evitáveis (ICSAP por 100k hab.)", fontsize=12)

# Ajusta as legendas e a grade
plt.legend(
    title="Ano",
    fontsize=11,
    title_fontsize=12,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)
plt.grid(True, linestyle=":", alpha=0.7)

plt.tight_layout()
plt.show()

# =========================
# 3. O COLAPSO HOSPITALAR: GARGALO vs MORTALIDADE
# =========================
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="tempo_medio_permanencia",
    y="taxa_mortalidade_evitavel_100k",
    scatter_kws={"alpha": 0.5, "color": "gray"},
    line_kws={"color": "red"},
)
plt.title(
    "O Gargalo: Como a Saturação de Leitos Reflete na Mortalidade",
    fontsize=14,
    weight="bold",
)
plt.xlabel("Tempo Médio de Permanência (Dias travando o Leito)")
plt.ylabel("Taxa de Mortalidade Evitável")
plt.tight_layout()
plt.show()

# =========================
# 4. ANÁLISE DE QUADRANTES (O GRÁFICO DEFINITIVO DA APRESENTAÇÃO)
# =========================
print("\nGerando Quadrantes de Vulnerabilidade...")

# Divide os Estados em grupos de Poder de Compra
df["nivel_renda"] = pd.qcut(
    df["renda_media"],
    q=4,
    labels=["Baixa Renda", "Renda Média-Baixa", "Renda Média-Alta", "Alta Renda"],
)

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df,
    x="nivel_renda",
    y="taxa_mortalidade_evitavel_100k",
    hue="ano",
    palette="Reds",
)
plt.title(
    "Sobrecarga do SUS: A Mortalidade é Menor Onde a População Pode Pagar Rede Privada?",
    fontsize=14,
    weight="bold",
)
plt.xlabel("Quartis de Renda Média Domiciliar")
plt.ylabel("Mortalidade Evitável por 100k hab.")
plt.legend(title="Ano", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

# print('\nAnálise Exploratória Concluída! Gráficos prontos para a apresentação.')
