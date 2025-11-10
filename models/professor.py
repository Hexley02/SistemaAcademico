import datetime
from pessoa import Pessoa
from disciplina import Disciplina


class Professor(Pessoa):
    def __init__(self, nome:str, email:str, data_nascimento:datetime.date, telefone:str, endereco:str,
                 codigo:int, departamento:str, disciplinas:Disciplina, email_institucional:str, titulo:str):
        super().__init__(nome, email, data_nascimento, telefone, endereco)
        self.__codigo = codigo
        self.__departamento = departamento
        self.__disciplinas = disciplinas
        self.__email_institucional = email_institucional
        self.__titulo = titulo

    #getters
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

    #setters
    def set_departamento(self, departamento:str):
        self.__departamento = departamento

    def set_titulo(self, titulo:str):
        self.__titulo = titulo

    # métodos
    def exibir_detalhes(self):
        detalhes_pessoa = super().exibir_detalhes()

        if not self.__disciplinas:
            disciplina_nome = "Nenhuma"
        else:
            # Se for um iterável (lista/tupla) e não uma string, junta os nomes
            if hasattr(self.__disciplinas, '__iter__') and not isinstance(self.__disciplinas, (str, bytes)):
                nomes = []
                for d in self.__disciplinas:
                    if hasattr(d, 'get_nome'):
                        nomes.append(d.get_nome())
                    else:
                        nomes.append(str(d))
                disciplina_nome = ", ".join(nomes) if nomes else "Nenhuma"
            else:
                # trata como objeto único
                disciplina_nome = self.__disciplinas.get_nome() if hasattr(self.__disciplinas, 'get_nome') else str(self.__disciplinas)

        detalhes_professor = (
            f"\n--- Detalhes do Professor ---\n"
            f"Código: {self.__codigo}\n"
            f"Departamento: {self.__departamento}\n"
            f"Disciplina: {disciplina_nome}\n"
            f"E-mail institucional: {self.__email_institucional}\n"
            f"Título: {self.__titulo}"
        )
        return detalhes_pessoa + detalhes_professor

    