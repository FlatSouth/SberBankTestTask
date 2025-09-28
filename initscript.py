import os
import subprocess
import sys
from pathlib import Path

def createVenv(venv_name=".sberenv"):
    if not Path(venv_name).exists():
        print(f"Create virtual environment{venv_name}...")
        subprocess.run([sys.executable, "-m", "venv", venv_name])
    else:
        print("Virtual environment are exists")

def createEnv():

    env_data = {
    "CHAT_URL":"https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
    "AUTH_KEY":"",
    "OAUTH_URL":"https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
    "TOKEN_FILE":"token.txt",
    "CERT_FILE":f"{os.path.abspath('russian_trusted_root_ca_pem.crt')}"
    }

    env_file = Path(".env")
    
    if env_file.exists():
        print(".env exists")
        return
    
    print("Creating .env")
    with open(env_file, "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}='{value}'\n")
    print(".env created")

def installRequirements():
    requirements_file = Path("requirements.txt")
    
    if requirements_file.exists():
        print("Установка зависимостей...")
        pip_path = ".sberenv/Scripts/pip3" if os.name == "nt" else ".sberenv/bin/pip3"
        subprocess.run([pip_path, "install", "-r", "requirements.txt"])
        print("requirements  installed")
    else:
        print("Not find requirements.txt")

def main():
    
    createVenv()
    
    createEnv()
    
    installRequirements()
    
    print("Configure complite\nPlease fill information in .env file about your Authorization key from https://developers.sber.ru/studio/workspaces\n")
    print("Activate env source .sberenv/bin/activate")

if __name__ == "__main__":
    main()
