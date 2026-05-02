import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
sns.set(style='whitegrid')

print('\nCarregando base consolidada histórica...')
# Lendo a nova base mestre gerada pelo main.py
df = pd.read_csv('./datasets/base_consolidada_saude_historico.csv')

# Convertendo 'ano' para string/categoria para os gráficos não acharem que é um número matemático
df['ano'] = df['ano'].astype(str)

# =========================
# LIMPEZA E TRATAMENTO
# =========================
df = df[df['populacao'] > 1000]
df = df.dropna(subset=['taxa_mortalidade_evitavel', 'pib_per_capita', 'perc_cobertura_saude'])

# =========================
# 1. EVOLUÇÃO TEMPORAL (GRÁFICO NOVO)
# =========================
plt.figure(figsize=(10, 5))
# O pointplot vai desenhar uma linha do tempo mostrando a média nacional
sns.pointplot(data=df, x='ano', y='taxa_mortalidade_evitavel', color='red', markers="o")
plt.title('Evolução da Taxa Média de Mortalidade Evitável no Brasil (2018 a 2022)')
plt.ylabel('Taxa por 100k hab.')
plt.xlabel('Ano')
plt.show()

# =========================
# 2. DISTRIBUIÇÕES COMPARATIVAS
# =========================
plt.figure(figsize=(12, 5))

# Usamos kdeplot (curvas de densidade) com hue='ano' para ver os morrinhos se sobrepondo
plt.subplot(1, 2, 1)
sns.kdeplot(data=df, x='taxa_mortalidade_evitavel', hue='ano', fill=True, common_norm=False, palette='Set1')
plt.title('Distribuição da Mortalidade Evitável por Ano')

plt.subplot(1, 2, 2)
sns.kdeplot(data=df, x='pib_per_capita', hue='ano', fill=True, common_norm=False, palette='Set1')
plt.title('Distribuição do PIB per capita por Ano')
plt.xscale('log')

plt.tight_layout()
plt.show()

# =========================
# 3. RELAÇÕES PRINCIPAIS (COM EVOLUÇÃO)
# =========================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Trocamos o regplot por scatterplot com hue para ver como os municípios se moveram no gráfico
sns.scatterplot(x='pib_per_capita', y='taxa_mortalidade_evitavel', hue='ano', data=df, 
                alpha=0.4, palette='Set1', ax=ax1)
ax1.set_title('PIB per capita vs Mortalidade (Comparativo Anual)')
ax1.set_xscale('log')

sns.scatterplot(x='perc_cobertura_saude', y='taxa_mortalidade_evitavel', hue='ano', data=df, 
                alpha=0.4, palette='Set1', ax=ax2)
ax2.set_title('Cobertura de Saúde vs Mortalidade (Comparativo Anual)')

plt.tight_layout()
plt.show()

# =========================
# 4. ANÁLISE POR QUINTIL DE RENDA (NOVO MÉTODO)
# =========================
print('\nAnalisando impacto da renda na mortalidade...')

# Como temos anos diferentes, calculamos os quintis para CADA ANO separadamente
df['nivel_renda'] = df.groupby('ano')['pib_per_capita'].transform(
    lambda x: pd.qcut(x, 5, labels=['Muito Pobre', 'Pobre', 'Média', 'Rica', 'Muito Rica'])
)

plt.figure(figsize=(12, 6))
# Gráfico de barras agrupado por ano
sns.barplot(x='nivel_renda', y='taxa_mortalidade_evitavel', hue='ano', data=df, palette='viridis')
plt.title('Mortalidade Evitável por Nível de Renda (Comparativo 2018-2022)')
plt.ylabel('Taxa por 100k hab.')
plt.show()

print('\nEDA Temporal finalizado! A história agora está completa.')