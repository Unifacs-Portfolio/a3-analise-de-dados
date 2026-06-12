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
    "2. Causas mal definidas",
    "obitos_outro_estab_saude",
    "Cap IX_hospital",
    "media_equip_diag_imagem_sus",
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

# --- MAPA DE CORES PADRONIZADO ---
CORES_REGIOES = {
    "Norte": "#2ECC71",  # Verde
    "Nordeste": "#E74C3C",  # Vermelho
    "Sudeste": "#3498DB",  # Azul
    "Centro-Oeste": "#F1C40F",  # Amarelo
    "Sul": "#9B59B6",  # Roxo
}

# O Truque de Cores Contínuas para a Linha Geral
mapa_regioes_id = {"Norte": 0, "Nordeste": 1, "Sudeste": 2, "Centro-Oeste": 3, "Sul": 4}
df["regiao_id"] = df["regiao_ibge"].map(mapa_regioes_id)
# Escala contínua exata mapeada para os IDs acima (0 a 4)
ESCALA_CONTINUA_REGIOES = [
    CORES_REGIOES["Norte"],
    CORES_REGIOES["Nordeste"],
    CORES_REGIOES["Sudeste"],
    CORES_REGIOES["Centro-Oeste"],
    CORES_REGIOES["Sul"],
]

# ------------------------------------------------------------------------------
# FEATURE ENGINEERING & LIMITES DE EIXO (VERSÃO OTIMIZADA)
# ------------------------------------------------------------------------------
LIMITES = {}

taxas_populacionais = [
    ("media_leitos_uti_sus", "leitos_uti_sus_100k", 100000, "max_uti_100k"),
    ("media_leitos_uti_sus", "leitos_uti_sus_1k", 1000, "max_uti_1k"),
    ("media_leitos_uti_nao_sus", "leitos_uti_privado_100k", 100000, None),
    ("media_leitos_enf_sus", "leitos_enf_sus_1k", 1000, "max_enf"),
    ("obitos_evitaveis", "mortalidade_evitavel_100k", 100000, "max_mort"),
    ("internacoes", "internacoes_100k", 100000, "max_int"),
    ("media_equip_manut_vida_sus", "equip_vida_sus_100k", 100000, "max_equip"),
    ("internacoes_sus_total", "internacoes_sus_100k", 100000, "max_int_sus"),
    (
        "obitos_domicilio",
        "obitos_domicilio_100k",
        100000,
        "max_obitos_dom",
    ),
    ("Cap IX_geral", "cap_ix_100k", 100000, "max_cap_ix"),
    (
        "obitos_hospital",
        "obitos_hospital_100k",
        100000,
        "max_obitos_hosp",
    ),
    ("dias_internacao_sus_total", "dias_internacao_sus_100k", 100000, "max_dias_int"),
    ("2. Causas mal definidas", "causas_mal_definidas_100k", 100000, "max_mal_def"),
    ("obitos_outro_estab_saude", "obitos_outro_estab_100k", 100000, "max_out_estab"),
    ("Cap IX_hospital", "cap_ix_hospital_100k", 100000, "max_cap_ix_hosp"),
]

for col_origem, col_nova, mult, chave_limite in taxas_populacionais:
    if col_origem in df.columns:
        df[col_nova] = (df[col_origem] / df["populacao"]) * mult
        if chave_limite:
            LIMITES[chave_limite] = df[col_nova].max() * 1.1

# Outras proporções
if "pib_milhares" in df.columns:
    df["pib_per_capita_absoluto"] = (df["pib_milhares"] * 1000) / df["populacao"]
    LIMITES["max_pib"] = df["pib_per_capita_absoluto"].max() * 1.1

if "dias_internacao" in df.columns and "internacoes" in df.columns:
    df["dias_por_internacao"] = df["dias_internacao"] / df["internacoes"]
    LIMITES["max_dias_por_int"] = df["dias_por_internacao"].max() * 1.1

if "media_leitos_uti_sus" in df.columns and "media_leitos_uti_nao_sus" in df.columns:
    df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]
    df["pct_uti_sus"] = np.where(
        df["total_uti"] > 0, (df["media_leitos_uti_sus"] / df["total_uti"]) * 100, 0
    )

for col, min_key, max_key in [
    ("idhm", "min_idhm", "max_idhm"),
    ("indice_gini", "min_gini", "max_gini"),
]:
    if col in df.columns:
        LIMITES[min_key] = df[col].min() * 0.95
        LIMITES[max_key] = df[col].max() * 1.05

print("[2/2] Dados processados com sucesso!\n")


# ==============================================================================
# 2. FUNÇÕES GERADORAS DE GRÁFICOS DINÂMICOS
# ==============================================================================

# Dicionário mestre para formatar automaticamente todos os eixos e tooltips
MAPA_NOMES = {
    "leitos_uti_sus_100k": "Leitos UTI SUS (por 100k hab.)",
    "leitos_uti_sus_1k": "Leitos UTI SUS (por 1k hab.)",
    "leitos_uti_privado_100k": "Leitos UTI Privados (por 100k hab.)",
    "leitos_enf_sus_1k": "Leitos Enf. SUS (por 1k hab.)",
    "mortalidade_evitavel_100k": "Mortalidade Evitável (por 100k hab.)",
    "internacoes_100k": "Total de Internações (por 100k hab.)",
    "equip_vida_sus_100k": "Equip. Suporte à Vida SUS (por 100k hab.)",
    "internacoes_sus_100k": "Internações no SUS (por 100k hab.)",
    "obitos_domicilio_100k": "Óbitos em Domicílio (por 100k hab.)",
    "cap_ix_100k": "Óbitos Cardiovasculares (por 100k hab.)",
    "obitos_hospital_100k": "Óbitos Hospitalares (por 100k hab.)",
    "dias_internacao_sus_100k": "Dias de Internação SUS (por 100k hab.)",
    "causas_mal_definidas_100k": "Causas Mal Definidas (por 100k hab.)",
    "obitos_outro_estab_100k": "Óbitos em UPAs/Outros (por 100k hab.)",
    "cap_ix_hospital_100k": "Óbitos Cardiovasculares no Hospital (por 100k hab.)",
    "idhm": "Índice de Desenv. Humano (IDHM)",
    "indice_gini": "Índice de Desigualdade (Gini)",
    "pib_per_capita_absoluto": "PIB per Capita (R$)",
    "pct_uti_sus": "Dependência de UTIs do SUS (%)",
    "pct_mortes_evitaveis": "Taxa de Mortes Evitáveis no Hospital (%)",
    "dias_por_internacao": "Média de Dias por Internação",
    "ano": "Ano",
    "nome_unidade_federativa": "Unidade Federativa",
    "regiao_ibge": "Região",
    "taxa_obitos_100k": "Taxa Nacional de Óbitos Evitáveis",
}


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
):
    if x_col not in df_dados.columns or y_col not in df_dados.columns:
        return print(
            f"\n[ERRO] Variáveis '{x_col}' ou '{y_col}' não encontradas no dataset."
        )

    print("A renderizar gráfico...")
    data = df_dados.copy()

    # 1. Agregação Se for Modo Consolidado
    if modo == "consolidado":
        data = (
            data.groupby(["nome_unidade_federativa", "regiao_ibge", "regiao_id"])
            .mean(numeric_only=True)
            .reset_index()
        )

    # 2. Configurações Base da Animação
    kwargs = {}
    if modo != "consolidado":
        kwargs["animation_frame"] = "ano"
        kwargs["animation_group"] = "nome_unidade_federativa"
        if max_x:
            kwargs["range_x"] = [min_x, max_x]
        if max_y:
            kwargs["range_y"] = [min_y, max_y]

    # 3. O TRUQUE DE EXAGERO VISUAL PARA O TAMANHO (Corrige o IDHM)
    if size and size in data.columns:
        min_val = data[size].min()
        data["tamanho_visual"] = (data[size] - min_val + 0.05) ** 2

        kwargs["size"] = "tamanho_visual"
        kwargs["size_max"] = 55
        kwargs["hover_data"] = {size: True, "tamanho_visual": False}

    # 4. Geração do Gráfico Consoante o Modo
    if modo == "consolidado":
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color,
            hover_name="nome_unidade_federativa",
            trendline="ols",
            trendline_scope="overall",
            title=titulo_consol,
            color_discrete_map=CORES_REGIOES,
            labels=MAPA_NOMES,
            **kwargs,
        )
    elif modo == "animado_regional":
        titulo = titulo_animado + " <br><sup>(Com Linhas de Tendência Regionais)</sup>"
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color,
            hover_name="nome_unidade_federativa",
            trendline="ols",
            trendline_scope="trace",
            title=titulo,
            color_discrete_map=CORES_REGIOES,
            labels=MAPA_NOMES,
            **kwargs,
        )
    elif modo == "animado_nacional":
        titulo = (
            titulo_animado + " <br><sup>(Tendência Nacional Dinâmica do Brasil)</sup>"
        )

        # PASSO A: Cria o gráfico visual principal com os pontos coloridos por Região (sem linha)
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color,
            hover_name="nome_unidade_federativa",
            title=titulo,
            color_discrete_map=CORES_REGIOES,
            labels=MAPA_NOMES,
            **kwargs,
        )

        # PASSO B: Cria o "Gráfico Fantasma" sem cores para forçar o cálculo OLS limpo ano a ano
        kwargs_fantasma = kwargs.copy()
        if "hover_data" in kwargs_fantasma:
            del kwargs_fantasma["hover_data"]  # Remove dados extras
        fig_fantasma = px.scatter(
            data, x=x_col, y=y_col, trendline="ols", **kwargs_fantasma
        )

        # PASSO C: Roubar a linha do frame inicial do fantasma e colar no gráfico principal
        linhas_iniciais = [t for t in fig_fantasma.data if t.mode == "lines"]
        if linhas_iniciais:
            linha_base = linhas_iniciais[0]
            linha_base.line.color = (
                "black"  # Pinta a linha geral de preto para dar destaque
            )
            linha_base.line.width = 3
            linha_base.name = "Tendência Brasil"
            linha_base.showlegend = True
            fig.add_trace(linha_base)

        # PASSO D: Fazer a mesma injeção mágica para CADA ANO da animação
        for i, frame in enumerate(fig.frames):
            linhas_frame = [t for t in fig_fantasma.frames[i].data if t.mode == "lines"]
            if linhas_frame:
                linha_f = linhas_frame[0]
                linha_f.line.color = "black"
                linha_f.line.width = 3
                # Adiciona a linha de tendência animada aos dados das bolinhas
                frame.data = list(frame.data) + [linha_f]

    # 5. Formatação Final (Aplica borda preta apenas nas bolhas, ignorando as linhas)
    fig.update_traces(
        marker=dict(opacity=0.8, line=dict(width=1, color="black")),
        selector=dict(mode="markers"),
    )
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
    )


def graf_apagao_diagnostico(modo):
    gerador_grafico(
        df,
        "idhm",
        "causas_mal_definidas_100k",
        modo,
        "<b>[ANIMADO] O Apagão Diagnóstico: IDHM vs Causas Mal Definidas</b>",
        "<b>[MÉDIA GERAL] O Apagão Diagnóstico: A Pobreza mascara a Causa da Morte</b>",
        min_x=LIMITES.get("min_idhm", 0),
        max_x=LIMITES.get("max_idhm", 1),
        max_y=LIMITES.get("max_mal_def"),
    )


# --- BLOCO C: COLAPSO E GRAVIDADE ---
def graf_prova_colapso(modo):
    gerador_grafico(
        df,
        "internacoes_100k",
        "obitos_outro_estab_100k",
        modo,
        "<b>[ANIMADO] A Retenção Mortal: Internações vs Mortes em UPAs/Ambulâncias</b>",
        "<b>[MÉDIA GERAL] A Retenção Mortal: A falta de camas no Hospital Principal</b>",
        max_x=LIMITES.get("max_int"),
        max_y=LIMITES.get("max_out_estab"),
    )


def graf_corrida_relogio(modo):
    gerador_grafico(
        df,
        "equip_vida_sus_100k",
        "cap_ix_100k",
        modo,
        "<b>[ANIMADO] Equipamentos de Vida vs Infartos/AVCs Gerais (Tamanho = População)</b>",
        "<b>[MÉDIA GERAL] Equipamentos de Vida vs Infartos/AVCs Gerais</b>",
        size="populacao",
        max_x=LIMITES.get("max_equip"),
        max_y=LIMITES.get("max_cap_ix"),
    )


def graf_gargalo_gravidade(modo):
    df_temp = df.copy()
    if "equip_vida_sus_100k" in df_temp.columns:
        df_temp["tamanho_bolha"] = df_temp["equip_vida_sus_100k"].fillna(0) + 1
    gerador_grafico(
        df_temp,
        "dias_por_internacao",
        "cap_ix_hospital_100k",
        modo,
        "<b>[ANIMADO] O Gargalo da Fila: Dias p/ Internação vs Mortes Cardiovasculares (Tamanho Bolha = Equip. Suporte à Vida SUS)</b>",
        "<b>[MÉDIA GERAL] O Gargalo da Fila: (Tamanho Bolha = Equip. Suporte à Vida)</b>",
        size="tamanho_bolha" if "tamanho_bolha" in df_temp.columns else None,
        max_x=LIMITES.get("max_dias_por_int"),
        max_y=LIMITES.get("max_cap_ix_hosp"),
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
        labels=MAPA_NOMES,  # <-- TRADUÇÃO DOS NOMES AQUI
    )
    fig.update_traces(line=dict(color="darkred", width=4), marker=dict(size=12))
    fig.update_layout(template="plotly_white")
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
        color_discrete_map=CORES_REGIOES,
        labels=MAPA_NOMES,  # <-- TRADUÇÃO DOS NOMES AQUI
        **kwargs,
    )
    fig.add_vline(x=50, line_dash="dash", line_color="black")
    fig.update_layout(
        template="plotly_white",
        yaxis=dict(autorange="reversed", categoryorder="total ascending"),
        height=750,
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
        labels=dict(x="Ano", y="Unidade Federativa", color="Taxa de Óbitos"),
    )
    fig.update_layout(template="plotly_white", height=700)
    fig.show()


def graf_matriz_correlacao():
    cols = [
        "mortalidade_evitavel_100k",
        "indice_gini",
        "idhm",
        "pib_per_capita_absoluto",
        "pct_uti_sus",
        "dias_por_internacao",
        "equip_vida_sus_100k",
    ]
    # Filtra as colunas que existem e calcula a correlação
    corr = df[[c for c in cols if c in df.columns]].corr()

    # TRADUÇÃO DOS NOMES NA MATRIZ: Muda o nome das linhas e colunas
    corr = corr.rename(columns=MAPA_NOMES, index=MAPA_NOMES)

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
            name="UTIs SUS (por 100k hab.)",
            line=dict(color="#008080", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=evolucao["ano"],
            y=evolucao["uti_privado"],
            name="UTIs Privadas (por 100k hab.)",
            line=dict(color="#E67E22", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=evolucao["ano"],
            y=evolucao["taxa_mort"],
            name="Taxa Mortalidade Evitável",
            line=dict(color="darkred", width=4, dash="dot"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="<b>Evolução Histórica Nacional Real</b>",
        template="plotly_white",
        hovermode="x unified",
    )
    fig.update_xaxes(title_text="Ano")
    fig.update_yaxes(title_text="Oferta de UTIs", secondary_y=False)
    fig.update_yaxes(title_text="Taxa de Mortalidade", secondary_y=True)
    fig.show()


def graf_ranking_cid10():
    print("A renderizar o Ranking de Causas (CID-10)...")

    # 1. Filtramos apenas as colunas que contêm os sufixos exatos desejados
    sufixos_permitidos = ["_geral", "_hospital", "_domicilio"]
    cols_cid = [
        c
        for c in df.columns
        if c.startswith("Cap ")
        and not c.endswith("_y")
        and any(sufixo in c for sufixo in sufixos_permitidos)
    ]

    if not cols_cid:
        return print("\n[ERRO] Não foram encontradas colunas do CID-10 válidas.")

    # 2. Agrupamento e transformação estrutural
    df_cid = df.groupby("ano")[cols_cid].sum().reset_index()
    df_melt = df_cid.melt(
        id_vars=["ano"],
        value_vars=cols_cid,
        var_name="Capitulo",
        value_name="Total_Obitos",
    )

    # 3. Limpeza e Formatação Elegante dos Rótulos
    df_melt["Capitulo"] = (
        df_melt["Capitulo"]
        .str.replace("_x", "", regex=False)
        .str.replace("_geral", " (Geral)", regex=False)
        .str.replace("_hospital", " (Hospital)", regex=False)
        .str.replace("_domicilio", " (Domicílio)", regex=False)
    )

    # 4. Ordenação e Limites
    df_melt = df_melt[df_melt["Total_Obitos"] > 0]
    df_melt = df_melt.sort_values(by=["ano", "Total_Obitos"], ascending=[True, True])
    limite_max = df_melt["Total_Obitos"].max() * 1.15

    # 5. Renderização
    fig = px.bar(
        df_melt,
        x="Total_Obitos",
        y="Capitulo",
        animation_frame="ano",
        orientation="h",
        title="<b>Ranking de Causas: Evolução dos Óbitos (Geral, Hospital e Domicílio)</b>",
        labels={"Total_Obitos": "Volume de Óbitos", "Capitulo": "CID-10", "ano": "Ano"},
        color="Capitulo",
        text="Total_Obitos",
    )
    fig.update_traces(texttemplate="%{text:.3s}", textposition="outside")
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        height=800,
        xaxis=dict(range=[0, limite_max]),
        yaxis=dict(categoryorder="total ascending"),
    )
    fig.show()


def graf_morte_silenciosa(modo):
    gerador_grafico(
        df,
        "internacoes_100k",
        "obitos_domicilio_100k",
        modo,
        "<b>[ANIMADO] A Morte Silenciosa: Menos Internações geram mais Mortes em Domicílio</b>",
        "<b>[MÉDIA GERAL] A Morte Silenciosa: Menos Internações geram mais Mortes em Domicílio</b>",
        max_x=LIMITES.get("max_int"),
        max_y=LIMITES.get("max_obitos_dom"),
    )


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


# ==============================================================================
# 3. INTERFACE DE TERMINAL
# ==============================================================================
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def perguntar_modo_dispersao():
    print(
        "\n   \033[93mComo deseja visualizar as Linhas de Correlação?\033[0m\n   [1] \033[96mAnimado (Linha Geral)\033[0m       - Evolução com a tendência do Brasil\n   [2] \033[96mAnimado (Linhas Regionais)\033[0m  - Evolução com a tendência de cada Região\n   [3] \033[95mVisão Geral Consolidada\033[0m     - Média Histórica Congelada (Todos os anos)"
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
    print(
        "\n   \033[93mComo deseja visualizar este gráfico?\033[0m\n   [1] \033[96mAnimado\033[0m     - Evolução Ano a Ano\n   [2] \033[95mVisão Geral\033[0m - Média Consolidada de Todos os Anos"
    )
    while True:
        resp = input("   👉 Escolha (1 ou 2) » ")
        if resp in ["1", "2"]:
            return "animado" if resp == "1" else "consolidado"
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
        print(f"\n {COR_SECCAO}📊 [BLOCO A] RELAÇÕES CLÍNICAS{COR_RESET}")
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
            f"   {COR_OPCAO}7.{COR_RESET} Apagão Diagnóstico   --> IDHM vs Causas Mal Definidas"
        )

        print(f"\n {COR_SECCAO}🚨 [BLOCO C] COLAPSO E LETALIDADE{COR_RESET}")
        print(
            f"   {COR_OPCAO}8.{COR_RESET} Morte Silenciosa     --> Internações vs Mortes em Domicílio"
        )
        print(
            f"   {COR_OPCAO}9.{COR_RESET} Retenção em UPAs     --> Internações vs Mortes em UPAs"
        )
        print(
            f"   {COR_OPCAO}10.{COR_RESET} Corrida p/ Vida      --> Equipamentos vs Doenças Cap IX"
        )
        print(
            f"   {COR_OPCAO}11.{COR_RESET} O Gargalo da Fila    --> Média de Dias Internados vs Morte Cardíaca"
        )

        print(f"\n {COR_SECCAO}📈 [BLOCO D] VISÕES GLOBAIS PANORÂMICAS{COR_RESET}")
        print(
            f"   {COR_OPCAO}12.{COR_RESET} Evolução Nacional    --> Linha do Tempo (Taxa Brasil)"
        )
        print(
            f"   {COR_OPCAO}13.{COR_RESET} Mix Público/Privado  --> Corrida de Barras (% de UTI SUS)"
        )
        print(
            f"   {COR_OPCAO}14.{COR_RESET} Mapa de Calor        --> Evolução Regional por Ano"
        )
        print(
            f"   {COR_OPCAO}15.{COR_RESET} Matriz de Correlação --> Interação Global de Variáveis"
        )
        print(
            f"   {COR_OPCAO}16.{COR_RESET} Eixo Duplo Histórico --> Infraestrutura vs Mortalidade"
        )
        print(
            f"   {COR_OPCAO}17.{COR_RESET} Ranking Causas Morte --> Corrida de Capítulos do CID-10"
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

        if escolha in [str(i) for i in range(1, 12)]:  # Agora vai de 1 a 11
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
                graf_apagao_diagnostico(modo)
            elif escolha == "8":
                graf_morte_silenciosa(modo)
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
