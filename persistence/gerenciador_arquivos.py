import json

class GerenciadorArquivos:
    @staticmethod
    def salvar(dados, caminho_arquivo):
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar(caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return []
