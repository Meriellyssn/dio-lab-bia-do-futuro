# Passo a passo de execução

## Configuração do Google Gemini

```bash
#1. Instale a biblioteca oficial do Google:
   Abra o seu terminal e rode o comando abaixo:
   
   pip install google-generativeai
#2.Gere a sua API Key (Chave de Acesso):
Acesse o [Google AI Studio](https://aistudio.google.com/), faça login com a sua conta do Google e crie uma chave de API gratuita.
#3. Insira a chave no código:
Abra o arquivo `app.py` na pasta `src` e substitua o texto `"COLOQUE_SUA_CHAVE_API_AQUI"` pela chave que você acabou de gerar.
```
---

## Código completo

Todo o código-fonte principal da aplicação está contido no arquivo `src/app.py`, que faz a leitura dos dados fictícios armazenados na pasta `data/`.

---

## Como rodar

Com a chave de API já configurada no código, siga os passos abaixo no terminal do seu sistema (PowerShell):

```bash
# 1. Instale as dependências necessárias (se ainda não as tiver)
pip install pandas streamlit

# 2. Execute a aplicação do Streamlit
python -m streamlit run .\src\app.py

```

Após rodar o comando, o seu navegador abrirá automaticamente com a interface do PoupAI.

---

## Evidência de Execução

<img width="1920" height="2026" alt="image" src="https://github.com/user-attachments/assets/d9337516-d962-403a-a335-8210bac2d5a8" />


```

```
