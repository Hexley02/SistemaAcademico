from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.disciplina import Disciplina
    from models.matricula import Matricula
    from models.historicoacademico import HistoricoAcademico


class MatriculaPagaDisciplina:
    def __init__(self, matricula: "Matricula", disciplina: "Disciplina", notas: List[float], faltas: int,
                  historico_acad: 'HistoricoAcademico' = None, nota_final: float = None):
        
        self.__matricula = matricula
        self.__disciplina = disciplina
        self.__notas = notas
        self.__faltas = faltas
        self.__media_final = self.calcular_media_final() 
        self.__historico_acad = historico_acad
        self.__nota_final = nota_final

    # getters
    def get_matricula(self) -> "Matricula":
        return self.__matricula

    def get_disciplina(self) -> "Disciplina":
        return self.__disciplina

    def get_notas(self) -> List[float]:
        return self.__notas

    def get_media_final(self) -> float:
        return self.__media_final

    def get_faltas(self) -> int:
        return self.__faltas
    
    def get_historico_acad(self) -> 'HistoricoAcademico':
        return self.__historico_acad
    
    def get_nota_final(self) -> float:
        return self.__nota_final
    
    def get_creditos_disciplina(self) -> int:
        """Retorna os créditos da disciplina (necessário para cálculo do IRA)"""
        # Assumindo que a disciplina tem um método get_creditos ou similar
        # Se não tiver, você precisará adicionar esse atributo na classe Disciplina
        if hasattr(self.__disciplina, 'get_creditos'):
            return self.__disciplina.get_creditos()
        return 4  # valor padrão caso não tenha
    
    # setter
    def set_nota_final(self, nota: float) -> None:
        if 0.0 <= nota <= 10.0:
            self.__nota_final = nota
        else:
            raise ValueError("A nota final deve estar entre 0.0 e 10.0")

    # métodos 
    def calcular_media_final(self) -> float:
        if not self.__notas:
            media = 0.0
        else:
            media = sum(self.__notas) / len(self.__notas)
            
        self.__media_final = media  # Atualiza o atributo privado
        return self.__media_final

    def verificar_faltas(self, max_faltas: int) -> bool:
        return self.__faltas > max_faltas

    def verificar_aprovacao(self, media_minima: float = 7.0, media_limite_final: float = 4.0, 
                          media_aprovacao_final: float = 5.0, max_faltas: int = 20) -> str:
        
        media_regular = self.get_media_final()
        
        # 1. Reprovado por Falta (Prioridade Máxima)
        if self.verificar_faltas(max_faltas):
            return "REPROVADO POR FALTA"
            
        # 2. APROVADO Direto (Média >= 7.0)
        elif media_regular >= media_minima:
            return "APROVADO"
        
        # 3. Vai para EXAME FINAL (Média >= 4.0 e < 7.0)
        elif media_regular >= media_limite_final and media_regular < media_minima:
            
            # Se a nota da final já estiver lançada, verifica o resultado PÓS-FINAL
            if self.__nota_final is not None:
                media_pos_final = self.calcular_media_pos_final()
                
                if media_pos_final >= media_aprovacao_final:
                    return "APROVADO PÓS-FINAL"
                else:
                    return "REPROVADO POR NOTA PÓS-FINAL"
            else:
                return "EXAME FINAL PENDENTE"  # Aluno elegível, mas nota da final não lançada
            
        # 4. Reprovado por Nota Direto (Média < 4.0)
        else:
            return "REPROVADO POR NOTA"
        
    def calcular_media_pos_final(self, media_aprovacao_final: float = 5.0) -> float:
        if self.__nota_final is None:
            return 0.0
        
        media_anterior = self.get_media_final()
        media_pos_final = (media_anterior + self.__nota_final) / 2

        return media_pos_final