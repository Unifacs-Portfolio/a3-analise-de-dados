import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
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

# Lista completa de colunas numéricas (incluindo as novas)
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

# Taxas base
if "media_leitos_uti_sus" in df.columns:
    df["leitos_uti_sus_100k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 100000
    df["leitos_uti_sus_1k"] = (df["media_leitos_uti_sus"] / df["populacao"]) * 1000
    LIMITES["max_uti_1k"] = df["leitos_uti_sus_1k"].max() * 1.1
    LIMITES["max_uti_100k"] = df["leitos_uti_sus_100k"].max() * 1.1

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

# Proporções
if "media_leitos_uti_sus" in df.columns and "media_leitos_uti_nao_sus" in df.columns:
    df["total_uti"] = df["media_leitos_uti_sus"] + df["media_leitos_uti_nao_sus"]
    df["pct_uti_sus"] = np.where(
        df["total_uti"] > 0, (df["media_leitos_uti_sus"] / df["total_uti"]) * 100, 0
    )

# NOVAS TAXAS (Colapso e Letalidade)
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
    """Função mestre para evitar repetição de código no Plotly"""
    if x_col not in df_dados.columns or y_col not in df_dados.columns:
        print(f"\n[ERRO] Variáveis '{x_col}' ou '{y_col}' não encontradas no dataset.")
        return

    print("A renderizar gráfico...")
    if modo == "consolidado":
        data = (
            df_dados.groupby(["nome_unidade_federativa", "regiao_ibge"])
            .mean(numeric_only=True)
            .reset_index()
        )
        kwargs = {}
        titulo = titulo_consol
    else:
        data = df_dados
        kwargs = {
            "animation_frame": "ano",
            "animation_group": "nome_unidade_federativa",
        }
        if max_x:
            kwargs["range_x"] = [min_x, max_x]
        if max_y:
            kwargs["range_y"] = [min_y, max_y]
        titulo = titulo_animado

    if size and size in data.columns:
        kwargs["size"] = size
        kwargs["size_max"] = 45

    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=color,
        hover_name="nome_unidade_federativa",
        trendline="ols",
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
        discrete_colors=px.colors.qualitative.Safe,
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
        "<b>[ANIMADO] Especialização do Cuidado: Sem correlação com Enfermaria</b>",
        "<b>[MÉDIA GERAL] Especialização do Cuidado: Sem correlação com Enfermaria</b>",
        max_x=LIMITES.get("max_enf"),
        max_y=LIMITES.get("max_mort"),
        discrete_colors=["#7F8C8D"],
    )


# --- BLOCO B: VIESES ---
def graf_paradoxo_regioes(modo):
    gerador_grafico(
        df,
        "leitos_uti_sus_100k",
        "mortalidade_evitavel_100k",
        modo,
        "<b>[ANIMADO] O Paradoxo Reativo: Blocos regionais sofrendo cargas diferentes</b>",
        "<b>[MÉDIA GERAL] O Paradoxo Reativo: Blocos regionais sofrendo cargas diferentes</b>",
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


def graf_mix_publico_privado(modo):
    if "pct_uti_sus" not in df.columns:
        return print("[ERRO] Variável não encontrada.")
    print("A renderizar gráfico...")
    if modo == "consolidado":
        data = (
            df.groupby(["nome_unidade_federativa", "regiao_ibge"])[["pct_uti_sus"]]
            .mean(numeric_only=True)
            .reset_index()
            .sort_values(by="pct_uti_sus")
        )
        kwargs = {}
        titulo = "<b>[MÉDIA GERAL] Assimetria do Mix Público-Privado (Dependência do SUS)</b>"
    else:
        data = df.sort_values(by=["ano", "regiao_ibge", "pct_uti_sus"])
        kwargs = {
            "animation_frame": "ano",
            "animation_group": "nome_unidade_federativa",
        }
        titulo = "<b>[ANIMADO] Mix Público-Privado: Corrida da Dependência do SUS</b>"

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


# --- BLOCO C: NOVOS (COLAPSO E GRAVIDADE) ---
def graf_prova_colapso(modo):
    gerador_grafico(
        df,
        "internacoes",
        "obitos_domicilio",
        modo,
        "<b>[ANIMADO] A Prova do Colapso: Menos Internações = Mais Mortes em Casa</b>",
        "<b>[MÉDIA GERAL] A Prova do Colapso: Acesso Hospitalar vs Morte Silenciosa</b>",
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
        "<b>[ANIMADO] Corrida Contra o Relógio: Equipamentos de Vida vs Infartos/AVCs</b>",
        "<b>[MÉDIA GERAL] Corrida Contra o Relógio: Equipamentos de Vida vs Infartos/AVCs</b>",
        size="populacao",
        max_x=LIMITES.get("max_equip"),
        max_y=LIMITES.get("max_cap_ix"),
        discrete_colors=px.colors.qualitative.Vivid,
    )


def graf_gargalo_gravidade(modo):
    df_temp = df.copy()
    if "leitos_uti_sus_100k" in df_temp.columns:
        df_temp["tamanho_bolha"] = (
            df_temp["leitos_uti_sus_100k"].fillna(0) + 1
        )  # +1 previne bolha invisível
    gerador_grafico(
        df_temp,
        "dias_internacao",
        "obitos_hospital",
        modo,
        "<b>[ANIMADO] O Gargalo e a Gravidade: Dias de Internação vs Letalidade Hospitalar</b>",
        "<b>[MÉDIA GERAL] O Gargalo e a Gravidade: Tempo de Espera e Mortalidade (Tamanho = UTIs)</b>",
        size="tamanho_bolha" if "tamanho_bolha" in df_temp.columns else None,
        max_x=LIMITES.get("max_dias_int"),
        max_y=LIMITES.get("max_obitos_hosp"),
        discrete_colors=px.colors.qualitative.Prism,
    )


# --- ESTATÍSTICA ---
def rodar_regressao_ols():
    print("\n" + "=" * 50)
    print("RESULTADO DO MODELO DE REGRESSÃO (OLS)")
    print("=" * 50)
    try:
        X = df[["leitos_uti_sus_100k", "idhm", "indice_gini"]].dropna()
        Y = df.loc[X.index, "mortalidade_evitavel_100k"]
        X = sm.add_constant(X)
        modelo_ols = sm.OLS(Y, X).fit()
        print(modelo_ols.summary())
    except Exception as e:
        print(
            f"Erro ao rodar regressão: {e}\n(Verifique se IDHM e Gini não têm valores nulos.)"
        )
    print("=" * 50 + "\n")


# ==============================================================================
# 3. INTERFACE DE TERMINAL
# ==============================================================================
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def perguntar_modo():
    print("\n   \033[93mComo deseja visualizar este gráfico?\033[0m")
    print("   [1] \033[96mAnimado\033[0m (Evolução Ano a Ano)")
    print("   [2] \033[95mVisão Geral\033[0m (Média Consolidada de Todos os Anos)")
    while True:
        resp = input("   👉 Escolha (1 ou 2) » ")
        if resp == "1":
            return "animado"
        elif resp == "2":
            return "consolidado"
        else:
            print("   Opção inválida.")


def menu_principal():
    COR_TITULO = "\033[95m"
    COR_SECCAO = "\033[96m"
    COR_OPCAO = "\033[92m"
    COR_RESET = "\033[0m"

    while True:
        limpar_tela()
        print(
            f"{COR_TITULO}╔════════════════════════════════════════════════════════════╗"
        )
        print(f"║     PAINEL DE ANÁLISE: SAÚDE PÚBLICA E MORTALIDADE         ║")
        print(
            f"╚════════════════════════════════════════════════════════════╝{COR_RESET}"
        )

        print(
            f"\n {COR_SECCAO}📊 [BLOCO A] STORYTELLING & RELAÇÕES CLÍNICAS{COR_RESET}"
        )
        print(
            f"   {COR_OPCAO}1.{COR_RESET} Alocação Reativa     --> UTIs vs Mortalidade Evitável (+0.72)"
        )
        print(
            f"   {COR_OPCAO}2.{COR_RESET} Fator de Proteção    --> Internações vs Mortalidade (-0.15)"
        )
        print(
            f"   {COR_OPCAO}3.{COR_RESET} Nível Complexidade   --> Enfermaria vs Mortalidade (0.00)"
        )

        print(
            f"\n {COR_SECCAO}🌍 [BLOCO B] MITIGAÇÃO DE VIÉS GEOGRÁFICO & SOCIAL{COR_RESET}"
        )
        print(
            f"   {COR_OPCAO}4.{COR_RESET} Paradoxo Regional    --> Carga Epidemiológica por População"
        )
        print(
            f"   {COR_OPCAO}5.{COR_RESET} Viés de Confundimento--> Relação Oculta entre IDHM e Saúde"
        )
        print(
            f"   {COR_OPCAO}6.{COR_RESET} Mix Público/Privado  --> A Dependência Estrita do SUS"
        )

        print(
            f"\n {COR_SECCAO}🚨 [BLOCO C] COLAPSO, GARGALO E LETALIDADE CLÍNICA{COR_RESET}"
        )
        print(
            f"   {COR_OPCAO}7.{COR_RESET} Prova do Colapso     --> Internações vs Morte em Domicílio"
        )
        print(
            f"   {COR_OPCAO}8.{COR_RESET} Corrida p/ Vida      --> Equipamentos vs Doenças do Coração/AVC"
        )
        print(
            f"   {COR_OPCAO}9.{COR_RESET} O Gargalo da Fila    --> Dias Internados vs Morte no Hospital"
        )

        print(f"\n {COR_SECCAO}⚙️  [BLOCO D] MODELAÇÃO MATEMÁTICA{COR_RESET}")
        print(
            f"   {COR_OPCAO}10.{COR_RESET} Executar Regressão OLS (Sumário Estatístico no Terminal)"
        )

        print(
            f"\n {COR_TITULO}────────────────────────────────────────────────────────────"
        )
        print(f"   {COR_OPCAO}0. Sair do Programa{COR_RESET}")
        print(
            f"{COR_TITULO}────────────────────────────────────────────────────────────{COR_RESET}"
        )

        try:
            escolha = input(f"\n👉 Selecione o Gráfico/Ação: {COR_OPCAO}")
            print(f"{COR_RESET}", end="")
        except (KeyboardInterrupt, EOFError):
            print("\n\nPrograma interrompido. Até logo!")
            sys.exit()

        if escolha in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            modo_selecionado = perguntar_modo()
            if escolha == "1":
                graf_alocacao_reativa(modo_selecionado)
            elif escolha == "2":
                graf_fator_protecao(modo_selecionado)
            elif escolha == "3":
                graf_enfermaria(modo_selecionado)
            elif escolha == "4":
                graf_paradoxo_regioes(modo_selecionado)
            elif escolha == "5":
                graf_vies_confundimento(modo_selecionado)
            elif escolha == "6":
                graf_mix_publico_privado(modo_selecionado)
            elif escolha == "7":
                graf_prova_colapso(modo_selecionado)
            elif escolha == "8":
                graf_corrida_relogio(modo_selecionado)
            elif escolha == "9":
                graf_gargalo_gravidade(modo_selecionado)
            input("\nPressione [ENTER] para voltar ao menu...")

        elif escolha == "10":
            limpar_tela()
            rodar_regressao_ols()
            input("\nPressione [ENTER] para voltar ao menu principal...")
        elif escolha == "0":
            limpar_tela()
            print("\n[INFO] Programa encerrado com sucesso. Até à próxima!\n")
            sys.exit()
        else:
            print("\n[ERRO] Opção inválida! Escolha de 0 a 10.")
            input("Pressione [ENTER] para tentar novamente...")


if __name__ == "__main__":
    menu_principal()
