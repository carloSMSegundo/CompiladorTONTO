# src/parser_tonto.py
import ply.yacc as yacc
import os
from lexico_tonto import tokens, build_lexer

# Estrutura para o relatório
sintese = {
    "pacotes": [],
    "classes": {},
    "tipos": {},
    "enums": {},
    "generalizacoes": [],
    "relacoes_externas": []
}
erros_sintaticos = []


# ========================================================================
# 1. ESTRUTURA PRINCIPAL
# ========================================================================

def p_program(p):
    '''program : imports_opt package_decl elementos'''
    p[0] = ("program", p[2], p[3])


def p_imports_opt(p):
    '''imports_opt : imports_opt import_decl
                   | import_decl
                   | empty'''
    pass


def p_package_decl(p):
    '''package_decl : KW_PACKAGE identifier_any
                    | empty'''
    if len(p) == 3:
        sintese["pacotes"].append(p[2])
        p[0] = ("package", p[2])
    else:
        p[0] = None


def p_elementos(p):
    '''elementos : elementos elemento
                 | elemento'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2]); p[0] = p[1]


def p_elemento(p):
    '''elemento : class_decl
                | datatype_decl
                | enum_decl
                | genset_decl
                | relation_decl_external
                | import_decl'''
    p[0] = p[1]


def p_import_decl(p):
    'import_decl : KW_IMPORT identifier_any'
    p[0] = ("import", p[2])


# ========================================================================
# 2. CLASSES
# ========================================================================

def p_class_decl(p):
    '''class_decl : CLASS_STEREOTYPE CLASS_NAME nature_opt inheritance_opt body_opt'''
    nome = p[2]
    est = p[1]
    heranca = p[4];
    corpo = p[5]
    attrs, rels = [], []

    if corpo:
        for item in corpo:
            if item[0] == 'atributo':
                attrs.append(item)
            elif item[0] == 'relacao_interna':
                rels.append(item)

    sintese["classes"][nome] = {"estereotipo": est, "heranca": heranca, "atributos": attrs, "relacoes_internas": rels}
    p[0] = ("class", nome)


def p_nature_opt(p):
    '''nature_opt : KW_OF RELATION_NAME
                  | empty'''
    pass


def p_inheritance_opt(p):
    '''inheritance_opt : KW_SPECIALIZES class_list
                       | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_body_opt(p):
    '''body_opt : LBRACE class_body RBRACE
                | empty'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = None


def p_class_body(p):
    '''class_body : class_body member
                  | member'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2]); p[0] = p[1]


def p_member(p):
    '''member : atributo
              | internal_relation'''
    p[0] = p[1]


# ========================================================================
# 3. ATRIBUTOS
# ========================================================================

def p_cardinality_opt(p):
    '''cardinality_opt : cardinality
                       | empty'''
    pass

def p_atributo(p):
    '''atributo : RELATION_NAME COLON tipo cardinality_opt meta_attribs_opt'''
    p[0] = ("atributo", p[1], p[3])


def p_meta_attribs_opt(p):
    '''meta_attribs_opt : LBRACE RELATION_NAME RBRACE
                        | LBRACE RBRACE
                        | empty'''
    pass


def p_tipo(p):
    '''tipo : DATA_TYPE
            | NEW_TYPE
            | CLASS_NAME'''
    p[0] = p[1]


# ========================================================================
# 4. RELAÇÕES INTERNAS
# ========================================================================

def p_internal_relation(p):
    '''internal_relation : opt_at cardinality REL_SYM cardinality CLASS_NAME
                         | opt_at cardinality REL_SYM RELATION_NAME REL_SYM cardinality CLASS_NAME
                         | opt_at REL_SYM RELATION_NAME REL_SYM cardinality CLASS_NAME
                         | REL_SYM RELATION_NAME REL_SYM cardinality CLASS_NAME
                         | opt_at REL_SYM CLASS_NAME'''
    target = p[len(p) - 1]
    p[0] = ("relacao_interna", target)


# ========================================================================
# 5. TIPOS, ENUMS E GENSETS
# ========================================================================

def p_datatype_decl(p):
    'datatype_decl : KW_DATATYPE NEW_TYPE LBRACE atributos_dt RBRACE'
    sintese["tipos"][p[2]] = p[4]
    p[0] = ("datatype", p[2])


def p_atributos_dt(p):
    '''atributos_dt : atributos_dt atributo
                    | atributo'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2]); p[0] = p[1]


def p_enum_decl(p):
    'enum_decl : KW_ENUM CLASS_NAME LBRACE lista_enum RBRACE'
    sintese["enums"][p[2]] = p[4]
    p[0] = ("enum", p[2])


def p_lista_enum(p):
    '''lista_enum : lista_enum COMMA CLASS_NAME
                  | CLASS_NAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3]); p[0] = p[1]


def p_genset_decl(p):
    '''genset_decl : genset_inline
                   | genset_block'''
    p[0] = p[1]


def p_genset_modifiers(p):
    '''genset_modifiers : KW_DISJOINT KW_COMPLETE
                        | KW_DISJOINT
                        | KW_COMPLETE
                        | empty'''
    pass


def p_genset_inline(p):
    '''genset_inline : genset_modifiers KW_GENSET identifier_any KW_WHERE class_list KW_SPECIALIZES CLASS_NAME'''
    sintese["generalizacoes"].append({"nome": p[3], "tipo": "inline"})
    p[0] = ("genset", p[3])


def p_genset_block(p):
    '''genset_block : genset_modifiers KW_GENSET identifier_any LBRACE general_decl specifics_decl RBRACE'''
    sintese["generalizacoes"].append({"nome": p[3], "tipo": "block"})
    p[0] = ("genset_block", p[3])


def p_general_decl(p):
    'general_decl : KW_GENERAL CLASS_NAME'
    p[0] = p[2]


def p_specifics_decl(p):
    'specifics_decl : KW_SPECIFICS class_list'
    p[0] = p[2]


def p_class_list(p):
    '''class_list : class_list COMMA CLASS_NAME
                  | CLASS_NAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3]); p[0] = p[1]


# ========================================================================
# 6. RELAÇÕES EXTERNAS E AUXILIARES
# ========================================================================

def p_relation_decl_external(p):
    '''relation_decl_external : opt_at KW_RELATION CLASS_NAME cardinality REL_SYM cardinality CLASS_NAME
                              | opt_at KW_RELATION CLASS_NAME cardinality REL_SYM RELATION_NAME REL_SYM cardinality CLASS_NAME
                              | RELATION_STEREOTYPE KW_RELATION CLASS_NAME cardinality REL_SYM cardinality CLASS_NAME'''
    sintese["relacoes_externas"].append({"raw": "relação externa"})
    p[0] = ("relation", "ok")


def p_opt_at(p):
    '''opt_at : AT RELATION_STEREOTYPE
              | RELATION_STEREOTYPE
              | empty'''
    pass


def p_cardinality(p):
    '''cardinality : LBRACKET NUMBER RBRACKET
                   | LBRACKET NUMBER RANGE_DOTS STAR RBRACKET
                   | LBRACKET NUMBER RANGE_DOTS NUMBER RBRACKET
                   | LBRACKET STAR RBRACKET'''
    pass


def p_identifier_any(p):
    '''identifier_any : CLASS_NAME
                      | RELATION_NAME'''
    p[0] = p[1]


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        erros_sintaticos.append(f"[ERRO SINTÁTICO] Token inesperado '{p.value}' ({p.type}) na linha {p.lineno}")
    else:
        erros_sintaticos.append("[ERRO SINTÁTICO] Final inesperado do arquivo.")


# ========================================================================
# BUILD
# ========================================================================

def analisar_sintaxe(codigo):
    # 1. Reset das estruturas
    sintese["pacotes"].clear()
    sintese["classes"].clear()
    sintese["tipos"].clear()
    sintese["enums"].clear()
    sintese["generalizacoes"].clear()
    sintese["relacoes_externas"].clear()
    erros_sintaticos.clear()

    # 2. Remove parsetab.py antigo para forçar regeneração do parser.out
    arquivos_para_remover = ["parsetab.py", os.path.join("src", "parsetab.py")]
    for arq in arquivos_para_remover:
        if os.path.exists(arq):
            try:
                os.remove(arq)
            except:
                pass

    # 3. Build
    lexer_fresco = build_lexer()
    parser = yacc.yacc()  # Gera parser.out na raiz por padrão

    parser.parse(codigo, lexer=lexer_fresco)
    return sintese, erros_sintaticos, parser