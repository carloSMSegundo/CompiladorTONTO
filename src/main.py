import os
import csv
from lexico_tonto import analisar_arquivo

def salvar_resultados(tabela, erros, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)

    # Salvar tabela de símbolos em TXT
    txt_path = os.path.join(pasta_saida, "tabela_de_simbolos.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"{'Tipo':<25} {'Valor':<30} {'Linha':<10} {'Posição':<10}\n")
        f.write('-' * 80 + '\n')
        for s in tabela:
            f.write(f"{s['tipo']:<25} {repr(s['valor']):<30} {s['linha']:<10} {s['posicao']:<10}\n")
    print(f"[✔] Tabela TXT salva em: {txt_path}")

    # CSV
    csv_path = os.path.join(pasta_saida, "tabela_de_simbolos.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['tipo', 'valor', 'linha', 'posicao'])
        writer.writeheader()
        writer.writerows(tabela)
    print(f"[✔] Tabela CSV salva em: {csv_path}")

    # HTML
    html_path = os.path.join(pasta_saida, "tabela_de_simbolos.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><title>Tabela de Símbolos - TONTO</title></head><body>")
        f.write("<h2>Tabela de Símbolos</h2><table border='1' cellspacing='0' cellpadding='5'>")
        f.write("<tr><th>Tipo</th><th>Valor</th><th>Linha</th><th>Posição</th></tr>")
        for s in tabela:
            f.write(f"<tr><td>{s['tipo']}</td><td>{s['valor']}</td><td>{s['linha']}</td><td>{s['posicao']}</td></tr>")
        f.write("</table></body></html>")
    print(f"[✔] Tabela HTML salva em: {html_path}")

    # Erros
    err_path = os.path.join(pasta_saida, "erros_lexicos.txt")
    with open(err_path, 'w', encoding='utf-8') as f:
        if erros:
            f.write("--- Erros Léxicos Encontrados ---\n")
            for e in erros:
                f.write(e + "\n")
        else:
            f.write("Nenhum erro léxico encontrado.\n")
    print(f"[✔] Relatório de erros salvo em: {err_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analisador Léxico para a Linguagem TONTO.")
    parser.add_argument("arquivo", help="Caminho do arquivo .tonto a ser analisado")
    parser.add_argument("--saida", default="outputs", help="Diretório de saída (padrão: outputs)")
    args = parser.parse_args()

    tabela, erros = analisar_arquivo(args.arquivo)
    salvar_resultados(tabela, erros, args.saida)
