import datetime
from typing import List, TYPE_CHECKING

from models.pessoa import Pessoa

if TYPE_CHECKING:
    from models.disciplina import Disciplina


class Professor(Pessoa):
    def __init__(self, nome: str, email: str, data_nascimento: datetime.date, telefone: str, endereco: str,
                 codigo: int, departamento: str, disciplinas: List["Disciplina"], email_institucional: str, titulo: str):
        super().__init__(nome, email, data_nascimento, telefone, endereco)
        self.__codigo = codigo
        self.__departamento = departamento
        self.__disciplinas = disciplinas if disciplinas is not None else []
        self.__email_institucional = email_institucional
        self.__titulo = titulo

    # getters
    def get_codigo(self) -> int:
        return self.__codigo

    def get_departamento(self) -> str:
        return self.__departamento

    def get_disciplinas(self) -> List["Disciplina"]:
        return self.__disciplinas

    def get_email_institucional(self) -> str:
        return self.__email_institucional

    def get_titulo(self) -> str:
        return self.__titulo

    # setters
    def set_departamento(self, departamento: str) -> None:
        self.__departamento = departamento

    def set_titulo(self, titulo: str) -> None:
        self.__titulo = titulo

    # métodos
    def exibir_detalhes(self) -> str:
        detalhes_pessoa = super().exibir_detalhes()

        if not self.__disciplinas:
            disciplina_nome = "Nenhuma"
        else:
            nomes = []
            for d in self.__disciplinas:
                if hasattr(d, 'get_nome'):
                    nomes.append(d.get_nome())
                else:
                    nomes.append(str(d))
            disciplina_nome = ", ".join(nomes) if nomes else "Nenhuma"

        detalhes_professor = (
            f"\n--- Detalhes do Professor ---\n"
            f"Código: {self.__codigo}\n"
            f"Departamento: {self.__departamento}\n"
            f"Disciplina: {disciplina_nome}\n"
            f"E-mail institucional: {self.__email_institucional}\n"
            f"Título: {self.__titulo}"
        )
        return detalhes_pessoa + detalhes_professor
    
    def alocar_disciplinas(self, disciplina: "Disciplina") -> None:

        try:
            disc_codigo = disciplina.get_codigo()
            disc_nome = disciplina.get_nome()
            
        except AttributeError:
            raise TypeError("Erro: O objeto fornecido não é uma Disciplina válida (falta get_codigo()).")

        if disciplina in self.__disciplinas:
            raise ValueError(f"A Disciplina '{disc_nome}' (Código {disc_codigo}) já está alocada a este professor.")
        
        self.__disciplinas.append(disciplina)
        print(f"Disciplina '{disc_nome}' alocada ao Professor {self.get_nome()} com sucesso.")
    

    def remover_disciplinas(self, disciplina: "Disciplina") -> None:

        try:
            disc_codigo = disciplina.get_codigo()
            disc_nome = disciplina.get_nome()   

        except AttributeError:
            raise TypeError("Erro: O objeto fornecido não é uma Disciplina válida (falta get_codigo()).")
        
        if disciplina in self.__disciplinas:
            self.__disciplinas.remove(disciplina)
            print(f"Disciplina '{disc_nome}' removida do Professor {self.get_nome()} com sucesso.")
        else:
            raise ValueError(f"A Disciplina '{disc_nome}' (Código {disc_codigo}) não está alocada a este professor.")