import json
import os
import re

CAMINHO_RESULTADOS = 'resultados.json'
CAMINHO_PROGRESSO = 'progresso.json'

def limpar_tema(tema):
    return re.sub(r'[^a-zA-Z0-9_]', '', tema.lower())

quizzes = {
    "logica": [
        {"pergunta": "Qual é o principal objetivo de um algoritmo?", "opcoes": ["Desenhar interfaces", "Resolver um problema", "Executar comandos aleatórios", "Criar imagens"], "resposta": "Resolver um problema"},
        {"pergunta": "O que uma estrutura condicional faz?", "opcoes": ["Executa repetidamente", "Compara valores e toma decisões", "Armazena dados", "Interrompe o programa"], "resposta": "Compara valores e toma decisões"},
        {"pergunta": "Qual é a estrutura usada para repetir uma ação?", "opcoes": ["Função", "Condicional", "Laço de repetição", "Algoritmo"], "resposta": "Laço de repetição"},
        {"pergunta": "O que é um pseudocódigo?", "opcoes": ["Linguagem de máquina", "Linguagem visual", "Descrição informal de algoritmos", "Código compilado"], "resposta": "Descrição informal de algoritmos"},
        {"pergunta": "Qual é a principal vantagem do uso de fluxogramas?", "opcoes": ["Substituir código", "Melhorar desempenho", "Visualizar a lógica", "Executar mais rápido"], "resposta": "Visualizar a lógica"}
    ],
    "python": [
        {"pergunta": "Qual dos seguintes é um tipo de dado em Python?", "opcoes": ["Integer", "Float", "Boolean", "Todos os anteriores"], "resposta": "Todos os anteriores"},
        {"pergunta": "Qual comando é usado para criar uma função em Python?", "opcoes": ["function", "def", "create", "fun"], "resposta": "def"},
        {"pergunta": "Como adicionamos um item a uma lista em Python?", "opcoes": ["lista.add()", "lista.push()", "lista.insert()", "lista.append()"], "resposta": "lista.append()"},
        {"pergunta": "Qual é a saída de print(type(5.0))?", "opcoes": ["<class 'float'>", "<class 'int'>", "<class 'str'>", "Erro"], "resposta": "<class 'float'>"},
        {"pergunta": "Qual estrutura é usada para armazenar pares chave-valor em Python?", "opcoes": ["Lista", "Tupla", "Dicionário", "Set"], "resposta": "Dicionário"}
    ],
    "scratch": [
        {"pergunta": "Qual é o principal benefício de usar o Scratch?", "opcoes": ["Executar códigos em C", "Aprender lógica de programação de forma visual", "Criar planilhas", "Executar comandos em terminal"], "resposta": "Aprender lógica de programação de forma visual"},
        {"pergunta": "Como os comandos são organizados no Scratch?", "opcoes": ["Em pastas", "Em tabelas", "Em blocos encaixáveis", "Em arquivos .py"], "resposta": "Em blocos encaixáveis"},
        {"pergunta": "Para que serve o bloco 'esperar' no Scratch?", "opcoes": ["Repetir ações", "Mover personagens", "Controlar tempo entre ações", "Mudar aparência"], "resposta": "Controlar tempo entre ações"},
        {"pergunta": "O que o bloco 'quando bandeira verde clicada' faz?", "opcoes": ["Termina o projeto", "Espera por eventos", "Inicia o programa", "Salva o código"], "resposta": "Inicia o programa"},
        {"pergunta": "Qual bloco permite repetir ações continuamente?", "opcoes": ["Esperar", "Repetir para sempre", "Mude o fundo", "Se então"], "resposta": "Repetir para sempre"}
    ],
    "lgpd": [
        {"pergunta": "Qual o principal objetivo da LGPD?", "opcoes": ["Proteger o meio ambiente", "Regular o uso de dados pessoais", "Reduzir impostos", "Controlar redes sociais"], "resposta": "Regular o uso de dados pessoais"},
        {"pergunta": "Qual destes é um direito do titular de dados?", "opcoes": ["Ser promovido no trabalho", "Acesso aos dados", "Anular multas", "Escolher senhas para outros"], "resposta": "Acesso aos dados"},
        {"pergunta": "O que a LGPD exige quanto à segurança?", "opcoes": ["Segurança é opcional", "É responsabilidade apenas da polícia", "Deve haver medidas de proteção de dados", "Nenhuma exigência específica"], "resposta": "Deve haver medidas de proteção de dados"},
        {"pergunta": "Qual entidade é responsável por fiscalizar a LGPD?", "opcoes": ["Receita Federal", "Polícia Federal", "ANPD", "STF"], "resposta": "ANPD"},
        {"pergunta": "O que é considerado dado sensível segundo a LGPD?", "opcoes": ["E-mail comercial", "Telefone residencial", "Opinião política", "Endereço de trabalho"], "resposta": "Opinião política"}
    ],
    "ciberseguranca": [
        {"pergunta": "O que é phishing?", "opcoes": ["Um tipo de firewall", "Ataque para roubo de dados via engano", "Antivírus avançado", "Proteção contra hackers"], "resposta": "Ataque para roubo de dados via engano"},
        {"pergunta": "Qual é uma boa prática de segurança?", "opcoes": ["Usar a mesma senha em tudo", "Desligar o antivírus", "Clicar em todos os links", "Atualizar os sistemas"], "resposta": "Atualizar os sistemas"},
        {"pergunta": "Engenharia social é:", "opcoes": ["Um tipo de rede de computadores", "Tentativa de manipular pessoas para obter dados", "Software de construção", "Aplicativo de segurança"], "resposta": "Tentativa de manipular pessoas para obter dados"},
        {"pergunta": "Qual destas ações é segura?", "opcoes": ["Compartilhar senhas com colegas", "Usar autenticação de dois fatores", "Salvar senhas em post-its", "Desligar o antivírus"], "resposta": "Usar autenticação de dois fatores"},
        {"pergunta": "O que é um antivírus?", "opcoes": ["Programa que acelera o PC", "Firewall", "Software para detectar e remover malware", "Aplicativo para editar vídeos"], "resposta": "Software para detectar e remover malware"}
    ],
    "sustentabilidade": [
        {"pergunta": "O que é sustentabilidade digital?", "opcoes": ["Instalar mais apps", "Usar muita energia", "Minimizar o impacto ambiental da tecnologia", "Fazer backups automáticos"], "resposta": "Minimizar o impacto ambiental da tecnologia"},
        {"pergunta": "Qual dessas é uma prática sustentável?", "opcoes": ["Deixar o PC ligado sempre", "Jogar eletrônicos no lixo comum", "Reciclar eletrônicos", "Imprimir tudo em papel"], "resposta": "Reciclar eletrônicos"},
        {"pergunta": "Como economizar energia na tecnologia?", "opcoes": ["Manter o brilho máximo", "Desligar o que não estiver usando", "Deixar todos os aparelhos ligados", "Aumentar a velocidade do Wi-Fi"], "resposta": "Desligar o que não estiver usando"},
        {"pergunta": "Qual atitude reduz o consumo de recursos naturais?", "opcoes": ["Comprar novos eletrônicos sempre", "Reutilizar equipamentos", "Jogar fora rapidamente", "Usar softwares pesados"], "resposta": "Reutilizar equipamentos"},
        {"pergunta": "O que é TI Verde?", "opcoes": ["Estilo de computador", "Software para gamers", "Prática sustentável na tecnologia", "Tipo de rede de internet"], "resposta": "Prática sustentável na tecnologia"}
    ]
}

from datetime import datetime

def salvar_resultado(usuario, tema, pontuacao):
    tema = limpar_tema(tema)
    resultados = {}
    if os.path.exists(CAMINHO_RESULTADOS):
        with open(CAMINHO_RESULTADOS, 'r') as f:
            resultados = json.load(f)

    if usuario not in resultados:
        resultados[usuario] = {}

    resultados[usuario][tema] = {
        "pontuacao": pontuacao,
        "total": len(quizzes[tema]),
        "data": datetime.now().isoformat()
    }

    with open(CAMINHO_RESULTADOS, 'w') as f:
        json.dump(resultados, f, indent=4)

def obter_ranking(tema):
    tema = limpar_tema(tema)
    if not os.path.exists(CAMINHO_RESULTADOS):
        return []

    with open(CAMINHO_RESULTADOS, 'r') as f:
        resultados = json.load(f)

    ranking = []
    for u, temas in resultados.items():
        if tema in temas:
            dados = temas[tema]
            pont = dados.get("pontuacao", 0)
            total = dados.get("total", 1)
            data = dados.get("data", "-")
            perc = round((pont / total) * 100)
            ranking.append((u, pont, total, perc, data))

    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:5]

def salvar_progresso(usuario, tema, acertos, total):
    tema = limpar_tema(tema)
    progresso = {}
    if os.path.exists(CAMINHO_PROGRESSO):
        with open(CAMINHO_PROGRESSO, 'r') as f:
            progresso = json.load(f)

    if usuario not in progresso:
        progresso[usuario] = {}

    progresso[usuario][tema] = {
        "acertos": acertos,
        "total": total,
        "completo": True
    }

    with open(CAMINHO_PROGRESSO, 'w') as f:
        json.dump(progresso, f, indent=4)

    return progresso[usuario]

def carregar_progresso(usuario):
    if os.path.exists(CAMINHO_PROGRESSO):
        with open(CAMINHO_PROGRESSO, 'r') as f:
            progresso = json.load(f)
        return progresso.get(usuario, {})
    return {}

def resetar_progresso(usuario):
    if not os.path.exists(CAMINHO_PROGRESSO):
        return
    with open(CAMINHO_PROGRESSO, 'r') as f:
        progresso = json.load(f)

    if usuario in progresso:
        del progresso[usuario]

    with open(CAMINHO_PROGRESSO, 'w') as f:
        json.dump(progresso, f, indent=4)
def resetar_resultados(usuario):
    if not os.path.exists(CAMINHO_RESULTADOS):
        return
    with open(CAMINHO_RESULTADOS, 'r') as f:
        resultados = json.load(f)

    if usuario in resultados:
        del resultados[usuario]

    with open(CAMINHO_RESULTADOS, 'w') as f:
        json.dump(resultados, f, indent=4)
