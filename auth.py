import json
import os
import bcrypt

CAMINHO_ARQUIVO = 'usuarios.json'
CAMINHO_USUARIO_ATUAL = 'usuario_atual.json'

def carregar_dados():
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, 'r') as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(CAMINHO_ARQUIVO, 'w') as f:
        json.dump(dados, f, indent=4)

def criptografar_senha(senha):
    try:
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    except Exception as e:
        print(f"Erro ao criptografar senha: {e}")
        return None

def verificar_senha(senha_digitada, senha_armazenada):
    try:
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_armazenada.encode('utf-8'))
    except Exception as e:
        print(f"Erro na verificação de senha: {e}")
        return False

def salvar_usuario_atual(usuario):
    with open(CAMINHO_USUARIO_ATUAL, 'w') as f:
        json.dump({"usuario": usuario}, f)

def carregar_usuario_atual():
    if os.path.exists(CAMINHO_USUARIO_ATUAL):
        try:
            with open(CAMINHO_USUARIO_ATUAL, 'r') as f:
                dados = json.load(f)
            if isinstance(dados, dict) and "usuario" in dados:
                return dados
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar usuario_atual.json: {e}")
    return {"usuario": ""}

