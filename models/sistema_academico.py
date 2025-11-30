import os
import sys
import datetime 

# Importa o Gerenciador de Arquivos (Classe)
from persistence.gerenciador_arquivos import GerenciadorArquivos

# Importa as classes de modelos
from models.aluno import Aluno
from models.professor import Professor
from models.curso import Curso
from models.disciplina import Disciplina
from models.matricula import Matricula
from models.historicoacademico import HistoricoAcademico
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.pessoa import Pessoa 


# --- FUNÇÕES DE SERIALIZAÇÃO/DESSERIALIZAÇÃO ---
# ATENÇÃO: É VITAL que essas funções existam em utils/serializador.py e utils/desserializar.py
from utils.serializador import (
    serealizar_aluno, serializar_professor, serealizar_curso, 
    serealizar_disciplina, serealizar_historico, serializar_matricula, 
    serializar_mpd, serializar_pessoa # Assumindo os nomes
)
from utils.desserializar import (
    desserializar_aluno, desserializar_professor, desserializar_curso, 
    desserializar_disciplina, desserializar_historico, desserializar_matricula, 
    desserializar_mpd, desserializar_pessoa, ligar_objetos, carregar_tudo
)
# ----------------------------------------------------


# Adiciona a pasta raiz do projeto ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SistemaAcademico:
    
    def __init__(self, arquivos_dados: dict = None):
        # Mantenho os nomes de atributos que você escolheu (sem '__')
        self.alunos = {}
        self.professores = {}
        self.cursos = {}
        self.disciplinas = {}
        self.historicos_academicos = {}
        self.matriculas = {}
        self.matriculas_pagas_disciplinas = {}
        
        self.arquivos_dados = arquivos_dados if arquivos_dados is not None else {'principal':'persistence/dados/sistema_academico.json'}
        
        # O Gerenciador de Arquivos é inicializado aqui
        self.gerenciador = GerenciadorArquivos(self.arquivos_dados)

        self.carregar_dados()

    # Getters (atualizados para seus novos nomes de atributos)

    def get_alunos(self):
        return self.alunos
    
    def get_professores(self):
        return self.professores
    
    def get_cursos(self):
        return self.cursos
    
    def get_disciplinas(self):
        return self.disciplinas
    
    def get_historicos_academicos(self):
        return self.historicos_academicos
    
    def get_matriculas(self):
        return self.matriculas
    
    def get_matriculas_pagas_disciplinas(self):
        return self.matriculas_pagas_disciplinas    
   
    
    
    def salvar_dados(self):
        """
        Serializa todos os objetos da memória e salva no arquivo JSON.
        CORRIGIDO: Agora usa a estrutura de dicionário (chave: valor) exigida pelo JSON.
        """
        print("Iniciando a serialização e salvamento...")

        # É OBRIGATÓRIO ter chaves (strings) para cada lista
        dados_serializados = {
            'alunos': [serealizar_aluno(a) for a in self.alunos.values()],
            'professores': [serializar_professor(p) for p in self.professores.values()],
            'cursos': [serealizar_curso(c) for c in self.cursos.values()],
            'disciplinas': [serealizar_disciplina(d) for d in self.disciplinas.values()],
            'historicos_academicos': [serealizar_historico(h) for h in self.historicos_academicos.values()],
            'matriculas': [serializar_matricula(m) for m in self.matriculas.values()],
            'matriculas_pagas_disciplinas': [serializar_mpd(mpd) for mpd in self.matriculas_pagas_disciplinas.values()],
        }

        try:
            self.gerenciador.salvar(dados_serializados)
            print("Dados salvos e serializados com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def carregar_dados(self):
        """
        Carrega dados do JSON, desserializa e reconstrói as associações.
        """
        dados_json = self.gerenciador.carregar()
        
        if not dados_json:
            print("Nenhum dado encontrado para carregar. Sistema iniciado vazio.")
            return 
            
        print("Dados JSON carregados, iniciando desserialização e ligação...")

        # Chama a função orquestradora que cria e liga todos os objetos
        try:
            alunos, cursos, disciplinas, professores, matriculas, historicos, mpds = carregar_tudo(
                dados_json.get('alunos', []),
                dados_json.get('cursos', []),
                dados_json.get('disciplinas', []),
                dados_json.get('professores', []),
                dados_json.get('matriculas', []),
                dados_json.get('historicos_academicos', []),
                dados_json.get('matriculas_pagas_disciplinas', [])

            )
            
            # ATUALIZAÇÃO DO ESTADO CENTRAL DO SISTEMA
            self.alunos = alunos
            self.cursos = cursos
            self.disciplinas = disciplinas
            self.professores = professores
            self.matriculas = matriculas
            self.historicos_academicos = historicos
            self.matriculas_pagas_disciplinas = mpds
            
            print(f"Dados carregados! Alunos: {len(self.alunos)}, Cursos: {len(self.cursos)}, MPDs: {len(self.matriculas_pagas_disciplinas)}")
            
        except Exception as e:
            print(f"ERRO CRÍTICO na desserialização ou ligação de objetos: {e}")
            print("O sistema foi reiniciado com dados vazios para evitar falhas.")
            self.alunos.clear()
            self.cursos.clear()
            self.disciplinas.clear()
            self.professores.clear()
            self.matriculas.clear()
            self.historicos_academicos.clear()
            self.matriculas_pagas_disciplinas.clear() 