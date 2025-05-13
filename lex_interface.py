from lexer import lexer

with open('data/sample0.xml', 'r', encoding='utf-8') as f:
    data = f.read()

lexer.input(data)
print("Tokens reconhecidos:\n")
for token in lexer:
    print(f"{token.type}: {token.value}")
