# 🧠 Analisador Léxico, Sintático e Semântico para a Linguagem TONTO

Este é um projeto de **Analisador Léxico, Sintático e Semântico** para a **Textual Ontology Language (TONTO)**, desenvolvido como parte da disciplina de **Compiladores**. O objetivo é reconhecer os componentes léxicos, verificar a corretude gramatical e validar a estrutura lógica (semântica) das ontologias, gerando relatórios detalhados.

O analisador foi implementado em **Python**, utilizando a biblioteca **PLY**, uma reimplementação das ferramentas **Lex** e **Yacc**.

---

## 🚀 Funcionalidades

### Análise Léxica
- **Reconhecimento de Tokens:** identifica estereótipos de classe, estereótipos de relação, palavras reservadas e símbolos especiais.
- **Validação de Nomenclatura:** aplica convenções para classes, relações, instâncias e novos tipos de dados.
- **Tratamento de Erros:** captura caracteres inválidos e fornece sugestões de correção.
- **Relatórios:** gera tabela de símbolos em múltiplos formatos (.txt, .csv, .html).

### Análise Sintática
- **Validação Estrutural:** verifica a gramática de pacotes, classes, heranças e tipos de dados.
- **Checagem de Relações:** valida a sintaxe de relações internas (dentro de classes) e externas.
- **Generalizações:** valida conjuntos de generalização (disjoint/complete).
- **Relatórios:** gera síntese da estrutura da ontologia e lista de erros sintáticos.

### Análise Semântica
- **Validação de ODPs:** verifica a conformidade das estruturas de modelagem com os Padrões de Projeto de Ontologias (ODPs), como Phase, RoleMixin e Relator Patterns.
- **Consistência Lógica:** assegura que as relações e generalizações sigam as regras de contexto (e.g., Relator mediando apenas para Roles).
- **Técnica de Coerção:** aplica a técnica de coerção para corrigir e reportar erros de consistência semântica, permitindo que a análise continue.
- **Relatórios:** gera relatório de padrões identificados, erros semânticos e coerções aplicadas.

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

Os resultados serão salvos na pasta `outputs/`, organizados em subpastas:

**Análise Léxica (`outputs/lexico/`):**
- `tabela_de_simbolos.txt` — tabela de símbolos em formato texto.
- `tabela_de_simbolos.csv` — tabela de símbolos em formato CSV.
- `tabela_de_simbolos.html` — tabela de símbolos em formato HTML.
- `erros_lexicos.txt` — relatório de erros léxicos encontrados.

**Análise Sintática (`outputs/sintatico/`):**
- `sintese_sintatica.txt` — resumo estrutural (pacotes, classes e relações encontradas).
- `erros_sintaticos.txt` — relatório de erros gramaticais encontrados.

**Análise Semântica (`outputs/semantico/`):**
- `relatorio_semantico.txt` — padrões identificados, erros de ODPs e coerções aplicadas.

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