import customtkinter as ctk
import re
import json
from auth import carregar_dados, salvar_dados, criptografar_senha, verificar_senha, salvar_usuario_atual, carregar_usuario_atual
from quiz import quizzes, salvar_resultado, obter_ranking, salvar_progresso, carregar_progresso, resetar_progresso, resetar_resultados
from conteudos import conteudos_educacionais
from utils import logout, marcar_erro, limpar_erro

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Plataforma Educacional Segura")

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
largura = int(screen_width * 0.7)
altura = int(screen_height * 0.85)
app.geometry(f"{largura}x{altura}")

app.resizable(False, False)

indice_pergunta = 0
pontuacao = 0
label_pergunta = None
botoes_opcoes = []
quiz_atual = []
tema_atual = ""
barra_quiz = None

def limpar_tema(tema):
    return re.sub(r'[^a-zA-Z0-9_]', '', tema.lower())

frame_principal = ctk.CTkFrame(app)
frame_principal.pack(expand=True, fill="both")

frame_conteudo = ctk.CTkFrame(frame_principal)
frame_conteudo.pack(expand=True, fill="both")
frame_login = ctk.CTkFrame(frame_conteudo)
frame_login = ctk.CTkFrame(frame_conteudo, corner_radius=20, fg_color="#1e293b")
frame_login.pack(expand=True, fill="both", padx=200, pady=80)
frame_quiz = ctk.CTkScrollableFrame(frame_conteudo)
frame_conteudo_educacional = ctk.CTkScrollableFrame(frame_conteudo)

from auth import carregar_dados, salvar_dados, criptografar_senha, verificar_senha, salvar_usuario_atual, carregar_usuario_atual
from quiz import quizzes, salvar_resultado, obter_ranking, salvar_progresso, carregar_progresso, resetar_progresso
from conteudos import conteudos_educacionais
from utils import logout, marcar_erro, limpar_erro

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Plataforma Educacional Segura")


screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
largura = int(screen_width * 0.7)
altura = int(screen_height * 0.85)
app.geometry(f"{largura}x{altura}")

app.resizable(False, False)


frame_principal = ctk.CTkFrame(app)
frame_principal.pack(expand=True, fill="both")

frame_conteudo = ctk.CTkFrame(frame_principal)
frame_conteudo.pack(expand=True, fill="both")
frame_login = ctk.CTkFrame(frame_conteudo)
frame_login.pack(pady=50, padx=50, fill="both", expand=True)
frame_bem_vindo = ctk.CTkScrollableFrame(frame_conteudo)
frame_quiz = ctk.CTkScrollableFrame(frame_conteudo)
frame_conteudo_educacional = ctk.CTkScrollableFrame(frame_conteudo)

titulo = ctk.CTkLabel(frame_login, text="🧠 Plataforma Educacional", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=(30, 20))

campo_usuario = ctk.CTkEntry(frame_login, placeholder_text="Usuário", width=300, font=("Arial", 14))
campo_usuario.pack(pady=10)

campo_senha = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=300, font=("Arial", 14))
campo_senha.pack(pady=10)

campo_confirmar_senha = ctk.CTkEntry(frame_login, placeholder_text="Confirmar Senha", show="*", width=300, font=("Arial", 14))
campo_confirmar_senha.pack(pady=10)

resultado_login = ctk.CTkLabel(frame_login, text="", font=("Arial", 12))
resultado_login.pack(pady=10)

def validar_login(event=None):
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    dados = carregar_dados()

    limpar_erro(campo_usuario)
    limpar_erro(campo_senha)

    if not usuario:
        resultado_login.configure(text="⚠️ Informe o usuário.", text_color="orange")
        marcar_erro(campo_usuario)
        return

    if not senha:
        resultado_login.configure(text="⚠️ Informe a senha.", text_color="orange")
        marcar_erro(campo_senha)
        return

    if usuario not in dados:
        resultado_login.configure(text="⚠️ Usuário não encontrado.", text_color="orange")
        marcar_erro(campo_usuario)
    elif not verificar_senha(senha, dados[usuario]):
        resultado_login.configure(text="❌ Senha incorreta.", text_color="red")
        marcar_erro(campo_senha)
    else:
        salvar_usuario_atual(usuario)
        resultado_login.configure(text="✅ Login realizado com sucesso!", text_color="green")
        exibir_bem_vindo()

def cadastrar_usuario():
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    senha_confirma = campo_confirmar_senha.get()
    dados = carregar_dados()

    limpar_erro(campo_usuario)
    limpar_erro(campo_senha)
    limpar_erro(campo_confirmar_senha)

    if not usuario:
        resultado_login.configure(text="⚠️ Informe o usuário.", text_color="orange")
        marcar_erro(campo_usuario)
        return

    if not senha:
        resultado_login.configure(text="⚠️ Informe a senha.", text_color="orange")
        marcar_erro(campo_senha)
        return

    if len(senha) < 6:
        resultado_login.configure(text="⚠️ A senha deve ter pelo menos 6 caracteres.", text_color="orange")
        marcar_erro(campo_senha)
        return

    if not senha_confirma:
        resultado_login.configure(text="⚠️ Confirme a senha.", text_color="orange")
        marcar_erro(campo_confirmar_senha)
        return

    if senha != senha_confirma:
        resultado_login.configure(text="❌ Senhas não coincidem.", text_color="red")
        marcar_erro(campo_senha)
        marcar_erro(campo_confirmar_senha)
        return

    if usuario in dados:
        resultado_login.configure(text="⚠️ Usuário já existe.", text_color="red")
        marcar_erro(campo_usuario)
        return

    senha_hash = criptografar_senha(senha)
    if senha_hash:
        dados[usuario] = senha_hash.decode('utf-8')
        salvar_dados(dados)
        resultado_login.configure(text="✅ Cadastro realizado!", text_color="blue")
        
def exibir_conteudo_formatado(frame, tema):
    for widget in frame.winfo_children():
        widget.destroy()

    conteudo = conteudos_educacionais.get(tema, "Conteúdo não encontrado.")
    linhas = conteudo.strip().split("\n")

    ctk.CTkLabel(frame, text=f"📘 Tema: {tema.title()}", font=("Arial", 22, "bold"), text_color="#2563eb").pack(pady=(10, 10))

    em_codigo_python = False
    buffer_python = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        if linha.startswith("```python"):
            em_codigo_python = True
            buffer_python = []
            continue
        elif linha.startswith("```") and em_codigo_python:
            em_codigo_python = False
            bloco = ctk.CTkTextbox(frame, height=120, width=700)
            bloco.configure(font=("Courier", 12))
            bloco.pack(pady=10, padx=20)
            bloco.insert("0.0", "\n".join(buffer_python))
            bloco.configure(state="disabled")
            continue

        if em_codigo_python:
            buffer_python.append(linha)
            continue

        if re.match(r"^[0-9]+\.\s", linha):  
            ctk.CTkLabel(frame, text=linha, font=("Arial", 17, "bold"), anchor="w", justify="left").pack(anchor="w", padx=20, pady=(10, 0))
        elif linha.startswith("-") or linha.startswith("•"):
            ctk.CTkLabel(frame, text=linha, font=("Arial", 14), anchor="w", justify="left").pack(anchor="w", padx=40)
        elif 'Fim' in linha or 'Inicio' in linha or '<-' in linha or 'Escreva' in linha:
            bloco = ctk.CTkTextbox(frame, height=80, width=700)
            bloco.configure(font=("Courier", 12))
            bloco.pack(pady=10, padx=20)
            bloco.insert("0.0", linha)
            bloco.configure(state="disabled")
        else:
            ctk.CTkLabel(frame, text=linha, font=("Arial", 14), anchor="w", wraplength=750, justify="left").pack(anchor="w", padx=20)

estilos_temas = {
    "logica": {"icone": "🧠", "cor": "#facc15"},
    "python": {"icone": "🐍", "cor": "#10b981"},
    "lgpd": {"icone": "🛡️", "cor": "#f97316"},
    "sustentabilidade": {"icone": "🌱", "cor": "#22c55e"},
    "ciberseguranca": {"icone": "🔐", "cor": "#60a5fa"},
    "scratch": {"icone": "🎮", "cor": "#ec4899"},
}
    
def exibir_bem_vindo():
    frame_login.pack_forget()
    frame_quiz.pack_forget()
    frame_conteudo_educacional.pack_forget()

    for widget in frame_bem_vindo.winfo_children():
        widget.destroy()

    usuario = carregar_usuario_atual().get("usuario", "")
    progresso = carregar_progresso(usuario)

    label_bem_vindo = ctk.CTkLabel(
        frame_bem_vindo,
        text=f"👋 Olá, {usuario}!\n📚 Explore seu conhecimento com nossos temas interativos:",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#60a5fa",
        justify="center",
        wraplength=600
    )
    label_bem_vindo.pack(pady=30)

    def calcular_nota_final(usuario):
        try:
            with open("resultados.json", "r") as f:
                dados = json.load(f)
        except:
            return (0, 0, 0)

        resultados_usuario = dados.get(usuario, {})
        acertos_totais = 0
        total_perguntas = 0

        for tema, resultado in resultados_usuario.items():
            if isinstance(resultado, dict) and "pontuacao" in resultado:
                acertos_totais += resultado["pontuacao"]
                total_perguntas += resultado["total"]

        percentual = round((acertos_totais / total_perguntas) * 100) if total_perguntas > 0 else 0
        return (acertos_totais, total_perguntas, percentual)

    acertos, total, percentual = calcular_nota_final(usuario)
    texto_nota = f"📊 Desempenho Geral: {acertos}/{total} acertos ({percentual}%)"
    label_nota = ctk.CTkLabel(frame_bem_vindo, text=texto_nota, font=("Arial", 16), text_color="#4ade80")
    label_nota.pack(pady=(0, 20))

    
    frame_grid_temas = ctk.CTkFrame(frame_bem_vindo)
    frame_grid_temas.pack(pady=10, padx=30, fill="both", expand=True)

    temas_ordenados = list(reversed(list(conteudos_educacionais)))
    colunas = 3

    for i, tema in enumerate(temas_ordenados):
        progresso_tema = progresso.get(tema, {})
        acertos_tema = progresso_tema.get("acertos", 0)
        total_tema = progresso_tema.get("total", len(quizzes.get(tema, [])))
        completo = progresso_tema.get("completo", False)

        estilo = estilos_temas.get(tema, {"icone": "📘", "cor": "#3b82f6"})
        icone_tema = estilo["icone"]
        cor_tema = estilo["cor"]

        status = "✅" if completo and acertos_tema == total_tema else "🔄" if completo else "❌"
        texto_progresso = f"{icone_tema} {tema.title()}  {status} ({acertos_tema}/{total_tema})"
        card = ctk.CTkFrame(frame_grid_temas, corner_radius=12, fg_color="#0f172a")
        card.grid(row=i // colunas, column=i % colunas, padx=15, pady=15, sticky="nsew")

        label_tema = ctk.CTkLabel(card, text=texto_progresso, font=("Arial", 17, "bold"), text_color="#3b82f6")
        label_tema.pack(pady=(10, 4), anchor="w", padx=20)

        barra = ctk.CTkProgressBar(card, width=300, height=16, progress_color="#22c55e", corner_radius=10)
        barra.set(acertos_tema / total_tema if total_tema > 0 else 0)
        barra.pack(pady=(0, 10), padx=20)

        botoes = ctk.CTkFrame(card, fg_color="transparent")
        botoes.pack(pady=5, padx=20, anchor="w")

        ctk.CTkButton(botoes, text="📖 Ver Conteúdo", width=120, command=lambda t=tema: mostrar_conteudo_fixo(t)).pack(side="left", padx=5)
        ctk.CTkButton(botoes, text="▶️ Iniciar Quiz", width=120, command=lambda t=tema: iniciar_quiz(t)).pack(side="left", padx=5)

    for i in range(colunas):
        frame_grid_temas.grid_columnconfigure(i, weight=1)

    botao_ranking = ctk.CTkButton(
    frame_bem_vindo,
    text="🏆 Ver Ranking",
    width=300,
    height=45,
    font=ctk.CTkFont(size=15, weight="bold"),
    fg_color="#3b82f6",
    hover_color="#2563eb",
    command=mostrar_ranking
)
    botao_ranking.pack(pady=(20, 10))


    def confirmar_reset():
        popup = ctk.CTkToplevel(app)
        popup.title("Resetar Progresso")
        popup.geometry("300x150")
        popup.grab_set()

        label = ctk.CTkLabel(popup, text="Deseja realmente apagar seu progresso?", font=("Arial", 14))
        label.pack(pady=20)

        def sim():
            try:
                usuario = carregar_usuario_atual().get("usuario", "")
                resetar_progresso(usuario)
                resetar_resultados(usuario)
                popup.destroy()
                exibir_bem_vindo()
            except Exception as e:
                print(f"Erro ao resetar: {e}")
                popup.destroy()

        def nao():
            popup.destroy()

        botoes = ctk.CTkFrame(popup)
        botoes.pack(pady=10)

        ctk.CTkButton(botoes, text="Sim", command=sim).pack(side="left", padx=10)
        ctk.CTkButton(botoes, text="Não", command=nao).pack(side="left", padx=10)

    botao_reset = ctk.CTkButton(
    frame_bem_vindo,
    text="🗑️ Resetar Progresso",
    width=300,
    height=45,
    font=ctk.CTkFont(size=15, weight="bold"),
    fg_color="#ef4444",
    hover_color="#b91c1c",
    command=confirmar_reset
)
    botao_reset.pack(pady=10)

    botao_sair = ctk.CTkButton(
    frame_bem_vindo,
    text="⬅️ Sair",
    width=300,
    height=45,
    font=ctk.CTkFont(size=15, weight="bold"),
    fg_color="#6b7280",
    hover_color="#4b5563",
    command=confirmar_logout
)
    botao_sair.pack(pady=(10, 30))

    frame_bem_vindo.pack(expand=True, fill="both", padx=20, pady=20)

def mostrar_conteudo_fixo(tema):
    frame_bem_vindo.pack_forget()
    frame_quiz.pack_forget()
    frame_conteudo_educacional.pack(expand=True, fill="both", padx=20, pady=20)

    for widget in frame_conteudo_educacional.winfo_children():
        widget.destroy()

    tema_limpo = limpar_tema(tema)
    exibir_conteudo_formatado(frame_conteudo_educacional, tema_limpo)

    botoes_frame = ctk.CTkFrame(frame_conteudo_educacional)
    botoes_frame.pack(pady=10)

    btn_voltar = ctk.CTkButton(botoes_frame, text="⬅️ Voltar", command=voltar_para_bem_vindo)
    btn_voltar.pack(side="left", padx=10)

    btn_iniciar_quiz = ctk.CTkButton(botoes_frame, text="▶️ Começar Quiz", command=lambda: iniciar_quiz(tema_limpo))
    btn_iniciar_quiz.pack(side="left", padx=10)

def iniciar_quiz(tema):
    global indice_pergunta, pontuacao, label_pergunta, quiz_atual, tema_atual, barra_quiz, label_progresso
    indice_pergunta = 0
    pontuacao = 0
    tema_atual = limpar_tema(tema)
    quiz_atual = quizzes.get(tema_atual, [])

    frame_bem_vindo.pack_forget()
    frame_conteudo_educacional.pack_forget()

    for widget in frame_quiz.winfo_children():
        widget.destroy()

    label_pergunta = ctk.CTkLabel(frame_quiz, text="", font=("Arial", 16), wraplength=500)
    label_pergunta.pack(pady=20)

    
    label_progresso = ctk.CTkLabel(frame_quiz, text="Progresso: 0%", font=("Arial", 13), text_color="#22c55e")
    label_progresso.pack(pady=(10, 2))

    barra_quiz = ctk.CTkProgressBar(
        frame_quiz,
        width=400,
        height=20,
        progress_color="#22c55e",
        corner_radius=10,
        fg_color="#1e293b",
        border_color="#334155",
        border_width=1
    )
    barra_quiz.set(0)
    barra_quiz.pack(pady=(0, 20))

    exibir_pergunta()

    ctk.CTkButton(frame_quiz, text="⬅️ Voltar", command=voltar_para_bem_vindo).pack(pady=30)
    frame_quiz.pack(expand=True, fill="both", padx=20, pady=20)


def exibir_pergunta():
    global label_pergunta, botoes_opcoes, indice_pergunta, pontuacao
    for botao in botoes_opcoes:
        botao.destroy()
    botoes_opcoes.clear()

    if indice_pergunta < len(quiz_atual):
        pergunta = quiz_atual[indice_pergunta]
        label_pergunta.configure(text=pergunta["pergunta"])

        for opcao in pergunta["opcoes"]:
            botao = ctk.CTkButton(frame_quiz, text=opcao, command=lambda o=opcao: verificar_resposta(o))
            botao.pack(pady=5)
            botoes_opcoes.append(botao)
    else:
        usuario = carregar_usuario_atual().get("usuario", "")
        salvar_resultado(usuario, tema_atual, pontuacao)
        progresso_atual = salvar_progresso(usuario, tema_atual, pontuacao, len(quiz_atual))
        label_pergunta.configure(text=f"🏁 Fim do Quiz! Pontuação: {pontuacao}/{len(quiz_atual)}")
        exibir_bem_vindo()  

        reiniciar = ctk.CTkButton(frame_quiz, text="🔁 Reiniciar", command=lambda: iniciar_quiz(tema_atual))
        reiniciar.pack(pady=10)
        botoes_opcoes.append(reiniciar)

def verificar_resposta(opcao):
    global indice_pergunta, pontuacao
    if opcao == quiz_atual[indice_pergunta]["resposta"]:
        pontuacao += 1

    usuario = carregar_usuario_atual().get("usuario", "")
    salvar_progresso(usuario, tema_atual, pontuacao, indice_pergunta + 1)  

    indice_pergunta += 1
    if barra_quiz and len(quiz_atual) > 0:
        progresso = indice_pergunta / len(quiz_atual)
        barra_quiz.set(progresso)
        label_progresso.configure(text=f"Progresso: {round(progresso * 100)}%")
    exibir_pergunta()
    
def mostrar_ranking():
    ranking = obter_ranking(limpar_tema(tema_atual))
    texto = f"🏆 Ranking do tema: {tema_atual}\n\n"
    
    from datetime import datetime

    for i, (usuario, pont, total, perc, data_iso) in enumerate(ranking, 1):
        try:
            data_formatada = datetime.fromisoformat(data_iso).strftime("%d/%m/%Y %H:%M")
        except:
            data_formatada = data_iso

        if perc >= 90:
            status = "🏅 Excelente"
        elif perc >= 70:
            status = "👍 Bom"
        elif perc >= 50:
            status = "🟡 Razoável"
        else:
            status = "🔴 Precisa melhorar"

        tempo_medio = round(60 / total, 1) if total > 0 else "-"
        texto += (
            f"{i}º - 👤 {usuario}\n"
            f"   ✔️ {pont}/{total} acertos ({perc}%)\n"
            f"   📅 {data_formatada}\n"
            f"   ⏱️ Estimado: {tempo_medio}s por pergunta\n"
            f"   {status}\n\n"
        )

    popup = ctk.CTkToplevel(app)
    popup.title("Ranking")
    popup.geometry("420x320")

    label = ctk.CTkLabel(popup, text=texto, font=("Arial", 14), justify="left")
    label.pack(pady=20, padx=10)

    ctk.CTkButton(popup, text="Fechar", command=popup.destroy).pack(pady=10)

def voltar_para_bem_vindo():
        frame_quiz.pack_forget()
        frame_conteudo_educacional.pack_forget()
        frame_bem_vindo.pack(expand=True, fill="both", padx=20, pady=20)

def confirmar_logout():
    popup = ctk.CTkToplevel(app)
    popup.title("Confirmação de Logout")
    popup.geometry("350x150")
    popup.grab_set()

    label = ctk.CTkLabel(popup, text="Você tem certeza que deseja sair?", font=("Arial", 14))
    label.pack(pady=20, padx=20)

    def sim():
        popup.destroy()
        logout()
        voltar_login()

    def nao():
        popup.destroy()

    frame_botoes = ctk.CTkFrame(popup)
    frame_botoes.pack(pady=10)

    botao_sim = ctk.CTkButton(frame_botoes, text="Sim", width=80, command=sim)
    botao_sim.pack(side="left", padx=10)

    botao_nao = ctk.CTkButton(frame_botoes, text="Não", width=80, command=nao)
    botao_nao.pack(side="left", padx=10)

def voltar_login():
    logout()
    frame_bem_vindo.pack_forget()
    frame_quiz.pack_forget()
    frame_conteudo_educacional.pack_forget()
    campo_usuario.delete(0, ctk.END)
    campo_senha.delete(0, ctk.END)
    campo_confirmar_senha.delete(0, ctk.END)
    resultado_login.configure(text="")
    frame_login.pack(pady=50, padx=50, fill="both", expand=True)

    
botao_login = ctk.CTkButton(frame_login, text="🔐 Login", width=300, height=45, font=("Arial", 14), command=validar_login)
botao_login.pack(pady=(20, 10))

botao_cadastrar = ctk.CTkButton(frame_login, text="🆕 Cadastrar", width=300, height=45, font=("Arial", 14), fg_color="#6a5acd", hover_color="#483d8b", command=cadastrar_usuario)
botao_cadastrar.pack(pady=(0, 10))

app.bind("<Return>", lambda event: validar_login())
try:
    usuario = carregar_usuario_atual().get("usuario", "")
    if usuario:
        exibir_bem_vindo()
    else:
        frame_login.pack(pady=50, padx=50, fill="both", expand=True)
except Exception as e:
    print(f"Erro ao carregar sessão: {e}")
    frame_login.pack(pady=50, padx=50, fill="both", expand=True)


app.mainloop()
