import ply.lex as lex
import os
import re # Importando a biblioteca de expressões regulares para checagens

# --- 1. Dicionário de Palavras Reservadas e Estereótipos ---
reserved = {
    # Palavras Reservadas
    'genset': 'RESERVED_WORD', 'disjoint': 'RESERVED_WORD', 'complete': 'RESERVED_WORD',
    'general': 'RESERVED_WORD', 'specifics': 'RESERVED_WORD', 'where': 'RESERVED_WORD', 'package': 'RESERVED_WORD',
    # Estereótipos de Classe
    'event': 'CLASS_STEREOTYPE', 'situation': 'CLASS_STEREOTYPE', 'process': 'CLASS_STEREOTYPE',
    'category': 'CLASS_STEREOTYPE', 'mixin': 'CLASS_STEREOTYPE', 'phaseMixin': 'CLASS_STEREOTYPE',
    'roleMixin': 'CLASS_STEREOTYPE', 'historicalRoleMixin': 'CLASS_STEREOTYPE', 'kind': 'CLASS_STEREOTYPE',
    'collective': 'CLASS_STEREOTYPE', 'quantity': 'CLASS_STEREOTYPE', 'quality': 'CLASS_STEREOTYPE',
    'mode': 'CLASS_STEREOTYPE', 'intrisicMode': 'CLASS_STEREOTYPE', 'extrinsicMode': 'CLASS_STEREOTYPE',
    'subkind': 'CLASS_STEREOTYPE', 'phase': 'CLASS_STEREOTYPE', 'role': 'CLASS_STEREOTYPE', 'historicalRole': 'CLASS_STEREOTYPE',
    # Estereótipos de Relação
    'material': 'RELATION_STEREOTYPE', 'derivation': 'RELATION_STEREOTYPE', 'comparative': 'RELATION_STEREOTYPE',
    'mediation': 'RELATION_STEREOTYPE', 'characterization': 'RELATION_STEREOTYPE', 'externalDependence': 'RELATION_STEREOTYPE',
    'componentOf': 'RELATION_STEREOTYPE', 'memberOf': 'RELATION_STEREOTYPE', 'subCollectionof': 'RELATION_STEREOTYPE',
    'subQualityOf': 'RELATION_STEREOTYPE', 'instantiation': 'RELATION_STEREOTYPE', 'termination': 'RELATION_STEREOTYPE',
    'participational': 'RELATION_STEREOTYPE', 'participation': 'RELATION_STEREOTYPE', 'historicalDependence': 'RELATION_STEREOTYPE',
    'creation': 'RELATION_STEREOTYPE', 'manifestation': 'RELATION_STEREOTYPE', 'bringsAbout': 'RELATION_STEREOTYPE',
    'triggers': 'RELATION_STEREOTYPE', 'composition': 'RELATION_STEREOTYPE', 'aggregation': 'RELATION_STEREOTYPE',
    'inherence': 'RELATION_STEREOTYPE', 'value': 'RELATION_STEREOTYPE', 'formal': 'RELATION_STEREOTYPE', 'constitution': 'RELATION_STEREOTYPE',
    # Meta-Atributos
    'ordered': 'META_ATTRIBUTE', 'const': 'META_ATTRIBUTE', 'derived': 'META_ATTRIBUTE', 'subsets': 'META_ATTRIBUTE', 'redefines': 'META_ATTRIBUTE',
    # Tipos de Dados Nativos
    'number': 'DATA_TYPE', 'string': 'DATA_TYPE', 'boolean': 'DATA_TYPE', 'date': 'DATA_TYPE', 'time': 'DATA_TYPE', 'datetime': 'DATA_TYPE'
}

# --- 2. Definição dos Tokens ---
tokens = [
    'SPECIAL_SYMBOL', 'CLASS_NAME', 'RELATION_NAME',
    'INSTANCE_NAME', 'NEW_TYPE', 'NUMBER'
] + list(set(reserved.values()))

# --- 3. Definição das Expressões Regulares (Regras) ---
# A ordem é importante: regras mais específicas primeiro.

# Símbolos Especiais (operadores mais longos primeiro)
t_SPECIAL_SYMBOL = r'<>--|--<>|<o>--|--|\.\.|\{|\}|\(|\)|\[|\]|\*|@|:'

# Regra para números inteiros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Convenção para Novos Tipos
def t_NEW_TYPE(t):
    r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ][a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]*DataType'
    return t

# Convenção para Nomes de Instâncias
def t_INSTANCE_NAME(t):
    r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ_]+[0-9]+'
    return t

# Regra para Identificadores (Nomes de Classe, Relação e Palavras-Chave)
def t_IDENTIFIER(t):
    r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ_][a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    
    if t.type == 'IDENTIFIER':
        if re.match(r'^[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]', t.value):
            t.type = 'CLASS_NAME'
        else:
            t.type = 'RELATION_NAME'
    return t

# --- 4. Regras de Controle do Analisador ---

# Regra para contar o número de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para ignorar comentários
def t_comment(t):
    r'\#.*'
    pass

# String para ignorar espaços e tabs
t_ignore  = ' \t'

# ATUALIZADO: A regra de erro agora aceita um ficheiro para escrever os erros
def t_error(t):
    mensagem = f"Erro Léxico: Caractere inesperado '{t.value[0]}' na linha {t.lexer.lineno}."
    print(mensagem) # Continua a mostrar na consola para feedback imediato
    erros_lexicos.append(mensagem)
    t.lexer.skip(1)

# --- 5. Construção e Execução ---

lexer = lex.lex()
lexer.lineno = 1
tabela_de_simbolos = []
erros_lexicos = [] # Lista para guardar as mensagens de erro

# Caminhos para os ficheiros
script_dir = os.path.dirname(__file__)
ficheiro_entrada = os.path.join(script_dir, '..', 'tests', 'exemplo1.tonto')
ficheiro_saida_simbolos = os.path.join(script_dir, '..', 'tabela_de_simbolos.txt')
ficheiro_saida_erros = os.path.join(script_dir, '..', 'erros_lexicos.txt')

try:
    with open(ficheiro_entrada, 'r', encoding='utf-8') as f:
        data = f.read()
    
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok: break
        tabela_de_simbolos.append({
            'tipo': tok.type, 'valor': tok.value,
            'linha': tok.lineno, 'posicao': tok.lexpos
        })

    # --- Escrita nos Ficheiros de Saída ---
    
    # Escrever a tabela de símbolos
    with open(ficheiro_saida_simbolos, 'w', encoding='utf-8') as f_simbolos:
        cabecalho = f"{'Tipo':<25} {'Valor':<30} {'Linha':<10} {'Posição':<10}\n"
        separador = "-" * 80 + "\n"
        f_simbolos.write(cabecalho)
        f_simbolos.write(separador)
        for simbolo in tabela_de_simbolos:
            linha = f"{simbolo['tipo']:<25} {repr(simbolo['valor']):<30} {simbolo['linha']:<10} {simbolo['posicao']:<10}\n"
            f_simbolos.write(linha)
    print(f"\nTabela de símbolos guardada em: {ficheiro_saida_simbolos}")

    # Escrever os erros léxicos
    with open(ficheiro_saida_erros, 'w', encoding='utf-8') as f_erros:
        if erros_lexicos:
            f_erros.write("--- Erros Léxicos Encontrados ---\n")
            for erro in erros_lexicos:
                f_erros.write(erro + "\n")
        else:
            f_erros.write("Nenhum erro léxico encontrado.\n")
    print(f"Relatório de erros guardado em: {ficheiro_saida_erros}")


except FileNotFoundError:
    print(f"Erro: Ficheiro de entrada não encontrado em '{ficheiro_entrada}'")

