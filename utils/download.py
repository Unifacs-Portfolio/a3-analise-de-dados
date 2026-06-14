import gdown
import os

def baixar_datasets():
    id_da_pasta = '1MCdSJvTEgZFBawR2GEc82dYAoF_Ccf4E?usp=sharing'
    url = f'https://drive.google.com/drive/folders/{id_da_pasta}'
    
    pasta_destino = './datasets'

    # Verifica se os dados já foram baixados para economizar tempo e banda
    if os.path.exists(pasta_destino):
        print(f"✅ Os dados já estão na pasta '{pasta_destino}'. Pulando o download.")
        return

    print("📥 Iniciando o download dos dados do DATASUS (isso pode demorar um pouco)...")
    
    # O gdown fará o download da pasta inteira
    gdown.download_folder(url, output=pasta_destino, quiet=False, use_cookies=False)
    
    print("🚀 Download concluído com sucesso!")

if __name__ == '__main__':
    baixar_datasets()