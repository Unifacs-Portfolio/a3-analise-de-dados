import os
import subprocess
import sys
import platform


def executar_comando(comando, descricao):
    print(f"\n🚀 {descricao}...")
    try:
        # Executa o comando no terminal e para se der erro
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError:
        print(f"\n❌ Erro crítico na etapa: {descricao}")
        print("Verifique os logs acima para entender o problema.")
        sys.exit(1)


def main():
    print("=" * 45)
    print(" 🛠️  Iniciando o Dashboard do Projeto A3BigData  🛠️ ")
    print("=" * 45)

    # Identificar o sistema operacional para achar o caminho certo do venv
    sistema = platform.system()
    if sistema == "Windows":
        python_venv = os.path.join("venv", "Scripts", "python")
    else:  # Linux ou Mac
        python_venv = os.path.join("venv", "bin", "python")

    # Atualizar dependências pelo requirements.txt
    executar_comando(
        [python_venv, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
        "Instalando/Atualizando bibliotecas do requirements.txt",
    )

    # Executar a aplicação principal
    print("\n" + "=" * 45)
    print(" 🎯 Tudo pronto! Iniciando o Dashboard(eda.py)...")
    print("=" * 45 + "\n")

    try:
        subprocess.run([python_venv, "eda.py"])
    except KeyboardInterrupt:
        print("\n🛑 Aplicação encerrada pelo usuário.")


if __name__ == "__main__":
    main()
