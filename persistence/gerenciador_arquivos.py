import json

class GerenciadorArquivos:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def salvar(self, dados):
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            print("Dados salvos com sucesso em {}".format(self.caminho_arquivo))

    def carregar(self):
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                print ("Dados carregados com sucesso de {}".format(self.caminho_arquivo))

                return dados
        except FileNotFoundError:
            print("Arquivo {} não encontrado.".format(self.caminho_arquivo))
            return None