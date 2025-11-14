# parser_tonto.py
import ply.yacc as yacc
from lexico_tonto import tokens

# Síntese sintática e lista de erros
sintese = {
    "pacotes": [],
    "classes": {},      # nome -> {estereotipo, atributos, relacoes_internas}
    "tipos": {},       # nome -> atributos
    "enums": {},       # nome -> [valores]
    "generalizacoes": [],  # list of dicts
    "relacoes_externas": []  # list of dicts
}
erros_sintaticos = []

# ----------------------------
# programa
# ----------------------------
def p_program(p):
    'program : package_decl elementos'
    p[0] = ("program", p[1], p[2])

# ----------------------------
# package
# ----------------------------
def p_package_decl(p):
    'package_decl : RESERVED_WORD CLASS_NAME'
    if p[1] != 'package':
        erros_sintaticos.append(f"Esperado 'package', encontrado '{p[1]}'.")
    else:
        sintese["pacotes"].append(p[2])
    p[0] = ("package", p[2])

# ----------------------------
# elementos (vários elementos: classes, tipos, enums, generalizacoes, relacoes)
# ----------------------------
def p_elementos(p):
    '''
    elementos : elementos elemento
              | elemento
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_elemento(p):
    '''
    elemento : class_decl
             | datatype_decl
             | enum_decl
             | generalizacao
             | relation_decl
    '''
    p[0] = p[1]

# ----------------------------
# class_decl
# suportamos duas formas: com atributos entre { ... } ou vazio { }
# ----------------------------
def p_class_decl(p):
    '''
    class_decl : CLASS_STEREOTYPE CLASS_NAME SPECIAL_SYMBOL atributos SPECIAL_SYMBOL
               | CLASS_STEREOTYPE CLASS_NAME SPECIAL_SYMBOL SPECIAL_SYMBOL
    '''
    nome = p[2]
    est = p[1]
    if len(p) == 6:
        # p[3] = '{', p[5] = '}'
        if p[3] != '{' and p[3] != '{':
            pass
        attrs = p[4]
    else:
        attrs = []
    sintese["classes"][nome] = {"estereotipo": est, "atributos": attrs, "relacoes_internas": []}
    p[0] = ("class", nome)

# ----------------------------
# atributos (lista)
# um atributo é name : tipo
# usamos RELATION_NAME (lex marca atributos minúsculos)
# ----------------------------
def p_atributos(p):
    '''
    atributos : atributos atributo
              | atributo
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_atributo(p):
    'atributo : RELATION_NAME SPECIAL_SYMBOL tipo'
    # p[2] deve ser ':'
    p[0] = (p[1], p[3])

def p_tipo(p):
    '''
    tipo : DATA_TYPE
         | NEW_TYPE
         | CLASS_NAME
    '''
    p[0] = p[1]

# ----------------------------
# datatype_decl (novos tipos)
# ex: EnderecoDataType { campo: string }
# ----------------------------
def p_datatype_decl(p):
    'datatype_decl : NEW_TYPE SPECIAL_SYMBOL atributos SPECIAL_SYMBOL'
    # p[2] == '{', p[4] == '}'
    sintese["tipos"][p[1]] = p[3]
    p[0] = ("datatype", p[1])

# ----------------------------
# enum_decl
# ex: enum EyeColor { Blue, Green }
# ----------------------------
def p_enum_decl(p):
    'enum_decl : RESERVED_WORD CLASS_NAME SPECIAL_SYMBOL lista_enum SPECIAL_SYMBOL'
    if p[1] != 'enum':
        erros_sintaticos.append(f"Esperado 'enum' antes de {p[2]}.")
    else:
        sintese["enums"][p[2]] = p[4]
    p[0] = ("enum", p[2])

def p_lista_enum(p):
    '''
    lista_enum : lista_enum SPECIAL_SYMBOL CLASS_NAME
               | CLASS_NAME
    '''
    # note: usamos SPECIAL_SYMBOL para vírgula (lex gera ',' como SPECIAL_SYMBOL com value ',')
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

# ----------------------------
# generalizacao (duas formas)
# Forma inline: disjoint complete genset Nome where A, B
# Forma em bloco: genset Nome { general Parent; specifics Child, Other }
# ----------------------------
def p_generalizacao_inline(p):
    'generalizacao : RESERVED_WORD RESERVED_WORD RESERVED_WORD CLASS_NAME RESERVED_WORD class_list'
    # ex: disjoint complete genset Person where Parent, Child
    # p[1] disjoint, p[2] complete, p[3] genset, p[5] where
    if p[3] != 'genset':
        erros_sintaticos.append("Esperado 'genset' em generalização inline.")
    sintese["generalizacoes"].append({
        "nome": p[4],
        "modifiers": [p[1], p[2]],
        "classes": p[7]
    })
    p[0] = ("genset_inline", p[4])

def p_class_list(p):
    '''
    class_list : CLASS_NAME
               | class_list SPECIAL_SYMBOL CLASS_NAME
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        # p[2] should be ',' (SPECIAL_SYMBOL value)
        p[1].append(p[3])
        p[0] = p[1]

def p_generalizacao_block(p):
    'generalizacao : RESERVED_WORD CLASS_NAME SPECIAL_SYMBOL general_block SPECIAL_SYMBOL'
    # ex: genset PersonGroup { general Parent specifics A, B }
    nome = p[2]
    body = p[4]
    sintese["generalizacoes"].append({"nome": nome, "body": body})
    p[0] = ("genset_block", nome)

def p_general_block(p):
    '''
    general_block : general_spec specifics_spec
    '''
    p[0] = {"general": p[1], "specifics": p[2]}

def p_general_spec(p):
    'general_spec : RESERVED_WORD CLASS_NAME'
    if p[1] != 'general':
        erros_sintaticos.append("Esperado 'general' em bloco de generalização.")
    p[0] = p[2]

def p_specifics_spec(p):
    'specifics_spec : RESERVED_WORD class_list'
    if p[1] != 'specifics':
        erros_sintaticos.append("Esperado 'specifics' em bloco de generalização.")
    p[0] = p[2]

# ----------------------------
# relations (externas e internas)
# Externa: optional '@' RELATION_STEREOTYPE relation_name? relation_body
# Interna (dentro de class_decl) não é totalmente implementada aqui, mas parser aceita uma linha com stereotipo + cardinalidades + target
# ----------------------------
def p_relation_decl(p):
    '''
    relation_decl : opt_at SIGNED_RELATION
                 | RELATION_STEREOTYPE SIGNED_RELATION
                 | RESERVED_WORD SIGNED_RELATION
    '''
    # SIGNED_RELATION is a helper nonterminal
    # p may be variable length; normalize
    if len(p) == 3:
        body = p[2]
        prefix = p[1]
    else:
        prefix = None
        body = p[2]
    sintese["relacoes_externas"].append({"prefix": prefix, "body": body})
    p[0] = ("relation", body)

def p_opt_at(p):
    'opt_at : SPECIAL_SYMBOL'
    # expects '@'
    if p[1] != '@':
        erros_sintaticos.append("Esperado '@' antes do estereótipo de relação.")
    p[0] = p[1]

def p_signed_relation(p):
    '''
    SIGNED_RELATION : RELATION_STEREOTYPE relation_body
                    | RESERVED_WORD relation_body
                    | relation_body
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_relation_body(p):
    '''
    relation_body : CLASS_NAME relation_symbol CLASS_NAME
                  | CLASS_NAME
    '''
    # relation_symbol is SPECIAL_SYMBOL values like '--' or '<>--'
    if len(p) == 4:
        p[0] = {"src": p[1], "symbol": p[2], "dst": p[3]}
    else:
        p[0] = {"single": p[1]}

# ----------------------------
# catch-all token for relation symbol
# We let parser accept any SPECIAL_SYMBOL token in these positions and will inspect its .value
# ----------------------------
def p_relation_symbol(p):
    'relation_symbol : SPECIAL_SYMBOL'
    p[0] = p[1]

# ----------------------------
# erro
# ----------------------------
def p_error(p):
    if p:
        erros_sintaticos.append(f"[ERRO SINTÁTICO] Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        erros_sintaticos.append("[ERRO SINTÁTICO] Final inesperado do arquivo.")

# ----------------------------
# Construção do parser
# ----------------------------
parser = yacc.yacc()

def analisar_sintaxe(codigo):
    """
    Recebe o texto completo e realiza a análise sintática.
    Retorna: (sintese, erros_sintaticos, arvore)
    """
    # Reset das estruturas
    sintese["pacotes"].clear()
    sintese["classes"].clear()
    sintese["tipos"].clear()
    sintese["enums"].clear()
    sintese["generalizacoes"].clear()
    sintese["relacoes_externas"].clear()
    erros_sintaticos.clear()

    # Deixa o PLY criar o próprio lexer
    arvore = parser.parse(codigo)

    return sintese, erros_sintaticos, arvore

