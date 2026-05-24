import requests
import pandas as pd
import os

def extrair_populacao_estado_ibge(ano):
    # Roteador Dinâmico: O IBGE muda a tabela nos anos de Censo
    if ano in [2018, 2021]:
        # Tabela 6579: Estimativas (Variável 9324)
        url = f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{ano}/variaveis/9324?localidades=N3[all]"
        ano_resposta = str(ano)
        
    elif ano == 2022:
        # Tabela 4714: Censo Demográfico Oficial (Variável 93)
        url = "https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93?localidades=N3[all]"
        ano_resposta = '2022'
        
    elif ano == 2023:
        # Como não houve estimativa em 2023, usamos o Censo 2022 como Proxy
        print("Aviso: Utilizando base do Censo 2022 como proxy populacional para 2023.")
        url = "https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93?localidades=N3[all]"
        ano_resposta = '2022' # A API vai retornar '2022', mas nós salvaremos como 2023
        
    else:
        print(f"Ano {ano} não mapeado no roteador.")
        return None

    print(f"Consumindo API SIDRA/IBGE para o ano {ano}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro na requisição: Status {response.status_code}")
        return None
        
    data = response.json()
    
    if not data:
        print(f"Nenhum dado encontrado para o ano {ano}.")
        return None
        
    resultados = data[0]['resultados'][0]['series']
    
    lista_populacao = []
    for item in resultados:
        valor_str = item['serie'].get(ano_resposta, '0')
        
        try:
            populacao = int(valor_str)
        except ValueError:
            populacao = 0 
            
        lista_populacao.append({
            'id_uf': item['localidade']['id'], # Agora pega o ID do Estado (Ex: 29 para Bahia)
            'nome_uf': item['localidade']['nome'],
            'populacao': populacao
        })
    
    df_ibge = pd.DataFrame(lista_populacao)
    
    caminho_pasta = f'../datasets/datasets{ano}'
    os.makedirs(caminho_pasta, exist_ok=True)
    
    # Salva o arquivo já carimbado com o ano da requisição
    caminho_arquivo = f'{caminho_pasta}/populacao_ibge_{ano}.csv'
    df_ibge.to_csv(caminho_arquivo, index=False)
    
    print(f"Dados Estaduais do IBGE ({ano}) salvos com sucesso em: {caminho_arquivo}\n")
    return df_ibge

# Executando o pipeline para todos os anos da série histórica
df_pop_2018 = extrair_populacao_estado_ibge(2018)
df_pop_2020 = extrair_populacao_estado_ibge(2021)
df_pop_2022 = extrair_populacao_estado_ibge(2022)
df_pop_2023 = extrair_populacao_estado_ibge(2023)