import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# CONFIG
# =========================
sns.set(style='whitegrid')

print('\nCarregando base...')
df = pd.read_csv('./datasets/base_consolidade_saude.csv')

# =========================
# VISÃO INICIAL
# =========================
print('\n=== HEAD ===')
print(df.head())

print('\n=== INFO ===')
print(df.info())

print('\n=== VALORES NULOS ===')
print(df.isnull().sum())

# =========================
# LIMPEZA BÁSICA
# =========================
print('\nLimpando dados inválidos...')

df = df[df['populacao'] > 0]
df = df[df['taxa_mortalidade'].notna()]
df = df[df['perc_cobertura_saude'].notna()]

# =========================
# ESTATÍSTICAS DESCRITIVAS
# =========================
print('\n=== ESTATÍSTICAS DESCRITIVAS ===')

cols = [
    'populacao',
    'total_obitos',
    'taxa_mortalidade',
    'perc_cobertura_saude'
]

print(df[cols].describe())

# =========================
# HISTOGRAMAS
# =========================
print('\nGerando histogramas...')

plt.figure()
df['taxa_mortalidade'].hist(bins=30)
plt.title('Distribuição da Taxa de Mortalidade')
plt.xlabel('Taxa')
plt.ylabel('Frequência')
plt.show()

plt.figure()
df['perc_cobertura_saude'].hist(bins=30)
plt.title('Distribuição da Cobertura de Saúde Privada')
plt.xlabel('% Cobertura')
plt.ylabel('Frequência')
plt.show()

# =========================
# BOXPLOTS (OUTLIERS)
# =========================
print('\nAnalisando outliers...')

plt.figure()
sns.boxplot(x=df['taxa_mortalidade'])
plt.title('Outliers - Taxa de Mortalidade')
plt.show()

plt.figure()
sns.boxplot(x=df['perc_cobertura_saude'])
plt.title('Outliers - Cobertura de Saúde')
plt.show()

# =========================
# RELAÇÃO PRINCIPAL
# =========================
print('\nAnalisando relação entre cobertura e mortalidade...')

plt.figure()
sns.regplot(
    x='perc_cobertura_saude',
    y='taxa_mortalidade',
    data=df,
    scatter_kws={'alpha': 0.5}
)
plt.title('Cobertura de Saúde vs Mortalidade (Tendência)')
plt.xlabel('% Cobertura')
plt.ylabel('Taxa de Mortalidade')
plt.show()

# =========================
# CORRELAÇÃO
# =========================
print('\n=== MATRIZ DE CORRELAÇÃO ===')

corr = df[[
    'taxa_mortalidade',
    'perc_cobertura_saude',
    'populacao'
]].corr()

print(corr)

plt.figure()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Mapa de Correlação')
plt.show()

# =========================
# GRUPOS DE COBERTURA
# =========================
print('\nCriando grupos de cobertura...')

df['grupo_cobertura'] = pd.qcut(
    df['perc_cobertura_saude'],
    4,
    labels=['Muito Baixa', 'Baixa', 'Alta', 'Muito Alta']
)

media_grupos = df.groupby('grupo_cobertura')['taxa_mortalidade'].mean()

print('\n=== MÉDIA DE MORTALIDADE POR GRUPO ===')
print(media_grupos)

plt.figure()
sns.boxplot(
    x='grupo_cobertura',
    y='taxa_mortalidade',
    data=df
)
plt.title('Mortalidade por Nível de Cobertura')
plt.xlabel('Grupo')
plt.ylabel('Taxa de Mortalidade')
plt.show()

# =========================
# RANKINGS
# =========================
print('\n=== TOP 10 MAIOR MORTALIDADE ===')
print(
    df[['id_chave', 'taxa_mortalidade']]
    .sort_values(by='taxa_mortalidade', ascending=False)
    .head(10)
)

print('\n=== TOP 10 MENOR MORTALIDADE ===')
print(
    df[['id_chave', 'taxa_mortalidade']]
    .sort_values(by='taxa_mortalidade', ascending=True)
    .head(10)
)

# =========================
# ÍNDICE DE PRESSÃO NO SUS
# =========================
print('\nCalculando índice de pressão no SUS...')

df['indice_pressao_sus'] = (
    (1 - df['perc_cobertura_saude'] / 100) *
    df['taxa_mortalidade']
)

plt.figure()
sns.histplot(df['indice_pressao_sus'], bins=30)
plt.title('Distribuição do Índice de Pressão no SUS')
plt.xlabel('Índice')
plt.ylabel('Frequência')
plt.show()

print('\n=== TOP 10 PRESSÃO NO SUS ===')
print(
    df[['id_chave', 'indice_pressao_sus']]
    .sort_values(by='indice_pressao_sus', ascending=False)
    .head(10)
)

print('\nEDA finalizado com sucesso.')