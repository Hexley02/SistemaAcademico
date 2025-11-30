import json
import os 

class GerenciadorArquivos:
    """
    Responsável por ler e escrever o dicionário de dados do sistema no formato JSON.
    Mantido simples para focar apenas na persistência.
    """
    def __init__(self, arquivos_dados: dict):
        """
        Inicializa com o caminho do arquivo principal, extraindo do dicionário.
        Args:
            arquivos_dados (dict): Dicionário contendo os caminhos, ex: {'principal': 'path/to/file.json'}
        """
        # Extrai o caminho da chave 'principal'
        self.caminho_arquivo = arquivos_dados.get('principal')
        
        # Garante que o diretório existe antes de tentar salvar
        self._verificar_diretorio()

    def _verificar_diretorio(self):
        """
        Verifica se o diretório para salvar o arquivo existe e o cria se necessário.
        """
        diretorio = os.path.dirname(self.caminho_arquivo)
        
        # Se houver um diretório especificado e ele não existir, cria-o
        if diretorio and not os.path.exists(diretorio):
            try:
                os.makedirs(diretorio)
                # print(f"Diretório criado: {diretorio}")
            except OSError as e:
                print(f"ERRO: Falha ao criar o diretório {diretorio}. {e}")

    def salvar(self, dados: dict):
        
        try:
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                # O ensure_ascii=False garante que caracteres acentuados funcionem
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            print("Dados salvos com sucesso em {}".format(self.caminho_arquivo))
        except IOError as e:
            print(f"ERRO: Não foi possível escrever no arquivo {self.caminho_arquivo}. {e}")
        except TypeError as e:
            print(f"ERRO: Objeto inválido para serialização JSON. Verifique as funções de serialização. {e}")


    def carregar(self) -> dict:
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                print("Dados carregados com sucesso de {}".format(self.caminho_arquivo))
                return dados
        except FileNotFoundError:
            # Captura se o arquivo não existe (comum no primeiro uso)
            print("Arquivo {} não encontrado. Retornando dados vazios.".format(self.caminho_arquivo))
            return {}
        except json.JSONDecodeError:
            # Captura se o arquivo está vazio ou corrompido
            print(f"AVISO: O arquivo {self.caminho_arquivo} está corrompido ou vazio. Retornando dados vazios.")
            return {}
        except Exception as e:
            print(f"ERRO inesperado ao carregar dados: {e}")
            return {}