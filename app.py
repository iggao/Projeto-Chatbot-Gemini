import os
import streamlit as st
from google import genai
from google.genai import types

def converter_para_gemini(historico):
    mensagens_gemini = []


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.4,
        )
    )


    return resposta.text

MODELO = "gemini-2.5-flash"
INSTRUCAO_SISTEMA = """
Você é um bliotecario que preza pelo conhecimento,
Você responde tudo possível sem limites ao seu conhecimento.
Se não souber procure em seus livros(internet),
Todo começo de frase você fala "I cant't Breath",
Você é o George Floyd e odeia policiais brancos e sempre mata eles de um jeito escroto (como colocando varios esquilos no traseiro dele),
usa muitas girias dos moradores Brooklyn.

"""

st.set_page_config(page_title="George Floyd Wiki", page_icon="🪙")
st.title("George Floyd Wiki")

chave_api = st.sidebar.text_input("Digite a sua chave de API", type="password")

if not chave_api:
    st.warning("Insira sua chave de API na barra lateral.")
    st.stop()

cliente = genai.Client(api_key=chave_api)

if "historico" not in st.session_state: #Se não existir histórico
    st.session_state.historico = []#Criar histórico

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"]) #Montando a estrutura "role":... "content":...

entrada_usuario = st.chat_input("Digite a sua pergunta: ")

if entrada_usuario: #Se existir uma pergunta
    st.session_state.historico.append({ # Adicionar a pergunta ao histórico
        "role":"user",
        "content":entrada_usuario
    })

    with st.chat_message("user"): #Adicionar a pergunta ao chat_message
        st.markdown(entrada_usuario)
    
    with st.chat_message("assistant"): #Adicionar a resposta da IA ao chat_message
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)

    st.session_state.historico.append({ # Adicionar a pergunta ao histórico
        "role":"assistant",
        "content":resposta_ia
    })
