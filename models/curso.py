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

    #set periodo

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
        
        if d not in self.__disciplinas:
            self.__disciplinas.append(d)
            disc_nome = d.get_nome() if hasattr(d, 'get_nome') else "Nova"
            print(f"Disciplina '{disc_nome}' adicionada ao curso {self.__codigo}.")
        else:
            print(f"Disciplina já existe neste curso.")

    def remover_disciplina(self, d: 'Disciplina'):
        
        if d in self.__disciplinas:
            self.__disciplinas.remove(d)
            disc_nome = d.get_nome() if hasattr(d, 'get_nome') else "Disciplina"
            print(f"Disciplina '{disc_nome}' removida do curso {self.__codigo}.")
        else:
            print(f"Disciplina não encontrada na grade curricular.")