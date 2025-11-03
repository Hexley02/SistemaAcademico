class HistoricoAcademico:
    def __init__(self, aluno, registros:list):
        self.__aluno = aluno
        self.__registros = registros

#getters
    def get_aluno(self):
        return self.__aluno

    def get_registros(self):
        return self.__registros

#setters
    def set_registros(self, registros:list):
        self.__registros = registros

#metódos
    def adicionar_registro(self, disciplina, nota:float, situacao:str):
        self.__registros.append({
            "disciplina": disciplina,
            "nota": nota,
            "situacao": situacao
        })

    def exibir_detalhes(self) -> str:
        nome_aluno = self.__aluno.get_nome() if self.__aluno else "Aluno não definido"
        detalhes_registros = ""
        if self.__registros:
            for registro in self.__registros:
                nome_disc = registro["disciplina"].get_nome() if registro["disciplina"] else "Desconhecida"
                detalhes_registros += (
                    f"\nDisciplina: {nome_disc}\n"
                    f"Nota: {registro['nota']}\n"
                    f"Situação: {registro['situacao']}\n"
                )
        else:
            detalhes_registros = "Nenhum registro encontrado."
        detalhes = (
            f"Histórico Acadêmico do aluno: {nome_aluno}\n"
            f"{detalhes_registros}"
        )
        return detalhes
