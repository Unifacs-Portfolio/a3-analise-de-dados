import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
sns.set(style='whitegrid')

print('\nCarregando base consolidada V2...')
# Lendo a nova base gerada pelo main.py
df = pd.read_csv('./datasets/base_consolidada_saude.csv')

# =========================
# LIMPEZA E TRATAMENTO
# =========================
# Filtramos municípios com dados consistentes
df = df[df['populacao'] > 1000] # Foco em cidades com representatividade
df = df.dropna(subset=['taxa_mortalidade_evitavel', 'pib_per_capita', 'perc_cobertura_saude'])

# =========================
# ESTATÍSTICAS DESCRITIVAS
# =========================
print('\n=== ESTATÍSTICAS DESCRITIVAS ===')
cols = [
    'pib_per_capita',
    'taxa_mortalidade_evitavel',
    'perc_cobertura_saude'
]
print(df[cols].describe())

# =========================
# DISTRIBUIÇÕES
# =========================
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(df['taxa_mortalidade_evitavel'], kde=True, color='red')
plt.title('Distribuição da Mortalidade Evitável')

plt.subplot(1, 2, 2)
sns.histplot(df['pib_per_capita'], kde=True, color='green')
plt.title('Distribuição do PIB per capita')
plt.xscale('log') # PIB costuma ter muita variação (escala log ajuda)

plt.tight_layout()
plt.show()

# =========================
# CORRELAÇÃO (O CORAÇÃO DO PROJETO)
# =========================
print('\n=== MATRIZ DE CORRELAÇÃO ===')
corr = df[cols + ['populacao']].corr()
print(corr)

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='RdYlGn_r', center=0)
plt.title('Mapa de Correlação: Renda vs Saúde vs Mortalidade')
plt.show()

# =========================
# RELAÇÕES PRINCIPAIS
# =========================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Relação 1: Renda vs Mortalidade
sns.regplot(x='pib_per_capita', y='taxa_mortalidade_evitavel', data=df, 
            scatter_kws={'alpha':0.3}, line_kws={'color':'red'}, ax=ax1)
ax1.set_title('PIB per capita vs Mortalidade Evitável')
ax1.set_xscale('log')

# Relação 2: Cobertura vs Mortalidade
sns.regplot(x='perc_cobertura_saude', y='taxa_mortalidade_evitavel', data=df, 
            scatter_kws={'alpha':0.3}, line_kws={'color':'blue'}, ax=ax2)
ax2.set_title('Cobertura de Saúde vs Mortalidade Evitável')

plt.tight_layout()
plt.show()

# =========================
# ANÁLISE POR QUINTIL DE RENDA
# =========================
print('\nAnalisando impacto da renda na mortalidade...')

df['nivel_renda'] = pd.qcut(
    df['pib_per_capita'], 
    5, 
    labels=['Muito Pobre', 'Pobre', 'Média', 'Rica', 'Muito Rica']
)

plt.figure(figsize=(10, 6))
sns.barplot(x='nivel_renda', y='taxa_mortalidade_evitavel', data=df, palette='viridis')
plt.title('Média de Mortalidade Evitável por Nível de Renda')
plt.ylabel('Taxa por 100k hab.')
plt.show()

# =========================
# RANKING DE VULNERABILIDADE
# =========================
# Municípios com Baixa Renda AND Baixa Cobertura AND Alta Mortalidade
print('\n=== TOP 10 MUNICÍPIOS MAIS VULNERÁVEIS ===')
vulneraveis = df[
    (df['pib_per_capita'] < df['pib_per_capita'].median()) & 
    (df['perc_cobertura_saude'] < df['perc_cobertura_saude'].median())
].sort_values(by='taxa_mortalidade_evitavel', ascending=False)

print(vulneraveis[['nome_municipio', 'pib_per_capita', 'taxa_mortalidade_evitavel']].head(10))

print('\nEDA Fase 2 finalizado. Agora os dados contam a história real!')