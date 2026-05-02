import requests
import pandas as pd
import os

def extrair_populacao_ibge(ano):
    # A URL agora recebe o ano dinamicamente e usa a variável 9324 correta para a tabela 6579
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/{ano}/variaveis/9324?localidades=N6[all]"
    
    print(f"Consumindo API SIDRA/IBGE para o ano {ano}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erro na requisição: Status {response.status_code}")
        return None
        
    data = response.json()
    
    # Prevenção de erro caso a API retorne uma lista vazia
    if not data:
        print(f"Nenhum dado encontrado para o ano {ano}.")
        return None
        
    # Achatando os dados
    resultados = data[0]['resultados'][0]['series']
    
    lista_populacao = []
    for item in resultados:
        # Pega o valor do ano dinamicamente
        valor_str = item['serie'].get(str(ano), '0')
        
        # O IBGE às vezes retorna '-' ou '...' para dados faltantes. 
        # Esse bloco try/except previne que o script quebre nesses casos.
        try:
            populacao = int(valor_str)
        except ValueError:
            populacao = 0 
            
        lista_populacao.append({
            'id_municipio': item['localidade']['id'],
            'nome_municipio': item['localidade']['nome'],
            'populacao': populacao
        })
    
    df_ibge = pd.DataFrame(lista_populacao)
    
    # Cria o diretório específico do ano, caso ele não exista
    caminho_pasta = f'../datasets/datasets{ano}'
    os.makedirs(caminho_pasta, exist_ok=True)
    
    # Salva o arquivo dinamicamente
    caminho_arquivo = f'{caminho_pasta}/populacao_ibge_{ano}.csv'
    df_ibge.to_csv(caminho_arquivo, index=False)
    
    print(f"Dados do IBGE ({ano}) salvos com sucesso em: {caminho_arquivo}\n")
    return df_ibge

# Executando o pipeline para os dois anos desejados
df_pop_2018 = extrair_populacao_ibge(2018)
df_pop_2020 = extrair_populacao_ibge(2020)