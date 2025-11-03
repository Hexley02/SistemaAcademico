import datetime

class Matricula:
    def __init__(self, aluno, data_matricula:datetime.date, matriculas_pagas:list):
        self.__aluno = aluno
        self.__data_matricula = data_matricula
        self.__matriculas_pagas = matriculas_pagas

#getters
    def get_aluno(self):
        return self.__aluno

    def get_data_matricula(self):
        return self.__data_matricula

    def get_matriculas_pagas(self):
        return self.__matriculas_pagas

#setters
    def set_matriculas_pagas(self, matriculas_pagas:list):
        self.__matriculas_pagas = matriculas_pagas

#metódos
    def adicionar_matricula_paga(self, matricula_paga):
        self.__matriculas_pagas.append(matricula_paga)

    def remover_matricula_paga(self, matricula_paga):
        if matricula_paga in self.__matriculas_pagas:
            self.__matriculas_pagas.remove(matricula_paga)

    def exibir_detalhes(self) -> str:
        nome_aluno = self.__aluno.get_nome() if self.__aluno else "Aluno não definido"
        data = self.__data_matricula.strftime('%d/%m/%Y') if hasattr(self.__data_matricula, 'strftime') else str(self.__data_matricula)
        lista_matriculas = ', '.join([m.get_disciplina().get_nome() for m in self.__matriculas_pagas]) if self.__matriculas_pagas else "Nenhuma disciplina"
        detalhes = (
            f"Aluno: {nome_aluno}\n"
            f"Data da matrícula: {data}\n"
            f"Disciplinas matriculadas: {lista_matriculas}"
        )
        return detalhes
