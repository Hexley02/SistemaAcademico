import datetime
from pessoa import Pessoa

class Professor(Pessoa):
    def __init__(self, nome:str, email:str, data_nascimento:datetime.date, telefone:str, endereco:str,
                 codigo:int, departamento:str, disciplinas:list, email_institucional:str, titulo:str):
        super().__init__(nome, email, data_nascimento, telefone, endereco)
        self.__codigo = codigo
        self.__departamento = departamento
        self.__disciplinas = disciplinas
        self.__email_institucional = email_institucional
        self.__titulo = titulo

    def get_codigo(self):
        return self.__codigo

    def get_departamento(self):
        return self.__departamento

    def get_disciplinas(self):
        return self.__disciplinas

    def get_email_institucional(self):
        return self.__email_institucional

    def get_titulo(self):
        return self.__titulo

    def set_departamento(self, departamento:str):
        self.__departamento = departamento

    def set_email_institucional(self, email_institucional:str):
        self.__email_institucional = email_institucional

    def set_titulo(self, titulo:str):
        self.__titulo = titulo

    def set_disciplinas(self, disciplinas:list):
        self.__disciplinas = disciplinas

    def exibir_informacoes(self) -> str:
        detalhes_pessoa = self.exibir_detalhes()
        detalhes_professor = (
            f"\nCódigo: {self.__codigo}\n"
            f"Departamento: {self.__departamento}\n"
            f"Disciplinas: {', '.join(self.__disciplinas) if self.__disciplinas else 'Nenhuma'}\n"
            f"E-mail institucional: {self.__email_institucional}\n"
            f"Título: {self.__titulo}"
        )
        return detalhes_pessoa + detalhes_professor
