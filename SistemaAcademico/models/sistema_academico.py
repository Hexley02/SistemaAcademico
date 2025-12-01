# models/sistema_academico.py
import os
import sys
import datetime
from typing import Dict, TYPE_CHECKING

# Gerenciador de Arquivos
from persistence.gerenciador_arquivos import GerenciadorArquivos

if TYPE_CHECKING:
    from models.aluno import Aluno
    from models.professor import Professor
    from models.curso import Curso
    from models.disciplina import Disciplina
    from models.matricula import Matricula
    from models.historicoacademico import HistoricoAcademico
    from models.matriculapagadisciplina import MatriculaPagaDisciplina
    from models.pessoa import Pessoa

# Importar serializadores
from utils.serializador import (
    serealizar_aluno, serializar_professor, serealizar_curso,
    serealizar_disciplina, serealizar_historico,
    serializar_matricula, serializar_mpd, serializar_pessoa
)

# Importar desserializadores e função central
from utils.desserializar import (
    desserializar_aluno, desserializar_professor, desserializar_curso,
    desserializar_disciplina, desserializar_historico,
    desserializar_matricula, desserializar_mpd,
    carregar_tudo
)


class SistemaAcademico:

    def __init__(self, arquivos_dados: dict = None):
        # Estruturas de dados principais
        self.alunos: Dict[str, "Aluno"] = {}
        self.professores: Dict[str, "Professor"] = {}
        self.cursos: Dict[str, "Curso"] = {}
        self.disciplinas: Dict[str, "Disciplina"] = {}
        self.historicos_academicos: Dict[str, "HistoricoAcademico"] = {}
        self.matriculas: Dict[int, "Matricula"] = {}
        self.matriculas_pagas_disciplinas: Dict[str, "MatriculaPagaDisciplina"] = {}

        # Arquivo de persistência
        self.arquivos_dados = arquivos_dados if arquivos_dados else {
            "principal": "persistence/dados/sistema_academico.json"
        }

        # Gerenciador de Arquivos
        self.gerenciador = GerenciadorArquivos(self.arquivos_dados)

        # Carregar dados ao iniciar sistema
        self.carregar_dados()

    # GETTERS DO SISTEMA
   
    def get_alunos(self) -> Dict[str, "Aluno"]:
        return self.alunos

    def get_professores(self) -> Dict[str, "Professor"]:
        return self.professores

    def get_cursos(self) -> Dict[str, "Curso"]:
        return self.cursos

    def get_disciplinas(self) -> Dict[str, "Disciplina"]:
        return self.disciplinas

    def get_historicos_academicos(self) -> Dict[str, "HistoricoAcademico"]:
        return self.historicos_academicos

    def get_matriculas(self) -> Dict[int, "Matricula"]:
        return self.matriculas

    def get_matriculas_pagas_disciplinas(self) -> Dict[str, "MatriculaPagaDisciplina"]:
        return self.matriculas_pagas_disciplinas

    # SALVAR DADOS
   
    def salvar_dados(self) -> None:
        print("🔄 Serializando dados...")

        dados_serializados = {
            "alunos": [serealizar_aluno(a) for a in self.alunos.values()],
            "professores": [serializar_professor(p) for p in self.professores.values()],
            "cursos": [serealizar_curso(c) for c in self.cursos.values()],
            "disciplinas": [serealizar_disciplina(d) for d in self.disciplinas.values()],
            "historicos_academicos": [serealizar_historico(h) for h in self.historicos_academicos.values()],
            "matriculas": [serializar_matricula(m) for m in self.matriculas.values()],
            "matriculas_pagas_disciplinas": [serializar_mpd(mpd) for mpd in self.matriculas_pagas_disciplinas.values()],
        }

        try:
            self.gerenciador.salvar(dados_serializados)
            print("💾 Dados salvos com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")

    # CARREGAR DADOS

    def carregar_dados(self) -> None:
        dados_json = self.gerenciador.carregar()

        if not dados_json:
            print("📁 Nenhum dado encontrado. Sistema iniciado vazio.")
            return

        print("📥 Dados carregados. Reconstruindo objetos...")

        try:
            alunos, cursos, disciplinas, professores, matriculas, historicos, mpds = carregar_tudo(
                dados_json.get("alunos", []),
                dados_json.get("cursos", []),
                dados_json.get("disciplinas", []),
                dados_json.get("professores", []),
                dados_json.get("matriculas", []),
                dados_json.get("historicos_academicos", []),
                dados_json.get("matriculas_pagas_disciplinas", [])
            )

            # Atualiza o estado do sistema
            self.alunos = alunos
            self.cursos = cursos
            self.disciplinas = disciplinas
            self.professores = professores
            self.matriculas = matriculas
            self.historicos_academicos = historicos
            self.matriculas_pagas_disciplinas = mpds

            print(f"✔ Sistema reconstruído com sucesso!")
            print(f"   Alunos: {len(self.alunos)}")
            print(f"   Cursos: {len(self.cursos)}")
            print(f"   Disciplinas: {len(self.disciplinas)}")
            print(f"   Professores: {len(self.professores)}")
            print(f"   Matrículas: {len(self.matriculas)}")
            print(f"   MPDs: {len(self.matriculas_pagas_disciplinas)}")

        except Exception as e:
            print(f"❌ Erro crítico ao carregar dados: {e}")
            print("⚠ Sistema iniciado vazio para evitar falhas.")
            self.__init__({})  # reset seguro