# Fluxograma de Análise: Impacto do Setor de Saúde na Mortalidade Evitável (5 a 74 anos)

Este documento apresenta duas abordagens metodológicas organizadas em fluxogramas de encadeamento (**Forward Chaining** e **Backward Chaining**) para estruturar a análise exploratória de dados e o storytelling de apresentação sobre o impacto do setor de saúde na mortalidade evitável.

---

## 1. Abordagem por Encadeamento para Frente (Forward Chaining)
*Orientada por Dados (Data-Driven)*: Inicia com os dados brutos e variáveis disponíveis, calcula indicadores, testa relações estatísticas e, através de regras de inferência, chega à conclusão.

### Diagrama Mermaid (Encadeamento para Frente)

```mermaid
graph TD
    %% Estilos de nós
    classDef input fill:#1f2937,stroke:#3b82f6,stroke-width:2px,color:#f3f4f6;
    classDef process fill:#1e3a8a,stroke:#2563eb,stroke-width:2px,color:#f3f4f6;
    classDef rule fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#f3f4f6;
    classDef model fill:#1e4b3c,stroke:#10b981,stroke-width:2px,color:#f3f4f6;
    classDef conclusion fill:#7c2d12,stroke:#ea580c,stroke-width:3px,color:#f3f4f6;

    subgraph DadosBrutos["1. Fatos Iniciais (Dados Brutos por UF/Ano)"]
        D1["Infraestrutura CNES<br>(Leitos UTI/Enf, Equipamentos)"]:::input
        D2["Uso do Sistema<br>(Internações, Dias de Internação)"]:::input
        D3["Mortalidade e População<br>(Óbitos Evitáveis 5-74, População)"]:::input
        D4["Controles Socioeconômicos<br>(Gini, Renda per Capita, IDHM)"]:::input
    end

    subgraph Indicadores["2. Processamento (Cálculo de Indicadores Padronizados)"]
        I1["Taxa de Mortalidade Evitável<br>(por 100k hab.)"]:::process
        I2["Leitos UTI e Enfermaria SUS / não-SUS<br>(por 1k hab.)"]:::process
        I3["Equipamentos de Imagem / Vida<br>(por 100k hab.)"]:::process
        I4["Taxa de Internação Hospitalar<br>(por 100k hab.)"]:::process
    end

    subgraph Regras["3. Análise Bivariada (Regras de Correlação de Pearson)"]
        R1{"Regra 1: Leitos UTI SUS<br>correlaciona positivamente<br>com óbitos evitáveis?"}:::rule
        R2{"Regra 2: Taxa de internações<br>correlaciona negativamente<br>com óbitos evitáveis?"}:::rule
        R3{"Regra 3: Variáveis de infraestrutura<br>têm maior correlação que<br>fatores socioeconômicos?"}:::rule
    end

    subgraph Modelagem["4. Modelagem Multivariada (Isolamento de Efeito)"]
        M1["Regressão Linear Múltipla<br>(Controlar por Gini, IDHM e Renda)"]:::model
    end

    subgraph Goal["5. Conclusão (Meta Final)"]
        C1["Conclusão:<br>O setor de saúde afeta diretamente<br>a mortalidade evitável?"]:::conclusion
    end

    %% Conexões
    D1 & D3 --> I2 & I3
    D2 & D3 --> I4
    D3 --> I1
    
    I1 & I2 --> R1
    I1 & I4 --> R2
    I1 & D4 --> R3
    
    R1 -- Sim (+0.72) --> M1
    R2 -- Sim (-0.15) --> M1
    R3 -- Análise comparativa --> M1
    
    M1 -->|Avaliar p-value e Coeficiente Beta| C1

```

### Roteiro de Storytelling: Do Dado ao Insight (Forward Chaining)
1. **A Origem**: Começamos com os dados reais de infraestrutura do CNES e de óbitos do DATASUS por Unidade Federativa.
2. **A Normalização**: Explicamos que, para comparar estados de tamanhos diferentes, transformamos números brutos em taxas (leitos por 1.000 habitantes, óbitos e internações por 100.000 habitantes).
3. **As Surpresas da Correlação**:
   - Mostramos que a **taxa de internação hospitalar** tem correlação negativa ($-0,15$), sugerindo que um maior volume de internações (acesso) está associado a menor mortalidade evitável.
   - Mostramos que a densidade de **leitos de UTI SUS** tem correlação positiva alta ($+0,72$). Isso nos leva ao insight de que a UTI é uma resposta reativa: onde há maior gravidade epidemiológica, há maior indução e instalação de leitos de terapia intensiva.
4. **O Controle de Variáveis**: Para garantir que isso não é apenas reflexo da riqueza do estado, rodamos uma regressão controlando por IDHM e Gini.
5. **O Veredicto**: Concluímos se a infraestrutura de saúde de fato reduz mortes evitáveis de forma independente das condições sociais.

---

## 2. Abordagem por Encadeamento para Trás (Backward Chaining)
*Orientada a Hipóteses (Goal-Driven)*: Começa com a pergunta final (a meta) e retrocede para encontrar as condições estatísticas necessárias, as sub-metas e, finalmente, os dados que suportam cada premissa.

### Diagrama Mermaid (Encadeamento para Trás)

```mermaid
graph TD
    %% Estilos de nós
    classDef input fill:#1f2937,stroke:#3b82f6,stroke-width:2px,color:#f3f4f6;
    classDef process fill:#1e3a8a,stroke:#2563eb,stroke-width:2px,color:#f3f4f6;
    classDef subgoal fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#f3f4f6;
    classDef evidence fill:#1e4b3c,stroke:#10b981,stroke-width:2px,color:#f3f4f6;
    classDef goal fill:#7c2d12,stroke:#ea580c,stroke-width:3px,color:#f3f4f6;

    subgraph MetaFinal["1. Meta Principal"]
        G1["Meta: Provar se o setor de saúde<br>afeta a taxa de mortalidade evitável<br>entre pessoas de 5 a 74 anos."]:::goal
    end

    subgraph SubMetas["2. Sub-metas (Condições Necessárias)"]
        SG1["Sub-meta A:<br>Existe efeito significativo da capacidade de leitos<br>e equipamentos sobre a mortalidade?"]:::subgoal
        SG2["Sub-meta B:<br>Existe efeito do acesso/uso (internações)<br>na redução da mortalidade?"]:::subgoal
        SG3["Sub-meta C:<br>O efeito da saúde é independente<br>dos fatores socioeconômicos?"]:::subgoal
    end

    subgraph Evidencias["3. Evidências Estatísticas Requeridas"]
        E1["Coeficiente de leitos/equipamentos<br>estatisticamente significativo (p < 0.05)<br>no modelo de regressão."]:::evidence
        E2["Correlação negativa e significativa<br>entre taxa de internação hospitalar<br>e óbitos evitáveis."]:::evidence
        E3["Modelo multivariado com R² robusto<br>onde coeficientes de saúde<br>permanecem significativos sob controle."]:::evidence
    end

    subgraph MetricasCalculadas["4. Métricas e Variáveis Necessárias"]
        M1["Taxa de óbitos evitáveis por 100k"]:::process
        M2["Taxa de internações por 100k"]:::process
        M3["Leitos UTI e Enfermaria por 1k (SUS vs Não-SUS)"]:::process
        M4["IDHM, Gini e Renda per capita por UF/Ano"]:::process
    end

    subgraph FontesDados["5. Fontes de Dados (Fatos Iniciais)"]
        FD1["DATASUS SIM (Óbitos Evitáveis 5-74)"]:::input
        FD2["DATASUS SIH (Internações e Dias)"]:::input
        FD3["DATASUS CNES (Equipamentos e Leitos)"]:::input
        FD4["IBGE (População e Socioeconomia)"]:::input
    end

    %% Conexões do Encadeamento para Trás (retrocedendo da meta para a base)
    G1 --> SG1 & SG2 & SG3
    
    SG1 --> E1
    SG2 --> E2
    SG3 --> E3
    
    E1 & E2 & E3 --> M1 & M2 & M3 & M4
    
    M1 --> FD1
    M2 --> FD2
    M3 --> FD3
    M4 --> FD4

```

### Roteiro de Storytelling: Do Problema à Evidência (Backward Chaining)
1. **A Pergunta de Milhão**: Iniciamos a apresentação com o questionamento: *"O investimento em infraestrutura e o acesso à saúde pública realmente reduzem as mortes que poderiam ser evitadas em pessoas de 5 a 74 anos no Brasil?"*
2. **As Condições de Prova**: Explicamos que, para responder "sim", precisamos provar três coisas (as sub-metas):
   - Que a quantidade de recursos hospitalares faz diferença.
   - Que o acesso a internações reduz a mortalidade.
   - Que o impacto do setor de saúde não é meramente um reflexo da desigualdade de renda ou IDHM regional.
3. **A Busca pela Evidência**:
   - Mostramos a análise de regressão múltipla, evidenciando se a presença de leitos e equipamentos afeta o indicador sob controle socioeconômico.
   - Apresentamos a taxa de internação hospitalar como um fator de proteção associado a menores óbitos evitáveis.
4. **Os Fundamentos no Dado Real**: Concluímos mostrando a base de dados consolidada que unificou SIM, CNES, SIH e dados socioeconômicos do IBGE.

---

## 3. Recomendações para a Análise Exploratória (EDA)
Com base nas correlações preliminares observadas nos dados consolidados:
* **Mortalidade Evitável 100k vs Leitos UTI SUS 1k ($+0.7267$):** Investigue essa correlação positiva. Crie um gráfico de dispersão com uma linha de tendência e destaque estados do Norte/Nordeste vs Sul/Sudeste. Demonstre que a alocação de UTI é frequentemente reativa à alta morbidade local.
* **Mortalidade Evitável 100k vs Internações 100k ($-0.1493$):** Plote a relação entre a taxa de internação e a mortalidade evitável. Isso sugere que o acesso hospitalar estruturado previne mortes por causas agudas tratáveis.
* **Leitos de Enfermaria SUS 1k ($-0.0003$):** Mostre que a distribuição simples de leitos de enfermaria comuns não possui correlação linear com a redução de mortes evitáveis de 5 a 74 anos, indicando a necessidade de especialização do cuidado (UTI, diagnóstico por imagem e tecnologias de suporte à vida).
