# Finlytics 💰

O **Finlytics** é um assistente financeiro pessoal desenvolvido em Python para analisar extratos bancários em CSV, categorizar transações e apresentar um resumo financeiro simples e visual.

O projeto combina regras locais com IA generativa via Gemini para classificar transações bancárias brasileiras de forma mais inteligente.

---

## 1. Objetivo do Projeto

O objetivo do Finlytics é facilitar a análise de gastos pessoais a partir de um extrato bancário.

Com ele, o usuário pode:

- Enviar um extrato em CSV;
- Visualizar as transações do mês;
- Classificar automaticamente receitas e despesas;
- Corrigir categorias manualmente;
- Ver o total de receitas, despesas e saldo;
- Identificar as principais categorias de gasto.

---

## 2. Arquitetura e Decisões Técnicas

Cada escolha técnica deste projeto foi feita com foco em três critérios: velocidade de entrega no MVP, clareza do pipeline e caminho natural para evoluir com IA.

| Camada | Escolha | Status | Por que escolhi? |
|---|---|---|---|
| Linguagem | Python | ✅ Implementado | Ecossistema maduro para análise de dados e IA, permitindo construir desde a leitura do CSV até a interface e integração com LLM usando a mesma linguagem. |
| Manipulação de dados | pandas | ✅ Implementado | Utilizado para leitura do extrato, conversão de datas, cálculo de receitas, despesas, saldo e agrupamento por categoria. |
| Entrada de dados | CSV | ✅ Implementado | Formato simples e acessível para simular extratos bancários sem depender de integração bancária real nesta fase do MVP. |
| Interface | Streamlit | ✅ Implementado | Permite criar uma interface visual em Python, com upload de CSV, tabela editável, métricas financeiras e gráfico de gastos. |
| IA Generativa | Gemini API | ✅ Implementado | Usado como fallback para categorizar transações que não foram identificadas pelas regras locais. Isso reduz chamadas à API e deixa o projeto mais eficiente. |
| Segurança | `.env` e `.env.example` | ✅ Implementado | A chave real da API fica fora do GitHub no arquivo `.env`, enquanto o `.env.example` mostra como configurar o projeto. |

---

## 3. Demonstração

O Finlytics possui uma interface visual construída com Streamlit.

Na aplicação, o usuário pode:

- Enviar um extrato em CSV;
- Visualizar as transações do mês;
- Corrigir categorias manualmente na tabela;
- Ver receitas, despesas e saldo do mês;
- Visualizar o Top 3 categorias de gasto em gráfico.

A interface foi pensada para ser simples, direta e acessível para pessoas que não querem depender de planilhas manuais.

---

## 4. Destaque de Engenharia: The Hard Part

O principal desafio técnico do Finlytics foi criar uma classificação de transações que fosse útil sem depender totalmente de IA.

A solução adotada foi um pipeline híbrido:

1. Primeiro, o sistema tenta classificar a transação usando regras locais baseadas em palavras-chave.
2. Se a categoria não for encontrada, a transação é enviada para o Gemini.
3. O Gemini retorna apenas uma categoria válida.
4. O usuário ainda pode corrigir manualmente a categoria na interface.

Esse desenho evita chamadas desnecessárias para a API, reduz custo, melhora a velocidade do sistema e mantém controle sobre as categorias possíveis.

Exemplo:

```text
IFOOD RESTAURANTE -> regra local -> Alimentação
PADARIA SAO JOSE -> Gemini -> Alimentação
```

---

## 5. Funcionalidades

Atualmente, o Finlytics permite:

- Upload de extrato bancário em CSV;
- Leitura e tratamento dos dados com pandas;
- Classificação automática das transações;
- Uso de regras locais para categorias conhecidas;
- Uso do Gemini como fallback para categorias não mapeadas;
- Edição manual das categorias na interface;
- Cálculo de receitas, despesas e saldo;
- Exibição do Top 3 categorias de gasto;
- Interface visual com Streamlit;
- Configuração segura da chave da API com `.env`.

---

## 6. Instruções de Instalação e Uso

### Pré-requisitos

- Python 3.12 ou superior;
- Git;
- Chave da API Gemini criada no Google AI Studio.

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Davidmtp58/finlytics.git
cd finlytics

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### Configuração da API Gemini

Crie um arquivo chamado `.env` na raiz do projeto.

Use o arquivo `.env.example` como referência:

```env
GEMINI_API_KEY=sua_chave_aqui
```

No arquivo `.env`, substitua `sua_chave_aqui` pela sua chave real da API Gemini.

> Importante: o arquivo `.env` não deve ser enviado para o GitHub.

### Executando a interface

```bash
streamlit run app.py
```

### Executando o relatório no terminal

```bash
python relatorio_financeiro.py
```

### O que esperar

Ao executar a interface, o usuário pode enviar um arquivo CSV e visualizar:

- Transações categorizadas;
- Receitas;
- Despesas;
- Saldo do mês;
- Top 3 categorias de gasto;
- Possibilidade de corrigir categorias manualmente.

---

## 7. Estrutura do Projeto

```text
finlytics/
│
├── app.py
├── finlytics.py
├── relatorio_financeiro.py
├── extrato_exemplo.csv
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── venv/
```

### Principais arquivos

| Arquivo | Descrição |
|---|---|
| `app.py` | Interface visual do projeto em Streamlit. |
| `finlytics.py` | Contém a lógica principal de leitura, categorização e cálculos. |
| `relatorio_financeiro.py` | Executa uma análise simples pelo terminal. |
| `extrato_exemplo.csv` | Arquivo de exemplo para testar o projeto. |
| `.env.example` | Modelo para configuração da chave da API Gemini. |
| `requirements.txt` | Lista de dependências do projeto. |

---

## 8. Roadmap

O Finlytics está sendo construído em fases. Abaixo estão os próximos passos para evoluir o MVP.

### Curto prazo

- Melhorar a visualização do gráfico de categorias;
- Implementar cache para categorias classificadas pela IA;
- Adicionar novos exemplos de extrato CSV;
- Criar validações para diferentes formatos de CSV;
- Melhorar mensagens de erro para arquivos inválidos.

### Médio prazo

- Suporte a PDF de extrato bancário;
- Entrada manual de transações;
- Persistência em SQLite para histórico multi-mês;
- Chat em linguagem natural com os próprios dados.

### Longo prazo

- Integração com Open Finance via Belvo ou Pluggy;
- Módulo de investimentos;
- Recomendações financeiras personalizadas com IA;
- Modelo freemium com recursos avançados.

---

## 9. Aprendizados

Durante o desenvolvimento deste projeto, foram praticados conceitos como:

- Manipulação de dados com pandas;
- Criação de interface com Streamlit;
- Uso de variáveis de ambiente com `.env`;
- Integração com API de IA generativa;
- Organização de um projeto Python;
- Versionamento com Git e GitHub;
- Construção de um MVP com foco em evolução incremental.

---

## 10. Autor

Desenvolvido por **David Mangueira**.

Este projeto faz parte da minha jornada de aprendizado em Dados, Python e Inteligência Artificial aplicada a produtos reais.