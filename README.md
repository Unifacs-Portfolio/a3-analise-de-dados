# 📊 A3BigData: Mapeamento da Desigualdade em Saúde no Brasil

**Equipe:** 
* Roan Nascimento Lisboa 
* Pedro Vinícius Montes dos Reis 
* Erick Barros Ferreira Gomes
* Rwmovido -> Marcus Vinícius dos Santos

Este projeto implementa um ecossistema de **Big Data e Engenharia de Dados (ETL)** focado em investigar o impacto da infraestrutura do Sistema Único de Saúde (SUS) e da desigualdade socioeconômica nas taxas de mortalidade evitável (5 a 74 anos) no Brasil.

Através de um pipeline modular e escalável em Python, o projeto consolida uma *Base Mestra* unindo dezenas de matrizes governamentais brutas em uma série histórica validada (2018 a 2023), isolando fatores de confusão como o Viés Geográfico e o Mix Público-Privado.

---

## 🏛️ Fontes de Dados Integradas
* **DATASUS (SIM & SIH):** Mortalidade Evitável, Internações, Capítulos do CID-10 e Locais de Ocorrência dos Óbitos.
* **DATASUS (CNES):** Infraestrutura hospitalar (Leitos de UTI/Enfermaria e Equipamentos de Suporte à Vida/Diagnóstico), segregados entre rede SUS e Não-SUS.
* **IBGE (PNAD/SIDRA):** População residente, Produto Interno Bruto (PIB), Rendimento Médio *per capita* e Índice de Gini.
* **Atlas Brasil (PNUD):** Índice de Desenvolvimento Humano Municipal (IDHM e IDHM-Longevidade).

---

## 🚀 Como Executar

Pensando na melhor experiência para os desenvolvedores e na padronização do ambiente, a configuração do projeto foi totalmente automatizada. Você só precisa ter o **Python** e o **Jupiter** instalado na sua máquina.

Abra o terminal na pasta raiz do projeto e execute o comando orquestrador para executar o ETL do projeto:

```bash
python start.py
```
Após isso, rode o script abaixo para rodar o Dashboard com os graficos do projeto!

```bash
python dashboard.py
```
--- 

## ⚙️ O que acontece por baixo dos panos?

1. O script identifica o seu sistema operacional automaticamente.

2. Cria um ambiente virtual (venv) isolado para evitar conflitos de versão.

3. Instala todas as bibliotecas necessárias mapeadas no requirements.txt (ex: Pandas, Openpyxl, Plotly, etc.).

4. Verifica e realiza o download de bases de dados pesadas (caso necessário).

5. Inicia o pipeline de ETL divido em duas fases de consolidação.

     * (Nota: Opcionalmente, o pipeline pode ser rodado manualmente através dos scripts "python main.py" seguido de "python etlv2.py").

6. Inicia o script responsável pela análise exploratória (eda.py), onde irá aparecer um **menu** para o usuário escolher qual categoria de gráfico vai ser gerado.

---

## 📂 Arquitetura de Pastas e Módulos

O projeto adota uma arquitetura em camadas baseada nos princípios Clean Code e Single Responsibility (Responsabilidade Única):

```
A3BigData/
│
├── etls/                     # Módulos de Domínio (Processamento de Saúde)
│   ├── etl_leitos.py         # Tratamento matricial e matemático de leitos hospitalares
│   └── etl_equipamentos.py   # Extração estatística do parque tecnológico (Média, Mediana, Desvio)
│
├── utils/                    # Funções utilitárias e de limpeza
│   └── utils.py              # Algoritmos de limpeza, Regex para UFs e remoção dinâmica de rodapés
│
├── datasets/                 # Diretório de armazenamento das bases governamentais brutos
│
├── eda.py                    # Arquivo de geração da Analise Exploratória [EDA]
│
├── main.py                   # [ETL Fase 1] Gera a base de dados consolidada 1 (Demografia + Infra + Economia)
├── etlv2.py                  # [ETL Fase 2] Enriquecimento Idempotente (Subgrupos CID-10 e IDHM via Glob)
│
├── start.py                  # Script orquestrador de setup e inicialização
├── requirements.txt          # Mapeamento de todas as dependências do projeto
└── README.md                 # Documentação oficial do projeto
```

## 📜 Links Úteis

Aqui estão os links respectivos a documentação do projeto e o vídeo de apresentação!

[Video de Apresentação](https://www.youtube.com/watch?v=vDagw8mnkd8)
---
[Documentação Oficial](https://drive.google.com/file/d/1c4QUaFWvaCCMt2rNp7hLS1wIikcUj4G0/view?usp=sharing)
---