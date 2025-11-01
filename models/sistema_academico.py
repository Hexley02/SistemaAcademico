import os
import sys
from persistence.gerenciador_arquivos import GerenciadorArquivos


# adiciona a pasta raiz do projeto ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SistemaAcademico:
    def __init__(self,alunos:list,professores:list, cursos:list, disciplinas:list, arquivos_dados:str):
        self.__alunos = alunos
        self.__professores = professores
        self.__cursos = cursos
        self.__disciplinas = disciplinas
        self.__arquivos_dados = arquivos_dados

    
    def get_alunos(self):
        return self.__alunos    
    
    def get_professores(self):
        return self.__professores
    
    def get_cursos(self):
        return self.__cursos
    
    def get_disciplinas(self):
        return self.__disciplinas
    
    def get_arquivos_dados(self):
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
        gerenciador.salvar(dados)

    def carregar_dados(self):
        dados = GerenciadorArquivos(self.__arquivos_dados).carregar()
        if dados:
            self.__alunos = dados.get('alunos', [])
            self.__professores = dados.get('professores', [])
            self.__cursos = dados.get('cursos', [])
            self.__disciplinas = dados.get('disciplinas', [])

        else:
            print("Nenhum dado encontrado para carregar.")
          

    

    