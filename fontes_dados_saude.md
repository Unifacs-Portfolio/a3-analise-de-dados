# Guia de Fontes de Dados Complementares em Saúde (CSV)

Este documento reúne as variáveis complementares recomendadas para enriquecer a análise do impacto do setor de saúde na mortalidade evitável, com as respectivas justificativas epidemiológicas, links diretos e instruções passo a passo para baixar os dados em formato CSV.

---

## 1. Cobertura da Atenção Primária e Saúde da Família (APS)
A Atenção Primária é a porta de entrada do SUS. Uma boa cobertura previne que doenças crônicas cheguem a estágios agudos que resultam em óbito.

*   **Variável:** Cobertura de Atenção Básica (AB) e Estratégia Saúde da Família (ESF) por UF e Ano.
*   **Fonte Oficial:** **e-Gestor Atenção Básica** (Ministério da Saúde).
*   **Link de Acesso:** [Histórico de Cobertura - e-Gestor](https://egestorab.saude.gov.br/paginas/acessoPublico/relatorios/relHistoricoCobertura.xhtml)
*   **Como Baixar:**
    1.  No painel, selecione o **Nível de Visualização** como *Estadual*.
    2.  Selecione a **Competência** (mês/ano desejados, ex: Dezembro de cada ano de 2018 a 2024).
    3.  Clique em *Pesquisar*.
    4.  No canto superior direito da tabela exibida, clique no ícone do **Excel (XLS)** ou **CSV** para exportar.

---

## 2. Internações por Condições Sensíveis à Atenção Primária (ICSAP)
Indica internações por doenças (hipertensão, diabetes, asma, etc.) que não deveriam ocorrer se a Atenção Primária fosse eficiente. É o melhor indicador de eficácia clínica da rede básica.

*   **Variável:** Taxa de Internações Sensíveis por UF e Ano.
*   **Fonte Oficial:** **TABNET DATASUS** (SIH - Sistema de Informações Hospitalares).
*   **Link de Acesso:** [SIH/SUS - Internações por UF](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/qiuf.def)
*   **Como Baixar:**
    1.  No campo **Linha**, selecione *Unidade da Federação*.
    2.  No campo **Coluna**, selecione *Ano processamento*.
    3.  No campo **Conteúdo**, selecione *Internações*.
    4.  No filtro **Grupo de causas (ICSAP)** (localizado nos filtros inferiores), você pode filtrar por causas específicas ou selecionar *Todas as causas ICSAP*.
    5.  Selecione os **Períodos Disponíveis** (anos de interesse).
    6.  Clique em *Mostra*.
    7.  Abaixo da tabela exibida, clique no botão **Copia como CSV** ou **Salvar CSV**.

---

## 3. Densidade de Profissionais de Saúde (Recursos Humanos)
Leitos e equipamentos precisam de médicos e enfermeiros para funcionar.

*   **Variável:** Quantidade de Médicos e Enfermeiros cadastrados por UF e Ano.
*   **Fonte Oficial:** **TABNET DATASUS** (CNES - Recursos Humanos).
*   **Link de Acesso:** [CNES - Profissionais por UF](http://tabnet.datasus.gov.br/cgi/deftohtm.exe?cnes/cnv/profuf.def)
*   **Como Baixar:**
    1.  Selecione **Linha:** *Unidade da Federação*.
    2.  Selecione **Coluna:** *Ano*.
    3.  Selecione **Conteúdo:** *Profissionais*.
    4.  No filtro **Classificação do Profissional** (filtros inferiores), selecione *Médicos* ou *Enfermeiros*.
    5.  Selecione os **Períodos Disponíveis**.
    6.  Clique em *Mostra* e depois em **Copia como CSV**.

---

## 4. Cobertura de Saúde Suplementar (Planos de Saúde Privados)
Controla a porcentagem da população que não depende exclusivamente do SUS, desafogando o sistema público.

*   **Variável:** Taxa de Cobertura de Planos de Saúde (Beneficiários) por UF e Ano.
*   **Fonte Oficial:** **Sala de Situação da ANS** / **TABNET ANS**.
*   **Link de Acesso:** [ANS TABNET - Beneficiários](http://www.ans.gov.br/anstabnet/cgi-bin/dh?dados/tabnet_br.def)
*   **Como Baixar:**
    1.  Selecione **Linha:** *Unidade da Federação*.
    2.  Selecione **Coluna:** *Ano*.
    3.  Selecione **Conteúdo:** *Beneficiários*.
    4.  Selecione os **Períodos Disponíveis**.
    5.  Clique em *Mostra* e baixe a tabela em formato CSV.

---

## 5. Financiamento Público da Saúde (Investimento per Capita)
Mostra se estados com mais recursos destinados à saúde obtêm menores taxas de mortalidade.

*   **Variável:** Despesa com Saúde por Habitante (Gasto próprio em saúde per Capita) por UF e Ano.
*   **Fonte Oficial:** **SIOPS** (Sistema de Informações sobre Orçamentos Públicos em Saúde).
*   **Link de Acesso:** [Indicadores do SIOPS](https://www.gov.br/saude/pt-br/acesso-a-informacao/siops/relatorios-publicos/indicadores-estaduais-e-municipais)
*   **Como Baixar:**
    1.  Acesse a área de *Indicadores Estaduais*.
    2.  Escolha a tabela de *Despesas com Saúde*.
    3.  Gere o relatório consolidado para todas as UFs selecionando os anos desejados.
    4.  Exportar a tabela resultante em CSV/Excel.

---

## 6. Envelhecimento Populacional (Padronização Demográfica)
Evita distorções na taxa de óbito. Estados mais velhos naturalmente morrem mais se não fizermos o ajuste por idade.

*   **Variável:** População residente por faixa etária (separando o grupo de 60 a 74 anos) por UF e Ano.
*   **Fonte Oficial:** **Banco de Dados SIDRA / IBGE**.
*   **Link de Acesso:** [IBGE SIDRA - Tabelas de População](https://sidra.ibge.gov.br/home) (Tabelas de estimativas de população por sexo e idade, como a Tabela 5918).
*   **Como Baixar:**
    1.  Pesquise pela tabela de **Estimativa de População**.
    2.  Selecione as **Unidades da Federação** desejadas.
    3.  No filtro **Faixa Etária**, selecione as faixas que compreendem *60 a 74 anos* e a *População Total*.
    4.  Selecione os **Períodos**.
    5.  Clique no ícone de download (nuvem com seta para baixo) e escolha a opção **CSV**.

# ------------------------------------------------------------------------------
# GRÁFICO 4: O Paradoxo da Prevenção (Atenção Básica vs ICSAP)
# Hipótese: Estados com MAIOR cobertura de Saúde da Família têm MENOR taxa de 
# internações por doenças que poderiam ser tratadas no postinho.
# ------------------------------------------------------------------------------
if "cobertura_esf_pct" in df.columns and "taxa_icsap_100k" in df.columns:
    fig_prev = px.scatter(
        df, 
        x="cobertura_esf_pct", 
        y="taxa_icsap_100k", 
        color="regiao", 
        hover_name="nome_unidade_federativa",
        size="populacao",
        trendline="ols",
        title="<b>A Eficácia da Prevenção: Cobertura da Saúde da Família vs Internações Evitáveis (ICSAP)</b><br><sup>Esperamos uma linha descendente: mais prevenção = menos internação</sup>",
        labels={
            "cobertura_esf_pct": "Cobertura da Estratégia Saúde da Família (%)",
            "taxa_icsap_100k": "Taxa de Internações Sensíveis à Atenção Primária (por 100k)",
            "regiao": "Região"
        },
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_prev.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="DarkSlateGrey")))
    fig_prev.update_layout(template="plotly_white")
    fig_prev.show()


# ------------------------------------------------------------------------------
# GRÁFICO 5: Financiamento vs Mortalidade (Controlado por Recursos Humanos)
# Hipótese: O gasto financeiro per capita se traduz em menos mortes apenas 
# se houver profissionais de saúde suficientes (tamanho da bolha).
# ------------------------------------------------------------------------------
if "gasto_saude_per_capita" in df.columns and "medicos_1k" in df.columns:
    fig_fin = px.scatter(
        df, 
        x="gasto_saude_per_capita", 
        y="mortalidade_evitavel_100k", 
        size="medicos_1k", 
        color="regiao",
        hover_name="nome_unidade_federativa",
        trendline="lowess", # Usamos 'lowess' porque a relação dinheiro x saúde costuma fazer uma curva, não uma reta perfeita
        title="<b>Investimento Público vs Mortalidade Evitável</b><br><sup>O tamanho da bolha representa a densidade de Médicos (por 1.000 hab.)</sup>",
        labels={
            "gasto_saude_per_capita": "Despesa com Saúde per Capita (R$ - SIOPS)",
            "mortalidade_evitavel_100k": "Óbitos Evitáveis (por 100k hab.)",
            "medicos_1k": "Médicos por 1k hab."
        },
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_fin.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="black")))
    fig_fin.update_layout(template="plotly_white")
    fig_fin.show()


# ------------------------------------------------------------------------------
# GRÁFICO 6: A Válvula de Escape do Sistema (Planos Privados vs Carga do SUS)
# Hipótese: Estados com alta cobertura de ANS têm menos internações evitáveis 
# no SUS, pois a população resolve na rede privada.
# ------------------------------------------------------------------------------
if "cobertura_ans_pct" in df.columns and "taxa_icsap_100k" in df.columns:
    fig_ans = px.scatter(
        df, 
        x="cobertura_ans_pct", 
        y="taxa_icsap_100k", 
        color="regiao",
        hover_name="nome_unidade_federativa",
        trendline="ols",
        title="<b>A Válvula de Escape: Cobertura Privada (ANS) alivia a carga de internações no SUS?</b>",
        labels={
            "cobertura_ans_pct": "População com Plano de Saúde Privado (%)",
            "taxa_icsap_100k": "Taxa de Internações Sensíveis no SUS (por 100k)"
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_ans.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=1, color="DarkSlateGrey")))
    fig_ans.update_layout(template="plotly_white")
    fig_ans.show()

