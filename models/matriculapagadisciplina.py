from disciplina import Disciplina
from matricula import Matricula
from historicoacademico import HistoricoAcademico
from typing import List


class MatriculaPagaDisciplina:
    def __init__(self, matricula: "Matricula", disciplina: "Disciplina", notas: List[float], faltas: int,
                  historico_acad: 'HistoricoAcademico' = None):
        
        self.__matricula = matricula
        self.__disciplina = disciplina
        self.__notas = notas
        self.__faltas = faltas
        self.__media_final = self.calcular_media_final() 
        self.__historico_acad = historico_acad
        

# getters
    def get_matricula(self) -> Matricula:
        return self.__matricula

    def get_disciplina(self) -> Disciplina:
        return self.__disciplina

    def get_notas(self) -> List[float]:
        return self.__notas

    def get_media_final(self) -> float:
        return self.__media_final

    def get_faltas(self) -> int:
        return self.__faltas
    
    def get_historico_acad(self) -> 'HistoricoAcademico':
        return self.__historico_acad

    
# métodos 
    def calcular_media_final(self) -> float:
        if not self.__notas:
            media = 0.0
        else:
            media = sum(self.__notas) / len(self.__notas)
            
        self.__media_final = media # Atualiza o atributo privado
        return self.__media_final

    def verificar_faltas(self, max_faltas: int) -> bool:
        return self.__faltas > max_faltas

    def verificar_aprovacao(self, media_minima: float = 7.0, max_faltas: int = 20) -> str:
        media = self.get_media_final()
        
        if self.verificar_faltas(max_faltas):
             return "REPROVADO POR FALTA"
        elif media >= media_minima:
             return "APROVADO"
        else:
             return "REPROVADO POR NOTA"
        
#média minima para a final. se for menor reprova por nota se maior vai para fnal (média =nota final)\ 2 = 7) caso não = reprovado por nota
"""
inclusive outras situações para verificar a final se quiser ver se o caba é laureavél também tá ligado 

USAR O RICH, BAIXANDO NO AMBIENTE VIRTUAL DO TERMINAL MESMO PARA DEIXAR BONITÃO

"""