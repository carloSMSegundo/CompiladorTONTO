import os
import csv
import argparse
from lexico_tonto import analisar_arquivo
from parser_tonto import analisar_sintaxe
# Importa a nova função (o arquivo semantico_tonto.py deve existir na mesma pasta)
from semantico_tonto import verificar_semantica 

def salvar_lexico(tabela, erros, pasta_raiz):
    pasta_lexico = os.path.join(pasta_raiz, "lexico")
    os.makedirs(pasta_lexico, exist_ok=True)

    txt_path = os.path.join(pasta_lexico, "tabela_de_simbolos.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"{'Tipo':<25} {'Valor':<30} {'Linha':<10} {'Posição':<10}\n")
        f.write('-' * 80 + '\n')
        for s in tabela:
            f.write(f"{s['tipo']:<25} {repr(s['valor']):<30} {s['linha']:<10} {s['posicao']:<10}\n")

    csv_path = os.path.join(pasta_lexico, "tabela_de_simbolos.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['tipo', 'valor', 'linha', 'posicao'])
        writer.writeheader()
        writer.writerows(tabela)

    html_path = os.path.join(pasta_lexico, "tabela_de_simbolos.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><meta charset='utf-8'><title>Tabela de Símbolos</title></head><body>")
        f.write("<h2>Tabela de Símbolos</h2><table border='1' cellspacing='0' cellpadding='5'>")
        f.write("<tr><th>Tipo</th><th>Valor</th><th>Linha</th><th>Posição</th></tr>")
        for s in tabela:
            f.write(f"<tr><td>{s['tipo']}</td><td>{s['valor']}</td><td>{s['linha']}</td><td>{s['posicao']}</td></tr>")
        f.write("</table></body></html>")

    erro_path = os.path.join(pasta_lexico, "erros_lexicos.txt")
    with open(erro_path, 'w', encoding='utf-8') as f:
        if erros:
            f.write("--- Erros Léxicos Encontrados ---\n")
            for e in erros:
                f.write(e + "\n")
        else:
            f.write("Nenhum erro léxico encontrado.\n")

    return txt_path, csv_path, html_path, erro_path


def salvar_sintatico(sintese, erros, pasta_raiz):
    pasta_sintatico = os.path.join(pasta_raiz, "sintatico")
    os.makedirs(pasta_sintatico, exist_ok=True)

    erro_path = os.path.join(pasta_sintatico, "erros_sintaticos.txt")
    with open(erro_path, 'w', encoding='utf-8') as f:
        if erros:
            f.write("--- Erros Sintáticos Encontrados ---\n")
            for e in erros:
                f.write(e + "\n")
        else:
            f.write("Nenhum erro sintático encontrado.\n")

    sintese_path = os.path.join(pasta_sintatico, "sintese_sintatica.txt")
    with open(sintese_path, 'w', encoding='utf-8') as f:
        f.write("--- Tabela de Síntese Sintática ---\n\n")

        f.write(f"Pacotes: {len(sintese['pacotes'])}\n")
        for p in sintese['pacotes']:
            f.write(f"  - {p}\n")

        f.write(f"\nClasses encontradas: {len(sintese['classes'])}\n")
        for name, meta in sintese['classes'].items():
            num_attrs = len(meta.get('atributos', []))
            # Ajuste para lidar com a nova estrutura de relacoes_internas (tupla com dict)
            rels_int = meta.get('relacoes_internas', [])
            num_rels_int = len(rels_int)

            f.write(
                f"  - {name} (estereótipo={meta.get('estereotipo')}), atributos={num_attrs}, relacoes_internas={num_rels_int}\n")

        if num_rels_int > 0:
                 for item in rels_int:
                     dados = item[1]
                     f.write(f"    -> Relação Interna: {dados.get('raw')}\n")

        f.write(f"\nTipos (DataTypes): {len(sintese['tipos'])}\n")
        for tname, attrs in sintese['tipos'].items():
            if isinstance(attrs, dict) and "especializa" in attrs:
                f.write(f"  - {tname} (especializa={attrs['especializa']})\n")
            else:
                num_attrs = len(attrs) if isinstance(attrs, list) else 0
                f.write(f"  - {tname} (atributos={num_attrs})\n")

        f.write(f"\nEnums: {len(sintese['enums'])}\n")
        for en, items in sintese['enums'].items():
            f.write(f"  - {en}: {', '.join(items)}\n")

        f.write(f"\nGeneralizações: {len(sintese['generalizacoes'])}\n")
        for g in sintese['generalizacoes']:
            mod_str = f" [{', '.join(g.get('modifiers', []))}]" if g.get('modifiers') else ""
            f.write(f"  - {g['nome']} ({g.get('general')} -> {g.get('specifics')}){mod_str}\n")

        f.write(f"\nRelações externas: {len(sintese['relacoes_externas'])}\n")
        for r in sintese['relacoes_externas']:
            desc = r.get('raw', 'relação externa detalhe indisponível')
            f.write(f"  - {desc}\n")

    return sintese_path, erro_path

def salvar_semantico(padroes, erros, pasta_raiz):
    pasta_sem = os.path.join(pasta_raiz, "semantico")
    os.makedirs(pasta_sem, exist_ok=True)
    
    path = os.path.join(pasta_sem, "relatorio_semantico.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write("=== RELATÓRIO DE ANÁLISE SEMÂNTICA (ODPs) ===\n\n")
        
        f.write("1. PADRÕES IDENTIFICADOS:\n")
        if padroes:
            for p in padroes:
                f.write(f"   {p}\n")
        else:
            f.write("   Nenhum padrão ODP completo identificado.\n")
            
        f.write("\n2. ERROS E COERÇÕES:\n")
        if erros:
            for e in erros:
                f.write(f"   [!] {e}\n")
        else:
            f.write("   Nenhum erro semântico de padrão encontrado.\n")
    return path


def main(caminho_arquivo, pasta_saida):
    print(f"\nProcessando: {caminho_arquivo}")
    print("-" * 40)

    # 1) Análise Léxica
    tabela, erros_lex = analisar_arquivo(caminho_arquivo)
    salvar_lexico(tabela, erros_lex, pasta_saida)
    print(f"[LÉXICO] Saídas salvas em: {os.path.join(pasta_saida, 'lexico')}")

    # 2) Análise Sintática
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    sintese, erros_sint, _ = analisar_sintaxe(codigo)
    salvar_sintatico(sintese, erros_sint, pasta_saida)
    print(f"[SINTÁTICO] Relatórios salvos em: {os.path.join(pasta_saida, 'sintatico')}")

    # 3) Análise Semântica
    print("[SEMÂNTICO] Iniciando validação de padrões ODP...")
    padroes, erros_sem = verificar_semantica(sintese)
    salvar_semantico(padroes, erros_sem, pasta_saida)
    print(f"[SEMÂNTICO] Relatório salvo em: {os.path.join(pasta_saida, 'semantico')}")

    print("-" * 40)
    print("Processamento concluído com sucesso! 🚀\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisador Léxico + Sintático + Semântico para TONTO")
    parser.add_argument("arquivo", help="Caminho para o arquivo .tonto")
    parser.add_argument("--saida", default="outputs", help="Diretório de saída")
    args = parser.parse_args()
    main(args.arquivo, args.saida)