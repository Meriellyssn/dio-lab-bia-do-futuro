import json
import pandas as pd
import streamlit as st
import google.generativeai as genai

# =================== CONFIGURAÇÃO GEMINI ===================

GOOGLE_API_KEY = "COLOQUE_SUA_CHAVE_API_AQUI"
genai.configure(api_key=GOOGLE_API_KEY)
MODELO = "gemini-3.5-flash" 

# =================== CONFIGURAÇÃO DA PÁGINA ===================
st.set_page_config(
    page_title="PoupAI - Assistente Financeiro",
    page_icon="💰",
    layout="wide", 
)

# =================== CARREGANDO DADOS ===================
@st.cache_data
def carregar_dados():
    try:
        
        perfil = json.load(open("./data/perfil_usuario.json", encoding="utf-8"))
        transacoes = pd.read_csv("./data/transacoes.csv")
        historico = pd.read_csv("./data/historico_atendimento.csv")
        dicas = json.load(open("./data/dicas_economia.json", encoding="utf-8"))
        return perfil, transacoes, historico, dicas
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar dados. Verifique a pasta 'data'. Detalhe: {e}")
        return {}, pd.DataFrame(), pd.DataFrame(), {}

perfil, transacoes, historico, dicas = carregar_dados()

# Calculando o progresso da meta para a interface
reserva_atual = perfil.get('reserva_emergencia_atual', 0)
meta_total = perfil.get('metas', [{'valor_necessario': 15000}])[0].get('valor_necessario', 15000)
valor_faltante = meta_total - reserva_atual

# =================== PAINEL LATERAL (SIDEBAR) ===================
with st.sidebar:
    st.title("📊 Painel do Cliente")
    st.write(f"**Nome:** {perfil.get('nome', 'Cliente')}")
    st.write(f"**Objetivo:** {perfil.get('objetivo_principal', 'Economizar')}")
    st.divider()
    st.metric("Reserva Atual", f"R$ {reserva_atual:,.2f}")
    st.metric("Meta Final", f"R$ {meta_total:,.2f}")
    st.metric("Falta Arrecadar", f"R$ {valor_faltante:,.2f}")

# =================== CONTEXTO E PROMPT ===================
context = f"""
DADOS DO CLIENTE:
- Nome: {perfil.get('nome', 'Cliente')}
- Renda Mensal: R$ {perfil.get('renda_mensal', 0):.2f}
- Objetivo Principal: {perfil.get('objetivo_principal', 'Economizar')}
- Reserva Atual: R$ {reserva_atual:.2f} | Meta: R$ {meta_total:.2f}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

DICAS DE ECONOMIA DISPONÍVEIS:
{json.dumps(dicas, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """Você é o PoupAI, um assistente financeiro acolhedor e encorajador.

OBJETIVO:
Analisar os gastos mensais do utilizador para ajudar a economizar para alcançar as suas metas financeiras.

REGRAS:
1. NUNCA recomende investimentos específicos ou ativos financeiros.
2. NUNCA julgue os gastos do utilizador. Seja sempre empático e foque na solução.
3. Use os dados de transações (extrato) fornecidos para dar exemplos personalizados de onde cortar gastos.
4. Baseie as suas sugestões de corte nas DICAS DE ECONOMIA fornecidas no contexto.
5. Se não souber algo ou for um pedido fora do escopo, admita educadamente: "Eu adoraria ajudar com isso, mas o meu foco é ajudar a organizar os seus gastos..."
6. Termine sempre a resposta com uma pergunta que incentive o utilizador a dar o próximo passo rumo à meta.
7. Responda de forma clara, concisa e amigável, evitando jargões financeiros complexos, com no maximo 3 parágrafos. Use uma linguagem simples e direta, adequada para o público em geral.
"""

# =================== CHAMAR GEMINI ===================
def perguntar(historico_mensagens):
    prompt_completo = f"CONTEXTO DO CLIENTE:\n{context}\n\nHISTÓRICO DA CONVERSA:\n"
    for msg in historico_mensagens:
        prompt_completo += f"{msg['role']}: {msg['content']}\n"
    
    try:
        # Configurando a inteligência do Gemini com o nosso System Prompt
        model = genai.GenerativeModel(
            model_name=MODELO,
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(prompt_completo)
        return response.text
    except Exception as e:
        return f"Desculpe, estou com problemas para me conectar ao Gemini. Detalhe técnico: {e}"

# =================== INTERFACE PRINCIPAL ===================
st.title("💰 PoupAI")
st.caption("O seu assistente financeiro focado em corte de gastos e metas!")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
    st.session_state.mensagens.append({
        "role": "assistant", 
        "content": f"Olá, {perfil.get('nome', 'Cliente')}! Faltam apenas R$ {valor_faltante:,.2f} para a sua meta. Como posso ajudar a organizar os seus gastos hoje?"
    })

for msg in st.session_state.mensagens:
    st.chat_message(msg["role"]).write(msg["content"])

if pergunta := st.chat_input("Digite sua pergunta ou dúvida financeira:"):
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)
    
    with st.spinner("PoupAI está analisando seus dados na nuvem..."):
        resposta = perguntar(st.session_state.mensagens)
        st.chat_message("assistant").write(resposta)
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})
