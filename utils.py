import os
import customtkinter as ctk
from auth import carregar_usuario_atual  

CAMINHO_USUARIO_ATUAL = 'usuario_atual.json'

def logout():
    if os.path.exists(CAMINHO_USUARIO_ATUAL):
        os.remove(CAMINHO_USUARIO_ATUAL)

def marcar_erro(campo):
    campo.configure(border_color="red")

def limpar_erro(campo):
    campo.configure(border_color="gray")  
    
def obter_usuario_logado():
    usuario = carregar_usuario_atual().get("usuario")
    if not usuario:
        raise Exception("Nenhum usuário está logado.")
    return usuario

