import datetime

class MatriculaPagaDisciplina:
    def __init__(self, aluno, disciplina, data_matricula:datetime.date, valor:float, status:str):
        self.__aluno = aluno
        self.__disciplina = disciplina
        self.__data_matricula = data_matricula
        self.__valor = valor
        self.__status = status

#getters
    def get_aluno(self):
        return self.__aluno
    
    def get_disciplina(self):
        return self.__disciplina
    
    def get_data_matricula(self):
        return self.__data_matricula
    
    def get_valor(self):
        return self.__valor
    
    def get_status(self):
        return self.__status

#setters
    def set_status(self, status:str):
        self.__status = status

    def set_valor(self, valor:float):
        self.__valor = valor

#metódos
    def exibir_detalhes(self) -> str:
        nome_aluno = self.__aluno.get_nome() if self.__aluno else "Aluno não definido"
        nome_disciplina = self.__disciplina.get_nome() if self.__disciplina else "Disciplina não definida"
        data = self.__data_matricula.strftime('%d/%m/%Y') if hasattr(self.__data_matricula, 'strftime') else str(self.__data_matricula)
        detalhes = (
            f"Aluno: {nome_aluno}\n"
            f"Disciplina: {nome_disciplina}\n"
            f"Data da matrícula: {data}\n"
            f"Valor: R${self.__valor:.2f}\n"
            f"Status: {self.__status}"
        )
        return detalhes
