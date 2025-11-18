import datetime
from pessoa import Pessoa
from curso import Curso

class Aluno(Pessoa):
    def __init__(self, nome:str, email:str, data_nascimento:datetime.date, telefone:str, endereco:str,
                 matricula:str, periodo_atual:int, email_institucional:str, curso: "Curso", creditos_concluidos:int):
        super().__init__(nome, email, data_nascimento, telefone, endereco)
        self.__matricula = matricula
        self.__periodo_atual = periodo_atual
        self.__email_institucional = email_institucional
        self.__curso = curso
        self.__creditos_concluidos = creditos_concluidos

    def get_matricula(self):
        return self.__matricula

    def get_periodo_atual(self):
        return self.__periodo_atual

    def get_email_institucional(self):
        return self.__email_institucional

    def get_curso(self):
        return self.__curso
    
    def get_creditos_concluidos(self):
        return self.__creditos_concluidos
    
    #setter para periodo



    def exibir_informacoes(self) -> str:
        detalhes_pessoa = self.exibir_detalhes()
        nome_curso = self.__curso.get_nome() if hasattr(self.__curso, 'get_nome') else "Curso ID: " + self.__curso.get_codigo()
        
        detalhes_aluno = (
            f"\nMatrícula: {self.__matricula}\n"
            f"Período atual: {self.__periodo_atual}\n"
            f"E-mail institucional: {self.__email_institucional}\n"
            f"Curso: {nome_curso}"
        )
        return detalhes_pessoa + detalhes_aluno
    
    def atualizar_creditos(self, creditos:int):
        self.__creditos_concluidos += creditos

    
