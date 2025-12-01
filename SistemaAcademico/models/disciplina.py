from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.aluno import Aluno
    from models.professor import Professor

class Disciplina:
    def __init__(self, codigo: int, período: int, nome: str, professor_responsavel: "Professor", alunos: List["Aluno"],
                 creditos_disciplina:int = 4):
        self.__codigo = codigo
        self.__nome = nome
        self.__período = período
        self.__professor_responsavel = professor_responsavel
        self.__alunos = alunos if alunos is not None else []
        self.__creditos_disciplina = creditos_disciplina

    # getters
    def get_codigo(self) -> int:
        return self.__codigo
    
    def get_nome(self) -> str:
        return self.__nome
    
    def get_período(self) -> int:
        return self.__período
    
    def get_professor_responsavel(self) -> "Professor":
        return self.__professor_responsavel
    
    def get_alunos(self) -> List["Aluno"]:
        return self.__alunos
    
    def get_creditos_disciplina(self) -> int:
        return self.__creditos_disciplina
    

    # setters
    def set_nome(self, nome: str) -> None:
        self.__nome = nome
         
    def set_professor_responsavel(self, professor: "Professor") -> None:
        self.__professor_responsavel = professor

    def set_periodo(self, período: int) -> None:
        self.__período = período

    # métodos
    def adicionar_aluno(self, aluno: "Aluno") -> None:
        self.__alunos.append(aluno)
    
    def remover_aluno(self, aluno: "Aluno") -> None:
        if aluno in self.__alunos:
            self.__alunos.remove(aluno)

    def exibir_detalhes(self) -> str:
        professor = self.__professor_responsavel.get_nome() if self.__professor_responsavel else "Sem professor"
        nomes_alunos = ', '.join([a.get_nome() for a in self.__alunos]) if self.__alunos else "Sem alunos"
        detalhes = (
            f"Código: {self.__codigo}\n"
            f"Nome: {self.__nome}\n"
            f"Período: {self.__período}\n"
            f"Professor responsável: {professor}\n"
            f"Alunos: {nomes_alunos}"
            f"\nCréditos da Disciplina: {self.__creditos_disciplina}"
        )
        return detalhes