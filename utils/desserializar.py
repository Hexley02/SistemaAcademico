# utils/desserializar.py
from models.aluno import Aluno
from models.professor import Professor
from models.curso import Curso
from models.disciplina import Disciplina
from models.matricula import Matricula
from models.historicoacademico import HistoricoAcademico
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.pessoa import Pessoa

import datetime

# ============================================================
# FUNÇÕES DE DESSERIALIZAÇÃO SIMPLES
# ============================================================

def desserializar_pessoa(d: dict) -> Pessoa:
    p = Pessoa(
        d["nome"],
        d["email"],
        datetime.date.fromisoformat(d["data_nascimento"]),
        d["telefone"],
        d["endereco"]
    )
    return p


def desserializar_aluno(d: dict) -> Aluno:
    p = desserializar_pessoa(d)
    aluno = Aluno(
        p.get_nome(), p.get_email(), p.get_data_nascimento(),
        p.get_telefone(), p.get_endereco(),
        d["matricula"], d["periodo_atual"],
        d["email_institucional"], d["creditos_concluidos"]
    )

    aluno._curso_codigo_temp = d["curso_codigo"]
    return aluno


def desserializar_professor(d: dict) -> Professor:
    p = desserializar_pessoa(d)
    prof = Professor(
        p.get_nome(), p.get_email(), p.get_data_nascimento(),
        p.get_telefone(), p.get_endereco(),
        d["codigo"], d["departamento"],
        d["email_institucional"], d["titulo"]
    )
    prof._disciplinas_temp = d.get("disciplinas_codigos", [])
    return prof


def desserializar_curso(d: dict) -> Curso:
    c = Curso(d["codigo"], d["periodo"], d["turno"], d["avaliacao_curso"])
    c._disciplinas_temp = d.get("disciplinas_codigos", [])
    return c


def desserializar_disciplina(d: dict) -> Disciplina:
    disc = Disciplina(d["codigo"], d["nome"], d["periodo"])
    disc._prof_temp = d.get("professor_responsavel_id")
    disc._alunos_temp = d.get("alunos_matriculas", [])
    return disc


def desserializar_historico(d: dict) -> HistoricoAcademico:
    h = HistoricoAcademico(
        matricula_aluno=None,
        quantidade_creditos=d["quantidade_creditos"],
        atividades=d["lista_atividades_complementares"]
    )

    h._matricula_temp = d["matricula_aluno_id"]
    h._registros_temp = d.get("registros_disciplinas", [])
    h._data_temp = d["data_emissao"]
    return h


def desserializar_matricula(d: dict) -> Matricula:
    m = Matricula(
        id_matricula=d["id_matricula"],
        aluno=None,
        status=d["status"]
    )

    m._aluno_temp = d["aluno_matricula_id"]
    m._historico_temp = d["historico_academico_id"]
    m._registros_temp = d.get("registros_disciplinas", [])
    return m


def desserializar_mpd(d: dict) -> MatriculaPagaDisciplina:
    mpd = MatriculaPagaDisciplina(
        matricula=None,
        disciplina=None,
        historico=None
    )

    mpd._id_mpd = d["id_mpd"]
    mpd._matricula_temp = d["matricula_id"]
    mpd._disciplina_temp = d["disciplina_id"]
    mpd._historico_temp = d["historico_id"]

    mpd._notas_temp = d["notas"]
    mpd._faltas_temp = d["faltas"]
    mpd._media_temp = d["media_final"]
    mpd._nota_final_temp = d["nota_final"]
    return mpd


# ============================================================
# FUNÇÃO QUE RECONSTRÓI TODA A REDE DE OBJETOS
# ============================================================
def carregar_tudo(alunos_json, cursos_json, disciplinas_json,
                  professores_json, matriculas_json,
                  historicos_json, mpds_json):

    alunos = {}
    cursos = {}
    disciplinas = {}
    professores = {}
    matriculas = {}
    historicos = {}
    mpds = {}

    # 1 — Criar objetos simples (sem ligações)
    for d in alunos_json:
        obj = desserializar_aluno(d)
        alunos[obj.get_matricula()] = obj

    for d in cursos_json:
        obj = desserializar_curso(d)
        cursos[obj.get_codigo()] = obj

    for d in disciplinas_json:
        obj = desserializar_disciplina(d)
        disciplinas[obj.get_codigo()] = obj

    for d in professores_json:
        obj = desserializar_professor(d)
        professores[obj.get_codigo()] = obj

    for d in matriculas_json:
        obj = desserializar_matricula(d)
        matriculas[obj.get_id_matricula()] = obj

    for d in historicos_json:
        obj = desserializar_historico(d)
        historicos[d["matricula_aluno_id"]] = obj

    for d in mpds_json:
        obj = desserializar_mpd(d)
        mpds[d["id_mpd"]] = obj  # ID estável OK!


    # 2 — Ligar objetos
    for aluno in alunos.values():
        if aluno._curso_codigo_temp:
            aluno.set_curso(cursos.get(aluno._curso_codigo_temp))

    for curso in cursos.values():
        curso._disciplinas = [
            disciplinas[codigo] for codigo in curso._disciplinas_temp
            if codigo in disciplinas
        ]

    for disciplina in disciplinas.values():
        if disciplina._prof_temp:
            disciplina.set_professor_responsavel(professores.get(disciplina._prof_temp))

        disciplina._alunos = [
            alunos[m] for m in disciplina._alunos_temp if m in alunos
        ]

    for historico in historicos.values():
        historico._matricula_aluno = alunos.get(historico._matricula_temp)
        historico._data_emissao = datetime.datetime.fromisoformat(historico._data_temp)

    for matricula in matriculas.values():
        matricula._aluno = alunos.get(matricula._aluno_temp)
        matricula._historico = historicos.get(matricula._historico_temp)

    for mpd in mpds.values():
        mpd._matricula = matriculas.get(mpd._matricula_temp)
        mpd._disciplina = disciplinas.get(mpd._disciplina_temp)
        mpd._historico_acad = historicos.get(mpd._historico_temp)

        mpd._notas = mpd._notas_temp
        mpd._faltas = mpd._faltas_temp
        mpd._media_final = mpd._media_temp
        mpd._nota_final = mpd._nota_final_temp

    return alunos, cursos, disciplinas, professores, matriculas, historicos, mpds
