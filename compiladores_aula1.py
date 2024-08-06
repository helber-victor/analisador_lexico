import re

def lexico(codigo_fonte):
    # Tabelas para armazenar tokens e símbolos
    tabela_tokens = []
    tabela_simbolos = {}

    # Expressões regulares para identificar tokens
    padrao_tokens = [
        ('COMENTARIO', r'\/\/.*|\/\*(.|\n)*?\*\/'),  # Comentários // e /* */
        ('NUMERO', r'\d+(\.\d+)?'),  # Números inteiros e decimais
        ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores
        ('OPERADOR', r'\+|\-|\*|\/'),  # Operadores matemáticos básicos
        ('ATRIBUICAO', r'\='),  # Operador de atribuição
        ('PARENTESE', r'\(|\)'),  # Parênteses
        ('PONTO_VIRGULA', r'\;'),  # Ponto e vírgula
    ]

    # Abrir o arquivo de código-fonte
    try:
        with open(codigo_fonte, 'r') as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{codigo_fonte}' não foi encontrado.")
        return

    # Processar cada linha do código-fonte
    for num_linha, linha in enumerate(linhas, start=1):
        pos = 0
        while pos < len(linha):
            encontrado = False
            for tipo, padrao in padrao_tokens:
                regex = re.compile(padrao)
                resultado = regex.match(linha, pos)
                if resultado:
                    valor = resultado.group(0)
                    tabela_tokens.append((tipo, valor, num_linha))
                    pos = resultado.end()
                    encontrado = True
                    # Adicionar à tabela de símbolos se for um identificador novo
                    if tipo == 'IDENTIFICADOR' and valor not in tabela_simbolos:
                        tabela_simbolos[valor] = None
                    break
            if not encontrado:
                print(f"Erro léxico na linha {num_linha}: Caractere inválido '{linha[pos]}'")
                pos += 1

    return tabela_tokens, tabela_simbolos

def gerar_saida(tabela_tokens, tabela_simbolos, arquivo_saida):
    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write("Tabela de Tokens:\n")
        for token in tabela_tokens:
            arquivo.write(f"{token[0]}: {token[1]} - Linha {token[2]}\n")

        arquivo.write("\nTabela de Símbolos:\n")
        for simbolo in tabela_simbolos:
            arquivo.write(f"{simbolo}\n")

    print(f"Análise léxica concluída. Saída salva em '{arquivo_saida}'.")

# Exemplo de uso:
codigo_fonte = 'exemplo_codigo.txt'  # Nome do arquivo de código-fonte
arquivo_saida = 'saida_lexico.txt'  # Nome do arquivo de saída

tabela_tokens, tabela_simbolos = lexico(codigo_fonte)
gerar_saida(tabela_tokens, tabela_simbolos, arquivo_saida)