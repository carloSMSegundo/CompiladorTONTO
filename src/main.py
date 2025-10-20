import os
import csv
from collections import Counter
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
    print(f"[✔] Tabela de Símbolos (analítica) salva em: {txt_path}")

    # CSV
    csv_path = os.path.join(pasta_saida, "tabela_de_simbolos.csv")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['tipo', 'valor', 'linha', 'posicao'])
        writer.writeheader()
        writer.writerows(tabela)
    print(f"[✔] Tabela de Símbolos (CSV) salva em: {csv_path}")

    # HTML
    html_path = os.path.join(pasta_saida, "tabela_de_simbolos.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<html><head><title>Tabela de Símbolos - TONTO</title></head><body>")
        f.write("<h2>Tabela de Símbolos (Visão Analítica)</h2><table border='1' cellspacing='0' cellpadding='5'>")
        f.write("<tr><th>Tipo</th><th>Valor</th><th>Linha</th><th>Posição</th></tr>")
        for s in tabela:
            f.write(f"<tr><td>{s['tipo']}</td><td>{s['valor']}</td><td>{s['linha']}</td><td>{s['posicao']}</td></tr>")
        f.write("</table></body></html>")
    print(f"[✔] Tabela de Símbolos (HTML) salva em: {html_path}")

    # Contar a ocorrência de cada tipo de token.
    contagem_tipos = Counter(s['tipo'] for s in tabela)

    sintese = {
        'Classes': contagem_tipos.get('CLASS_NAME', 0),
        'Relações': contagem_tipos.get('RELATION_NAME', 0),
        'Palavras-Chave (Estereótipos)': contagem_tipos.get('CLASS_STEREOTYPE', 0) + contagem_tipos.get('RELATION_STEREOTYPE', 0),
        'Indivíduos (Instâncias)': contagem_tipos.get('INSTANCE_NAME', 0),
        'Palavras Reservadas': contagem_tipos.get('RESERVED_WORD', 0),
        'Meta-Atributos': contagem_tipos.get('META_ATTRIBUTE', 0)
    }

    # Salvar a tabela de síntese em TXT
    sintese_path = os.path.join(pasta_saida, "tabela_de_sintese.txt")
    with open(sintese_path, 'w', encoding='utf-8') as f:
        f.write("--- Tabela de Síntese ---\n")
        f.write("Contagem dos elementos encontrados no código-fonte.\n")
        f.write('-' * 40 + '\n')
        for categoria, quantidade in sintese.items():
            f.write(f"{categoria:<30}: {quantidade}\n")
    print(f"[✔] Tabela de Síntese salva em: {sintese_path}")


    # Salvar Relatório de Erros (continua o mesmo)
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

    tabela_analitica, erros_lexicos = analisar_arquivo(args.arquivo)
    
    # Passa a tabela e os erros para a função que salva tudo
    salvar_resultados(tabela_analitica, erros_lexicos, args.saida)