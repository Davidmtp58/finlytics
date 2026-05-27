# Finlytics 💰

🌐 **App no ar:** [finlytics2.streamlit.app](https://finlytics2.streamlit.app)

O **Finlytics** é um assistente financeiro pessoal desenvolvido em Python para analisar extratos bancários, categorizar transações e apresentar um resumo financeiro simples e visual.

O projeto aceita extratos em **CSV, PDF e imagem** e combina regras locais com IA generativa via Gemini para classificar transações bancárias brasileiras de forma mais inteligente.

---

## 1. Objetivo do Projeto

O objetivo do Finlytics é facilitar a análise de gastos pessoais a partir de um extrato bancário.

Com ele, o usuário pode:

- Enviar um extrato em CSV, PDF ou imagem;
- Filtrar por período/mês;
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
| Linguagem | Python | ✅ Implementado | Ecossistema maduro para análise de dados e IA, permitindo construir desde a leitura do arquivo até a interface e integração com LLM usando a mesma linguagem. |
| Manipulação de dados | pandas | ✅ Implementado | Utilizado para leitura do extrato, conversão de datas, cálculo de receitas, despesas, saldo e agrupamento por categoria. |
| Entrada de dados | CSV, PDF e imagem | ✅ Implementado | CSV é lido diretamente; PDF e imagem são interpretados pelo Gemini, que extrai as transações. Isso permite usar extratos no formato que o banco entrega. |
| Interface | Streamlit | ✅ Implementado | Permite criar uma interface visual em Python, com upload de CSV, PDF e imagem, tabela editável, métricas financeiras e gráfico de gastos. |
| IA Generativa | Gemini API | ✅ Implementado | Usado em dois pontos: extrair transações de PDF/imagem e classificar transações que não foram identificadas pelas regras locais. As regras locais reduzem chamadas à API e deixam o projeto mais eficiente. |
| Segurança | `.env` e `.env.example` | ✅ Implementado | A chave real da API fica fora do GitHub no arquivo `.env`, enquanto o `.env.example` mostra como configurar o projeto. |

---

## 3. Demonstração

A aplicação está disponível online em: **[finlytics2.streamlit.app](https://finlytics2.streamlit.app)**

O Finlytics possui uma interface visual construída com Streamlit.

Na aplicação, o usuário pode:

- Enviar um extrato em CSV, PDF ou imagem;
- Filtrar por período/mês (ou ver tudo consolidado);
- Visualizar as transações do mês;
- Corrigir categorias manualmente na tabela;
- Ver receitas, despesas e saldo do mês;
- Visualizar o Top 3 categorias de gasto em gráfico.

A interface foi pensada para ser simples, direta e acessível para pessoas que não querem depender de planilhas manuais.

---

## 4. Destaque de Engenharia: The Hard Part

O Finlytics tem dois destaques de engenharia, ambos apoiados em IA generativa.

### 4.1. Classificação híbrida (regra → IA → usuário)

O principal desafio técnico foi criar uma classificação de transações que fosse útil sem depender totalmente de IA. A solução foi um pipeline híbrido em cascata:

1. Primeiro, o sistema tenta classificar a transação usando regras locais baseadas em palavras-chave.
2. Se a categoria não for encontrada, a transação é enviada ao Gemini, que retorna apenas uma categoria válida da lista.
3. Se o Gemini falhar (sem internet, cota excedida, etc.), o sistema retorna "Outros" automaticamente, sem derrubar a aplicação.
4. O usuário ainda pode corrigir manualmente a categoria na interface.

Esse desenho evita chamadas desnecessárias à API, reduz custo, melhora a velocidade e mantém controle sobre as categorias possíveis.

Exemplos reais:

```text
IFOOD RESTAURANTE      -> regra local            -> Alimentação
PADARIA DOCE PÃO       -> regra não achou -> Gemini -> Alimentação
ACADEMIA SMART FIT     -> regra não achou -> Gemini -> Fitness
CONTA DE LUZ ENERGISA  -> regra não achou -> Gemini -> Outros
```

### 4.2. Extração de documentos via Gemini multimodal

Para aceitar PDF e imagem, o Finlytics usa o Gemini multimodal: o documento é enviado ao modelo, que "lê" o extrato e devolve as transações estruturadas em JSON. O JSON é então convertido em DataFrame e passa pelo mesmo pipeline de classificação.

```text
PDF/imagem -> Gemini -> JSON -> DataFrame -> classificação
```

Isso permite que o usuário envie o extrato no formato que o banco entrega, sem precisar montar um CSV manualmente.

---

## 5. Funcionalidades

Atualmente, o Finlytics permite:

- Upload de extrato bancário em CSV, PDF ou imagem;
- Extração de transações de PDF e imagem via Gemini multimodal;
- Leitura e tratamento dos dados com pandas;
- Classificação automática das transações (regra local + Gemini como fallback);
- Categorias suportadas: Alimentação, Transporte, Streaming, Saúde, Fitness, Salário, Entrada Diversa e Outros;
- Edição manual das categorias na interface;
- Filtro por mês ou visualização consolidada;
- Cálculo de receitas, despesas e saldo;
- Exibição do Top 3 categorias de gasto;
- Formatação de valores e datas no padrão brasileiro (R$ 1.234,56 e dd/mm/aaaa);
- Interface visual com Streamlit;
- Configuração segura da chave da API com `.env`.

---

## 6. Instruções de Instalação e Uso

### Pré-requisitos

- Python 3.12 ou superior;
- Git;
- Chave da API Gemini criada no Google AI Studio (obrigatória para leitura de PDF/imagem e para a classificação via IA).

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

Ao executar a interface, o usuário pode enviar um arquivo CSV, PDF ou imagem e visualizar:

- Transações categorizadas;
- Receitas, despesas e saldo do mês;
- Top 3 categorias de gasto;
- Possibilidade de filtrar por mês e corrigir categorias manualmente.

---

## 7. Estrutura do Projeto

```text
finlytics/
│
├── app.py
├── finlytics.py
├── relatorio_financeiro.py
├── extrato_exemplo.csv
├── extrato_bancario_abril_2026.pdf
├── EXTRATO_TESTE.PNG
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
| `finlytics.py` | Contém a lógica principal de leitura, extração, categorização e cálculos. |
| `relatorio_financeiro.py` | Executa uma análise simples pelo terminal. |
| `extrato_exemplo.csv` | Arquivo CSV de exemplo para testar o projeto. |
| `extrato_bancario_abril_2026.pdf` | Exemplo de extrato em PDF para testar a extração. |
| `EXTRATO_TESTE.PNG` | Exemplo de extrato em imagem para testar a extração. |
| `.env.example` | Modelo para configuração da chave da API Gemini. |
| `requirements.txt` | Lista de dependências do projeto. |

---

## 8. Roadmap

O Finlytics está sendo construído em fases. Abaixo estão os próximos passos para evoluir o MVP.

### Curto prazo

- Implementar cache para categorias já classificadas pela IA (evitar chamadas repetidas);
- Migrar da biblioteca `google-generativeai` para `google-genai` (a antiga foi descontinuada);
- Criar validações para diferentes formatos de CSV;
- Melhorar mensagens de erro para arquivos inválidos.

### Médio prazo

- Reclassificação automática ao editar a descrição na tabela;
- Filtro por intervalo de datas personalizado;
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
- Integração com API de IA generativa (Gemini);
- Engenharia de prompt para classificação e extração de dados;
- Uso de JSON para estruturar respostas da IA;
- Conceito de `mime_type` para enviar PDF e imagem ao modelo;
- Gemini multimodal (leitura de documentos);
- Organização de um projeto Python em módulos;
- Versionamento com Git e GitHub;
- Construção de um MVP com foco em evolução incremental.

---

## 10. Autor

Desenvolvido por **David Mangueira**.

Este projeto faz parte da minha jornada de aprendizado em Dados, Python e Inteligência Artificial aplicada a produtos reais.