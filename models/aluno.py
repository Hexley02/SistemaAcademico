import datetime
from pessoa import Pessoa

class Aluno(Pessoa):
    def __init__(self, nome:str, email:str, data_nascimento:datetime.date, telefone:str, endereco:str,
                 matricula:str, periodo_atual:int, email_institucional:str, curso:str):
        super().__init__(nome, email, data_nascimento, telefone, endereco)
        self.__matricula = matricula
        self.__periodo_atual = periodo_atual
        self.__email_institucional = email_institucional
        self.__curso = curso

    def get_matricula(self):
        return self.__matricula

    def get_periodo_atual(self):
        return self.__periodo_atual

    def get_email_institucional(self):
        return self.__email_institucional

    def get_curso(self):
        return self.__curso

    def set_periodo_atual(self, periodo_atual:int):
        self.__periodo_atual = periodo_atual

    def set_email_institucional(self, email_institucional:str):
        self.__email_institucional = email_institucional

    def set_curso(self, curso:str):
        self.__curso = curso

    def exibir_informacoes(self) -> str:
        detalhes_pessoa = self.exibir_detalhes()
        detalhes_aluno = (
            f"\nMatrícula: {self.__matricula}\n"
            f"Período atual: {self.__periodo_atual}\n"
            f"E-mail institucional: {self.__email_institucional}\n"
            f"Curso: {self.__curso}"
        )
        return detalhes_pessoa + detalhes_aluno
