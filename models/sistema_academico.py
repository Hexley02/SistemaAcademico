import os
import sys
from persistence.gerenciador_arquivos import GerenciadorArquivos


# adiciona a pasta raiz do projeto ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SistemaAcademico:
    def __init__(self,alunos:list = None ,professores:list = None, cursos:list = None , disciplinas:list = None , arquivos_dados:dict = None):
        self.__alunos = alunos if alunos is not None else []
        self.__professores = professores if professores is not None else []
        self.__cursos = cursos if cursos is not None else []
        self.__disciplinas = disciplinas if disciplinas is not None else []
      

    
    #getters 

    def get_alunos(self) -> list:
        return self.__alunos    
    
    def get_professores(self) -> list:
        return self.__professores
    
    def get_cursos(self) -> list:
        return self.__cursos
    
    def get_disciplinas(self) -> list:
        return self.__disciplinas
    
    def get_arquivos_dados(self) -> dict:
        return self.__arquivos_dados
    
# metódos 

    def salvar_dados(self):
        dados = {
            'alunos': self.__alunos,
            'professores': self.__professores,
            'cursos': self.__cursos,
            'disciplinas': self.__disciplinas

        }

        gerenciador = GerenciadorArquivos(self.__arquivos_dados)
        
        try: 
            gerenciador.salvar(dados)
            print("Dados salvo com sucesso!")
        except Exception as e:
            print("Erro ao salvar dados: {e}")

    def carregar_dados(self):
        gerenciador = GerenciadorArquivos(self.__arquivos_dados)

        try:
            dados = gerenciador.carregar()
            if dados:
                self.__alunos = dados.get('alunos', [])
                self.__professores = dados.get('professores', [])
                self.__cursos = dados.get('cursos', [])
                self.__disciplinas = dados.get('disciplinas', [])
            else:
                print("Nenhum dado encontrado para carregar. Inicializando com listas vazias.")
                self.__alunos = []
                self.__professores = []
                self.__cursos = []
                self.__disciplinas = []
        except FileNotFoundError:
            print("Arquivo de dados não encontrado. Inicializando com listas vazias.")
            self.__alunos = []
            self.__professores = []
            self.__cursos = []
            self.__disciplinas = []
        except Exception as e:
            print(f"Erro ao carregar dados: {e}. Inicializando com listas vazias.")
            self.__alunos = []
            self.__professores = []
            self.__cursos = []
            self.__disciplinas = []

    
    

    