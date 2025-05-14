from src.interface.gui import Application
from src.parser import parser

# Opções: 'parser' ou 'interface'
RUN_MODE = 'interface'


def run_parser():
    with open('data/sample.xml', 'r') as f:
        data = f.read()

    articles = parser.parse(data)

    for i, art in enumerate(articles, 1):
        print(f"\nArtigo {i}:")
        print(f"  Título:   {art.get('title', [''])[0]}")
        print(f"  Autores:  {', '.join(art.get('author', []))}")
        print(f"  Abstract: {' '.join(art.get('abstract', []))}")
        print(f"  Ano:      {art.get('year', [''])[0]}")


def run_interface():
    app = Application()
    app.run()


def main():
    if RUN_MODE == 'parser':
        run_parser()
    elif RUN_MODE == 'interface':
        run_interface()
    else:
        raise ValueError(f'Modo de execução desconhecido: {RUN_MODE}')


if __name__ == '__main__':
    main()
