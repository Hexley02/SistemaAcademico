from aluno import Aluno
from historicoacademico import HistoricoAcademico
from matriculapagadisciplina import MatriculaPagaDisciplina
from typing import List 

class Matricula:
    def __init__(self, id_matricula: int, aluno: "Aluno", 
                 historico_academico: 'HistoricoAcademico', status: bool,
                 registros_disciplinas: List['MatriculaPagaDisciplina'] = None):
        
        self.__id_matricula = id_matricula
        self.__aluno = aluno
        self.__historico_academico = historico_academico
        self.__status = status
        self.__registros_disciplinas = registros_disciplinas if registros_disciplinas is not None else []


# Getters

    def get_id_matricula(self) -> int:
        return self.__id_matricula

    def get_aluno(self) -> 'Aluno':
        return self.__aluno
    
    def get_historico_academico(self) -> 'HistoricoAcademico':
        return self.__historico_academico
    
    def get_status(self) -> bool:
        return self.__status

    def get_registros_disciplinas(self) -> List['MatriculaPagaDisciplina']:
        return self.__registros_disciplinas
    
    def set_status(self, status: bool):
        self.__status = status


# Métodos

    def alterar_matricula(self, novo_status: bool = None):
        
        if novo_status is not None:
            self.set_status(novo_status)
            status_str = "ATIVA" if novo_status else "TRANCADA/CANCELADA"
            aluno_nome = self.__aluno.get_nome() if hasattr(self.__aluno, 'get_nome') else "Aluno"
            
            print(f"Status da Matrícula {self.__id_matricula} de {aluno_nome} alterado para: **{status_str}**.")


    def adicionar_registro_disciplina(self, registro_pd: 'MatriculaPagaDisciplina'):
        """ Adiciona um registro detalhado de notas e faltas (Agregação). """
        if registro_pd not in self.__registros_disciplinas:
            self.__registros_disciplinas.append(registro_pd)
            print(f"Registro detalhado adicionado à Matrícula {self.__id_matricula}.")
        else:
            print("Este registro já existe nesta matrícula.")
            
   