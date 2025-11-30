

class MenuPrincipal:

    def exibir(self):
        menu_aluno = MenuAluno()
        # menu_professor = MenuProfessor()  ← depois colocamos

        opcao = -1

        while opcao != "0":
            print("\n===== SISTEMA ACADÊMICO =====")
            print("1 - Menu Aluno")
            print("2 - Menu Professor")
            print("0 - Sair")
            opcao = input("Escolha: ")

            match opcao:
                case "1":
                    menu_aluno.exibir()
                case "2":
                    print("Menu professor ainda não implementado.")
                case "0":
                    print("Encerrando...")
                case _:
                    print("Opção inválida!")
