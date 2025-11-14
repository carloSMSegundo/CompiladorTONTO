# main.py (unificado: léxico + sintático + relatórios)
import os
import csv
import argparse
from collections import Counter
from lexico_tonto import analisar_arquivo, build_lexer
from parser_tonto import analisar_sintaxe

# ========================================================================
# 1. Utilitários para salvar relatórios
# ========================================================================

def salvar_tabela_simbolos(tabela, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    txt_path = os.path.join(pasta_saida, "tabela_de_simbolos.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"{'Tipo':<25} {'Valor':<30} {'Linha':<10} {'Posição':<10}\n")
        f.write('-' * 80 + '\n')
        for s in tabela:
            f.write(f"{s['tipo']:<25} {repr(s['valor']):<30} {s['linha']:<10} {s['posicao']:<10}\n")

    csv_path = os.path.join(pasta_saida, "tabela_de_simbolos.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['tipo', 'valor', 'linha', 'posicao'])
        writer.writeheader()
        writer.writerows(tabela)

    html_path = os.path.join(pasta_saida, "tabela_de_simbolos.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><meta charset='utf-8'><title>Tabela de Símbolos</title></head><body>")
        f.write("<h2>Tabela de Símbolos</h2><table border='1' cellspacing='0' cellpadding='5'>")
        f.write("<tr><th>Tipo</th><th>Valor</th><th>Linha</th><th>Posição</th></tr>")
        for s in tabela:
            f.write(f"<tr><td>{s['tipo']}</td><td>{s['valor']}</td><td>{s['linha']}</td><td>{s['posicao']}</td></tr>")
        f.write("</table></body></html>")

    return txt_path, csv_path, html_path


def salvar_erros(erros_lex, erros_sint, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    lex_path = os.path.join(pasta_saida, "erros_lexicos.txt")
    with open(lex_path, 'w', encoding='utf-8') as f:
        if erros_lex:
            f.write("--- Erros Léxicos Encontrados ---\n")
            for e in erros_lex:
                f.write(e + "\n")
        else:
            f.write("Nenhum erro léxico encontrado.\n")

    syn_path = os.path.join(pasta_saida, "erros_sintaticos.txt")
    with open(syn_path, 'w', encoding='utf-8') as f:
        if erros_sint:
            f.write("--- Erros Sintáticos Encontrados ---\n")
            for e in erros_sint:
                f.write(e + "\n")
        else:
            f.write("Nenhum erro sintático encontrado.\n")

    return lex_path, syn_path


def salvar_sintese(sintese, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    sintese_path = os.path.join(pasta_saida, "sintese_sintatica.txt")
    with open(sintese_path, 'w', encoding='utf-8') as f:
        f.write("--- Tabela de Síntese Sintática ---\n\n")

        f.write(f"Pacotes: {len(sintese['pacotes'])}\n")
        for p in sintese['pacotes']:
            f.write(f"  - {p}\n")

        f.write(f"\nClasses encontradas: {len(sintese['classes'])}\n")
        for name, meta in sintese['classes'].items():
            f.write(f"  - {name} (estereótipo={meta.get('estereotipo')}), atributos={len(meta.get('atributos', []))}\n")

        f.write(f"\nTipos (DataTypes): {len(sintese['tipos'])}\n")
        for tname, attrs in sintese['tipos'].items():
            f.write(f"  - {tname} (atributos={len(attrs)})\n")

        f.write(f"\nEnums: {len(sintese['enums'])}\n")
        for en, items in sintese['enums'].items():
            f.write(f"  - {en}: {', '.join(items)}\n")

        f.write(f"\nGeneralizações: {len(sintese['generalizacoes'])}\n")
        for g in sintese['generalizacoes']:
            f.write(f"  - {g}\n")

        f.write(f"\nRelações externas: {len(sintese['relacoes_externas'])}\n")
        for r in sintese['relacoes_externas']:
            f.write(f"  - {r}\n")

    return sintese_path


# ========================================================================
# 2. Função PRINCIPAL
# ========================================================================

def main(caminho_arquivo, pasta_saida):

    # ------------------------
    # 1) Análise Léxica
    # ------------------------
    tabela, erros_lex = analisar_arquivo(caminho_arquivo)
    txt_path, csv_path, html_path = salvar_tabela_simbolos(tabela, pasta_saida)

    # ------------------------
    # 2) Análise Sintática
    # ------------------------
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    sintese, erros_sint, arvore = analisar_sintaxe(codigo)

    # ------------------------
    # 3) Salvamento dos relatórios
    # ------------------------
    lex_path, syn_path = salvar_erros(erros_lex, erros_sint, pasta_saida)
    sintese_path = salvar_sintese(sintese, pasta_saida)

    # ------------------------
    # 4) Print final
    # ------------------------
    print(f"[✔] Tabela de símbolos: {txt_path}")
    print(f"[✔] CSV: {csv_path}")
    print(f"[✔] HTML: {html_path}")
    print(f"[✔] Erros léxicos: {lex_path}")
    print(f"[✔] Erros sintáticos: {syn_path}")
    print(f"[✔] Síntese sintática: {sintese_path}")


# ========================================================================
# 3. Execução via terminal
# ========================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisador Léxico + Sintático para TONTO")
    parser.add_argument("arquivo", help="Caminho para o arquivo .tonto")
    parser.add_argument("--saida", default="outputs", help="Diretório de saída")
    args = parser.parse_args()
    main(args.arquivo, args.saida)
