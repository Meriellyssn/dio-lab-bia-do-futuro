# Passo a passo de execução

##Setup do Ollama

```bash
#1. Instalar o Ollama (ollama.com)
#2. Baixar um modulo leve
ollama pull gpt-oss:20b

#Testa se funciona
ollama run gpt-oss "Olá!"

```

##Código completo
Todo código-fonte esta no arquivo `app.py`

##Como rodar
```bash
#1. Instalar dependecias
pip install -r requirements.txt

#2. Garantir que o Ollama está rodando
ollama serve

#3. Rodar a aplicação
streamlit run .\src\app.py
```
