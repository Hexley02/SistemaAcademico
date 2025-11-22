from disciplina import Disciplina
from typing import List

class Curso:
    def __init__(self, codigo: str, disciplinas: List['Disciplina'], 
                 periodo: int, turno: str, avaliacao_curso: float):
        
        self.__codigo = codigo
        self.__disciplinas = disciplinas if disciplinas is not None else []
        self.__periodo = periodo
        self.__turno = turno
        self.__avaliacao_curso = avaliacao_curso 
        
      

    #getters

    def get_codigo(self) -> str:
        return self.__codigo

    def get_disciplinas(self) -> List['Disciplina']:
        return self.__disciplinas

    def get_periodo(self) -> int:
        return self.__periodo
    
    def get_turno(self) -> str:
        return self.__turno
    
    def get_avaliacao_curso(self) -> float:
        return self.__avaliacao_curso

    #setters

    def set_turno(self, turno: str):
        self.__turno = turno

    def set_avaliacao_curso(self, avaliacao_curso: float):
        self.__avaliacao_curso = avaliacao_curso

    def set_periodo(self, periodo: int):
        self.__periodo = periodo

    #métodos
    
    def exibir_informacoes(self):
        
        disciplinas_count = len(self.__disciplinas)
        
        print(f"\n=== Detalhes do Curso ({self.__codigo}) ===")
        print(f"Código: {self.__codigo}")
        print(f"Turno: {self.__turno}")
        print(f"Duração Total: {self.__periodo} períodos")
        print(f"Avaliação Institucional: {self.__avaliacao_curso:.2f}")
        print(f"Total de Disciplinas na Grade: {disciplinas_count}")

    def adicionar_disciplina(self, d: 'Disciplina'):
        try:
           
            disc_codigo = d.get_codigo()
            disc_nome = d.get_nome()
        except AttributeError:
           
            raise TypeError(f"Erro: O objeto fornecido não é uma Disciplina válida (falta get_nome() ou get_codigo()).")

        # Se a disciplina for válida, segue a lógica de negócio
        if d not in self.__disciplinas:
            self.__disciplinas.append(d)
            print(f"Disciplina '{disc_nome}' (Código {disc_codigo}) adicionada ao curso {self.__codigo}.")
        else:
          
            raise ValueError(f"Disciplina '{disc_nome}' já existe neste curso.")
        
    def remover_disciplina(self, d: 'Disciplina'):
        try:
            disc_nome = d.get_nome()
            disc_codigo = d.get_codigo()
            
        except AttributeError:
            raise TypeError(f"Erro: O objeto fornecido não é uma Disciplina válida (falta get_nome() ou get_codigo()).")

        if d in self.__disciplinas:
            self.__disciplinas.remove(d)
            print(f"Disciplina '{disc_nome}' (Código {disc_codigo}) removida do curso {self.__codigo}.")
        else:
            # Esta é a exceção de negócio (a disciplina não existe)
            raise ValueError(f"Disciplina '{disc_nome}' não encontrada na grade curricular.")