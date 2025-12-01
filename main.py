import streamlit as st
import sys
import os

# Adiciona a pasta raiz ao path
caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, caminho_raiz)

from models.sistema_academico import SistemaAcademico

# Configuração da página
st.set_page_config(
    page_title="Sistema Acadêmico",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização do sistema na sessão
if 'sistema' not in st.session_state:
    st.session_state.sistema = SistemaAcademico()

sistema = st.session_state.sistema

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎓 Sistema Acadêmico</h1>', unsafe_allow_html=True)

# Sidebar - Menu Principal
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Menu Principal")
    
    opcao_menu = st.radio(
        "Selecione uma opção:",
        ["🏠 Dashboard", "👨‍🎓 Gestão de Alunos", "👨‍🏫 Gestão de Professores", 
         "📚 Gestão de Cursos", "📖 Gestão de Disciplinas", "📊 Relatórios"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if st.button("💾 Salvar Dados", use_container_width=True):
        sistema.salvar_dados()
        st.success("Dados salvos com sucesso!")
    
    if st.button("🔄 Recarregar Dados", use_container_width=True):
        sistema.carregar_dados()
        st.success("Dados recarregados!")

# Conteúdo Principal
if opcao_menu == "🏠 Dashboard":
    st.header("Visão Geral do Sistema")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👨‍🎓 Total de Alunos",
            value=len(sistema.get_alunos()),
            delta="Ativos"
        )
    
    with col2:
        st.metric(
            label="👨‍🏫 Total de Professores",
            value=len(sistema.get_professores()),
            delta="Cadastrados"
        )
    
    with col3:
        st.metric(
            label="📚 Total de Cursos",
            value=len(sistema.get_cursos()),
            delta="Disponíveis"
        )
    
    with col4:
        st.metric(
            label="📖 Total de Disciplinas",
            value=len(sistema.get_disciplinas()),
            delta="Cadastradas"
        )
    
    st.divider()
    
    # Informações detalhadas
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📋 Resumo de Matrículas")
        total_matriculas = len(sistema.get_matriculas())
        st.info(f"Total de Matrículas: **{total_matriculas}**")
        
        if total_matriculas > 0:
            matriculas_ativas = sum(1 for m in sistema.get_matriculas().values() if m.get_status())
            st.success(f"Matrículas Ativas: **{matriculas_ativas}**")
            st.warning(f"Matrículas Inativas: **{total_matriculas - matriculas_ativas}**")
    
    with col_right:
        st.subheader("📊 Históricos Acadêmicos")
        total_historicos = len(sistema.get_historicos_academicos())
        st.info(f"Total de Históricos: **{total_historicos}**")
        
        total_mpds = len(sistema.get_matriculas_pagas_disciplinas())
        st.success(f"Registros de Disciplinas: **{total_mpds}**")

elif opcao_menu == "👨‍🎓 Gestão de Alunos":
    st.header("Gestão de Alunos")
    
    tab1, tab2, tab3 = st.tabs(["📝 Cadastrar", "📋 Listar", "🔍 Buscar"])
    
    with tab1:
        st.subheader("Cadastrar Novo Aluno")
        with st.form("form_aluno"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome completo*")
                email = st.text_input("E-mail*")
                matricula = st.text_input("Matrícula*")
                email_inst = st.text_input("E-mail institucional*")
            
            with col2:
                data_nasc = st.date_input("Data de nascimento*")
                telefone = st.text_input("Telefone*")
                periodo = st.number_input("Período atual*", min_value=1, max_value=12, value=1)
                creditos = st.number_input("Créditos concluídos", min_value=0, value=0)
            
            endereco = st.text_area("Endereço*")
            
            # Seleção de curso
            cursos_disponiveis = list(sistema.get_cursos().keys())
            curso_selecionado = st.selectbox("Curso*", cursos_disponiveis if cursos_disponiveis else ["Nenhum curso cadastrado"])
            
            submitted = st.form_submit_button("✅ Cadastrar Aluno", use_container_width=True)
            
            if submitted:
                if nome and email and matricula and email_inst and telefone and endereco:
                    st.success(f"Aluno {nome} cadastrado com sucesso!")
                    st.info("⚠️ Funcionalidade de cadastro será implementada na próxima etapa")
                else:
                    st.error("Por favor, preencha todos os campos obrigatórios (*)")
    
    with tab2:
        st.subheader("Lista de Alunos Cadastrados")
        
        alunos = sistema.get_alunos()
        
        if alunos:
            for matricula, aluno in alunos.items():
                with st.expander(f"📋 {aluno.get_nome()} - {matricula}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**E-mail:** {aluno.get_email()}")
                        st.write(f"**Telefone:** {aluno.get_telefone()}")
                        st.write(f"**Período:** {aluno.get_periodo_atual()}")
                    
                    with col2:
                        st.write(f"**E-mail Institucional:** {aluno.get_email_institucional()}")
                        st.write(f"**Créditos:** {aluno.get_creditos_concluidos()}")
                        curso = aluno.get_curso()
                        curso_nome = curso.get_codigo() if curso else "Não definido"
                        st.write(f"**Curso:** {curso_nome}")
        else:
            st.info("Nenhum aluno cadastrado no sistema.")
    
    with tab3:
        st.subheader("Buscar Aluno")
        busca = st.text_input("Digite a matrícula ou nome do aluno:")
        
        if busca:
            alunos = sistema.get_alunos()
            resultados = {k: v for k, v in alunos.items() 
                         if busca.lower() in k.lower() or busca.lower() in v.get_nome().lower()}
            
            if resultados:
                for matricula, aluno in resultados.items():
                    st.success(f"✅ Encontrado: {aluno.get_nome()} - {matricula}")
            else:
                st.warning("Nenhum aluno encontrado com esse critério.")

elif opcao_menu == "👨‍🏫 Gestão de Professores":
    st.header("Gestão de Professores")
    st.info("🚧 Módulo em desenvolvimento")
    
    professores = sistema.get_professores()
    
    if professores:
        for codigo, prof in professores.items():
            with st.expander(f"👨‍🏫 {prof.get_nome()} - Código: {codigo}"):
                st.write(f"**Departamento:** {prof.get_departamento()}")
                st.write(f"**Título:** {prof.get_titulo()}")
                st.write(f"**E-mail:** {prof.get_email()}")
    else:
        st.info("Nenhum professor cadastrado.")

elif opcao_menu == "📚 Gestão de Cursos":
    st.header("Gestão de Cursos")
    st.info("🚧 Módulo em desenvolvimento")
    
    cursos = sistema.get_cursos()
    
    if cursos:
        for codigo, curso in cursos.items():
            with st.expander(f"📚 Curso: {codigo}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Turno:** {curso.get_turno()}")
                    st.write(f"**Duração:** {curso.get_periodo()} períodos")
                with col2:
                    st.write(f"**Avaliação:** {curso.get_avaliacao_curso():.2f}")
                    st.write(f"**Disciplinas:** {len(curso.get_disciplinas())}")
    else:
        st.info("Nenhum curso cadastrado.")

elif opcao_menu == "📖 Gestão de Disciplinas":
    st.header("Gestão de Disciplinas")
    st.info("🚧 Módulo em desenvolvimento")
    
    disciplinas = sistema.get_disciplinas()
    
    if disciplinas:
        for codigo, disc in disciplinas.items():
            with st.expander(f"📖 {disc.get_nome()} - Código: {codigo}"):
                st.write(f"**Período:** {disc.get_periodo()}")
                prof = disc.get_professor_responsavel()
                prof_nome = prof.get_nome() if prof else "Não atribuído"
                st.write(f"**Professor:** {prof_nome}")
                st.write(f"**Alunos matriculados:** {len(disc.get_alunos())}")
    else:
        st.info("Nenhuma disciplina cadastrada.")

elif opcao_menu == "📊 Relatórios":
    st.header("Relatórios e Estatísticas")
    st.info("🚧 Módulo em desenvolvimento")
    
    tab1, tab2, tab3 = st.tabs(["📈 Estatísticas Gerais", "🎯 Desempenho", "📋 Históricos"])
    
    with tab1:
        st.subheader("Estatísticas Gerais do Sistema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Registros", 
                     len(sistema.get_matriculas_pagas_disciplinas()))
        
        with col2:
            st.metric("Históricos Emitidos", 
                     len(sistema.get_historicos_academicos()))
        
        with col3:
            matriculas_ativas = sum(1 for m in sistema.get_matriculas().values() if m.get_status())
            st.metric("Taxa de Matrículas Ativas", 
                     f"{(matriculas_ativas/max(len(sistema.get_matriculas()), 1)*100):.1f}%")
    
    with tab2:
        st.subheader("Análise de Desempenho")
        st.info("Relatórios de desempenho acadêmico serão exibidos aqui.")
    
    with tab3:
        st.subheader("Históricos Acadêmicos")
        st.info("Consulta de históricos acadêmicos será exibida aqui.")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Sistema Acadêmico v1.0 | Desenvolvido com Streamlit 🚀</p>
    </div>
""", unsafe_allow_html=True)