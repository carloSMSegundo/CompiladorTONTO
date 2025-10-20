# 🧠 Analisador Léxico para a Linguagem TONTO

Este é um projeto de **Analisador Léxico** para a **Textual Ontology Language (TONTO)**, desenvolvido como parte da disciplina de **Compiladores**. O objetivo é reconhecer os componentes léxicos da linguagem — como **palavras reservadas**, **estereótipos**, **símbolos** e **convenções de nomenclatura** — e gerar uma **tabela de símbolos** como saída.

O analisador foi implementado em **Python**, utilizando a biblioteca **PLY**, uma reimplementação das ferramentas **Lex** e **Yacc**.

---

## 🚀 Funcionalidades

- Reconhecimento de Tokens: identifica estereótipos de classe, estereótipos de relação, palavras reservadas e símbolos especiais.  
- Validação de Nomenclatura: aplica convenções para classes, relações, instâncias e novos tipos de dados.  
- Tratamento de Erros: captura erros léxicos e fornece mensagens claras com a linha do erro e sugestões de correção.  
- Geração de Saídas: cria uma tabela de símbolos detalhada em múltiplos formatos (.txt, .csv, .html) e relatório de erros.

---

## 🧠 Tecnologias utilizadas

- Python 3.x  
- [PLY](http://www.dabeaz.com/ply/)

---

## 🤔 Como utilizar?

### 1️⃣ Configuração do Ambiente

1. Criar um ambiente virtual na raiz do projeto:

<pre>python -m venv venv</pre>

2. Ativar o ambiente virtual:

**Windows (Git Bash):**

<pre>source venv/bin/activate</pre>

**Windows (WSL):**

<pre>source venv/bin/activate</pre>

**Linux/macOS:**

<pre>source venv/bin/activate.fish</pre>

3. Instalar dependências:

<pre>pip install -r requirements.txt</pre>

---

### 2️⃣ Executando o Analisador

Para analisar um arquivo `.tonto`, utilize:

<pre>python src/main.py tests/exemplo1.tonto</pre>

---

### 3️⃣ Verificando a Saída

Os resultados serão salvos na pasta `outputs/`:

- `tabela_de_simbolos.txt` — tabela de símbolos em formato texto.  
- `tabela_de_simbolos.csv` — tabela de símbolos em formato CSV.  
- `tabela_de_simbolos.html` — tabela de símbolos em formato HTML.  
- `erros_lexicos.txt` — relatório de erros léxicos encontrados.

---

### 4️⃣ Possíveis Problemas
Verifique se instalou corretamente as dependências
(Passo 3)
Caso tenha algum problema, verifique sua versão do Python
**Windows WSL:**
<pre>sudo apt install python3.12-venv -y</pre>
Em seguida
<pre>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
</pre>
Depois, tente rodar novamente o projeto.

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais na disciplina de **Compiladores**.
