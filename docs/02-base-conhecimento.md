# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no PoupAI? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores, mantendo o tom de parceiro de jornada nas metas. |
| `perfil_usuario.json` | JSON | Personalizar o atendimento focado nos objetivos financeiros e metas do cliente (ex: reserva de emergência). |
| `dicas_economia.json` | JSON | Servir como um guia de conselhos práticos e validados para redução de gastos nas principais categorias do dia a dia. |
| `transacoes.csv` | CSV | Analisar o padrão de fluxo de caixa e identificar oportunidades de corte de gastos invisíveis. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Como o agente PoupAI foca em corte de gastos e organização, para se adaptar ao seu contexto resolvi substituir o produtos_financeiros.json por um novo arquivo dicas_economia.json. Essa mudança garante que o agente tenha insumos para sugerir dicas práticas de poupança diária e respeite rigidamente a regra de segurança de não atuar como consultor de investimentos.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos são carregados para a memória do sistema através de código em Python, utilizando a biblioteca pandas para ler as planilhas (CSVs) e a biblioteca nativa json para ler os arquivos de texto estruturado (JSONs).

```python
import pandas as pd
import json

perfil = json.load(open('../data/perfil_usuario.json'))
transacoes = pd.read_csv('../data/transacoes.csv')
historico = pd.read_csv('../data/historico.csv')
dicas = json.load(open('../data/dicas_economia.json'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar nesta primeira versão, os dados são "injetados" diretamente no prompt de sistema (Ctrl+C, Ctrl+V do conteúdo dos arquivos), garantindo que o agente PoupAI tenha todo o contexto antes de responder.
```text
DADOS DO CLIENTE E PERFIL:(data/perfil_usuario.json)
{
  "nome": "João Silva",
  "renda_mensal": 5000.00,
  "objetivo_principal": "Construir reserva de emergência",
  "reserva_emergencia_atual": 10000.00,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    }
  ]
}

TRANSAÇÕES DO CLIENTE:(data/transacoes.csv)
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida

HISTORICO DE ATENDIMENTO DO CLIENTE:(data/historico_atendimento.csv)
data,canal,tema,resumo,resolvido
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim

DICAS DE ECONOMIA:(data/dicas_economia.json)
[
  {
    "categoria_alvo": "alimentacao",
    "gatilho": "Gasto excessivo com delivery ou restaurantes",
    "dica_pratica": "Que tal testar a regra do '1 por 1'? Para cada refeição pedida por aplicativo, tente preparar a próxima em casa."
  },
  {
    "categoria_alvo": "transporte",
    "gatilho": "Gastos frequentes com aplicativos de mobilidade em trajetos curtos.",
    "dica_pratica": "Que tal substituir 2 corridas curtas na semana por uma caminhada? Além de economizar, faz bem para a saúde!"
  }
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto abaixo sintetiza as informações mais relevantes da base de conhecimento, otimizando o consumo de tokens e garantindo que o agente PoupAI foque no corte de gastos para atingir as metas.

```text

DADOS DO CLIENTE:
- Nome: João Silva
- Renda Mensal: R$ 5.000,00
- Objetivo: Construir reserva de emergência 
- Reserva atual: R$ 10.000,00 (Meta final: R$ 15.000,00)

RESUMO DE GASTOS (Mês Atual):
- Moradia: R$ 1.380,00
- Alimentação: R$ 570,00
- Transporte: R$ 295,00
- Saúde: R$ 188,00
- Lazer: R$ 55,90

DICAS DE ECONOMIA DISPONÍVEIS:
- Alimentação (Gasto excessivo): Testar a regra do '1 por 1' no delivery (preparar a próxima refeição em casa).
- Transporte (Gastos frequentes): Substituir 2 corridas curtas na semana por uma caminhada.
```
