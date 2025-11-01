from

if __name__ == "__main__":
    gerenciador = GerenciadorArquivos("data/alunos.json")

    alunos = [
        {"nome": "Letícia", "email": "leticia@email.com"},
        {"nome": "Alan", "email": "alan@email.com"}
    ]

    # Salvar
    gerenciador.salvar(alunos)

    # Carregar
    dados_lidos = gerenciador.carregar()
    print(dados_lidos)
