# utils/serializador.py
import datetime
from models.aluno import Aluno 
from models.curso import Curso
from models.disciplina import Disciplina
from models.historicoacademico import HistoricoAcademico
from models.matricula import Matricula
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.professor import Professor
from models.pessoa import Pessoa

# ============================================================
# SERIALIZAR PESSOA
# ============================================================
def serializar_pessoa(pessoa: Pessoa) -> dict:
    return {
        "nome": pessoa.get_nome(),
        "email": pessoa.get_email(),
        "data_nascimento": pessoa.get_data_nascimento().isoformat(),
        "telefone": pessoa.get_telefone(),
        "endereco": pessoa.get_endereco()
    }

# ============================================================
# SERIALIZAR ALUNO
# ============================================================
def serealizar_aluno(aluno: Aluno) -> dict:
    dados = serializar_pessoa(aluno)

    dados.update({
        "matricula": aluno.get_matricula(),
        "periodo_atual": aluno.get_periodo_atual(),
        "email_institucional": aluno.get_email_institucional(),
        "creditos_concluidos": aluno.get_creditos_concluidos(),
        "curso_codigo": aluno.get_curso().get_codigo() if aluno.get_curso() else None
    })

    return dados

serializar_aluno = serealizar_aluno  # Alias compatível


# ============================================================
# SERIALIZAR PROFESSOR
# ============================================================
def serializar_professor(professor: Professor) -> dict:
    dados = serializar_pessoa(professor)
    
    dados.update({
        "codigo": professor.get_codigo(),
        "departamento": professor.get_departamento(),
        "email_institucional": professor.get_email_institucional(),
        "titulo": professor.get_titulo(),
        "disciplinas_codigos": [
            d.get_codigo() for d in (professor.get_disciplinas() or [])
        ]
    })
    
    return dados


# ============================================================
# SERIALIZAR CURSO
# ============================================================
def serealizar_curso(curso: Curso) -> dict:
    return {
        "codigo": curso.get_codigo(),
        "periodo": curso.get_periodo(),
        "turno": curso.get_turno(),
        "avaliacao_curso": curso.get_avaliacao_curso(),
        "disciplinas_codigos": [
            d.get_codigo() for d in (curso.get_disciplinas() or [])
        ]
    }

serializar_curso = serealizar_curso


# ============================================================
# SERIALIZAR DISCIPLINA
# ============================================================
def serealizar_disciplina(disciplina: Disciplina) -> dict:
    return {
        "codigo": disciplina.get_codigo(),
        "nome": disciplina.get_nome(),
        "periodo": disciplina.get_período(),
        "professor_responsavel_id": disciplina.get_professor_responsavel().get_codigo()
                                   if disciplina.get_professor_responsavel() else None,
        "alunos_matriculas": [
            a.get_matricula() for a in (disciplina.get_alunos() or [])
        ]
    }

serializar_disciplina = serealizar_disciplina


# ============================================================
# SERIALIZAR HISTÓRICO
# ============================================================
def serializar_historico(h: HistoricoAcademico) -> dict:
    return {
        "matricula_aluno_id": h.get_matricula_aluno().get_matricula()
                              if h.get_matricula_aluno() else None,
        "data_emissao": h.get_data_emissao().isoformat(),
        "quantidade_creditos": h.get_quantidade_creditos(),
        "lista_atividades_complementares": h.get_lista_atividades_complementares(),
        "registros_disciplinas": [
            serializar_mpd(r) for r in (h.get_registros_disciplinas() or [])
        ]
    }

serealizar_historico = serializar_historico  # Alias compatível


# ============================================================
# SERIALIZAR MATRÍCULA
# ============================================================
def serializar_matricula(matricula: Matricula) -> dict:
    # Pegar histórico do aluno
    aluno = matricula.get_aluno()
    historico_id = None
    if aluno:
        # Assumindo que o ID do histórico é a matrícula do aluno
        historico_id = aluno.get_matricula()
    
    return {
        "id_matricula": matricula.get_id_matricula(),
        "status": matricula.get_status(),
        "aluno_matricula_id": aluno.get_matricula() if aluno else None,
        "historico_academico_id": historico_id,
        "registros_disciplinas": [
            serializar_mpd(r) for r in (matricula.get_registros_disciplinas() or [])
        ]
    }


# ============================================================
# SERIALIZAR MPD (MatriculaPagaDisciplina)
# ============================================================
def serializar_matricula_paga_disciplina(mpd: MatriculaPagaDisciplina) -> dict:
    matricula = mpd.get_matricula()
    disciplina = mpd.get_disciplina()

    matricula_id = matricula.get_id_matricula() if matricula else None
    disciplina_id = disciplina.get_codigo() if disciplina else None

    # ID estável (melhor forma possível)
    id_mpd = f"{matricula_id}_{disciplina_id}"

    return {
        "id_mpd": id_mpd,
        "matricula_id": matricula_id,
        "disciplina_id": disciplina_id,
        "historico_id": (
            mpd.get_historico_acad().get_matricula_aluno().get_matricula()
            if mpd.get_historico_acad() and mpd.get_historico_acad().get_matricula_aluno() else None
        ),
        "notas": mpd.get_notas(),
        "faltas": mpd.get_faltas(),
        "media_final": mpd.get_media_final(),
        "nota_final": mpd.get_nota_final()
    }

serializar_mpd = serializar_matricula_paga_disciplina