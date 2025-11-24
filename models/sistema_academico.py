import os
import sys
from persistence.gerenciador_arquivos import GerenciadorArquivos
from aluno import Aluno
from professor import Professor
from curso import Curso
from disciplina import Disciplina


# Adiciona a pasta raiz do projeto ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SistemaAcademico:
    
    def __init__(self, alunos: list = None, professores: list = None, cursos: list = None, 
                 disciplinas: list = None, arquivos_dados: dict = None):
        
        self.__alunos = alunos if alunos is not None else []
        self.__professores = professores if professores is not None else []
        self.__cursos = cursos if cursos is not None else []
        self.__disciplinas = disciplinas if disciplinas is not None else []
        self.__arquivos_dados = arquivos_dados if arquivos_dados is not None else {}
      
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
        dados_serializados = {
            'alunos': [serializar_aluno(a) for a in self.__alunos],
            'professores': [serializar_professor(p) for p in self.__professores],
            'cursos': [serializar_curso(c) for c in self.__cursos],
            'disciplinas': [serializar_disciplina(d) for d in self.__disciplinas],
           
        }

        gerenciador = GerenciadorArquivos(self.__arquivos_dados)
        
        try: 
            gerenciador.salvar(dados_serializados) 
            print("Dados salvos e serializados com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def carregar_dados(self):
        def carregar_dados(self):
            gerenciador = GerenciadorArquivos(self.__arquivos_dados)
            
            try:
                dados_json = gerenciador.carregar()
                
                if not dados_json:
                    print("Nenhum dado encontrado.")
                    return 

                print("Dados JSON carregados. Iniciando desserialização...")

                # 1. DESSERIALIZAÇÃO INICIAL (cria objetos SEM associações)
                # A ordem é importante: carregar primeiro quem é referenciado
                
                self.__disciplinas = [desserializar_disciplina(d) for d in dados_json.get('disciplinas', [])]
                self.__professores = [desserializar_professor(p) for p in dados_json.get('professores', [])]
                self.__cursos = [desserializar_curso(c) for c in dados_json.get('cursos', [])]
                self.alunos = [desserializar_aluno(a) for a in dados_json.get('alunos', [])]
                # ... desserializar as demais classes (Matricula, Historico, MPD)

                # 2. RECONSTRUÇÃO DAS ASSOCIAÇÕES (O passo mais importante)
                # Você precisa de métodos de busca no SistemaAcademico para encontrar objetos por ID.
                # Exemplo: Reconstruindo a associação Professor-Disciplina
                self.reconstruir_associacoes() # Chamamos um novo método para isso.
                
                print("Dados carregados e objetos reconstruídos com sucesso!")
                
            except FileNotFoundError:
                print("Arquivo de dados não encontrado. Inicializando com listas vazias.")
                self.inicializar_vazio()
            except Exception as e:
                print(f"Erro ao carregar/desserializar dados: {e}. Inicializando vazio.")
                self.inicializar_vazio()

        def inicializar_vazio(self):
            self.__alunos = []
            self.__professores = []
            self.__cursos = []
            self.__disciplinas = []

        
        # Você precisará de métodos de busca como este:
        def buscar_professor_por_codigo(self, codigo):
            for p in self.__professores:
                if p.get_codigo() == codigo:
                    return p
            return None
            
        def buscar_curso_por_codigo(self, codigo):
            for c in self.__cursos:
                if c.get_codigo() == codigo:
                    return c
            return None