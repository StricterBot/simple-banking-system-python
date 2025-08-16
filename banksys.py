from datetime import datetime
import textwrap

LANG = "PT"  # Troque para "EN" para inglês (Ainda não atualizado)

MESSAGES = {
    "EN": {
        "welcome": "Welcome!",
        "menu": """\nPlease select operation:\n
[1] Deposit
[2] Withdraw
[3] Statement
[4] New User
[5] New Account
[6] List Accounts
[7] Exit

=> """,
        "user_created_success": "User created successfully!",
        "user_exists_error": "Error: A user with this CPF already exists.",
        "user_not_found_error": "Error: User not found.",
        "account_created_success": "Account created successfully!",
        "deposit_prompt": "Enter the deposit amount: R$ ",
        "deposit_success": "Your deposit was successful.",
        "deposit_error": "Invalid operation. Please enter a positive value.",
        "withdraw_prompt": "Enter the withdraw amount: R$ ",
        "withdraw_success": "Your withdrawal was successful.",
        "balance_error": "Operation failed! You do not have enough balance.",
        "limit_error": "Operation failed! The withdrawal amount exceeds the limit.",
        "daily_limit_error": "Operation failed! Maximum number of withdrawals exceeded.",
        "no_transactions": "No transactions yet.",
        "balance": "Current Balance: R$ {:.2f}",
        "goodbye": "Thank you for using our services. See you next time!",
        "invalid_option": "Invalid option. Please select a valid operation.",
        "input_error": "Input error. Please enter numeric values only.",
    },
    "PT": {
        "welcome": "Bem-vindo ao sistema bancário em python!\n",
        "menu": """
Por favor, selecione a operação desejada:

[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[6] Listar Contas
[7] Sair

=> """,
        "user_created_success": "Usuário criado com sucesso!",
        "user_exists_error": "Erro: Já existe um usuário cadastrado com este CPF.",
        "user_not_found_error": "Erro: Usuário não encontrado.",
        "account_created_success": "Conta criada com sucesso!",
        "deposit_prompt": "Informe o valor do depósito: R$ ",
        "deposit_success": "Depósito realizado com sucesso.",
        "deposit_error": "Operação inválida. Por favor, insira um valor positivo.",
        "withdraw_prompt": "Informe o valor do saque: R$ ",
        "withdraw_success": "Saque realizado com sucesso.",
        "balance_error": "Operação falhou! Você não tem saldo suficiente.",
        "limit_error": "Operação falhou! O valor do saque excede o limite.",
        "daily_limit_error": "Operação falhou! Número máximo de saques excedido.",
        "no_transactions": "Nenhuma movimentação registrada.",
        "balance": "Saldo atual: R$ {:.2f}",
        "goodbye": "Obrigado por usar nossos serviços. Até a próxima!",
        "invalid_option": "Opção inválida. Por favor, selecione uma operação válida.",
        "input_error": "Erro de entrada. Por favor, insira apenas valores numéricos.",
    }
}

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"[{timestamp}] Depósito:\t\tR$ {valor:.2f}\n"
        print(MESSAGES[LANG]["deposit_success"])
    else:
        print(MESSAGES[LANG]["deposit_error"])
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print(MESSAGES[LANG]["balance_error"])
    elif excedeu_limite:
        print(MESSAGES[LANG]["limit_error"])
    elif excedeu_saques:
        print(MESSAGES[LANG]["daily_limit_error"])
    elif valor > 0:
        saldo -= valor
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        extrato += f"[{timestamp}] Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(MESSAGES[LANG]["withdraw_success"])
    else:
        print(MESSAGES[LANG]["deposit_error"])
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print(MESSAGES[LANG]["no_transactions"] if not extrato else extrato)
    print(f"\n{MESSAGES[LANG]['balance'].format(saldo)}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    cpf = "".join(filter(str.isdigit, cpf))

    usuario_existe = filtrar_usuario(cpf, usuarios)
    if usuario_existe:
        print(MESSAGES[LANG]["user_exists_error"])
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    print("\n--- Cadastro de Endereço ---")
    logradouro = input("Informe o logradouro (Ex: Rua, Avenida): ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    sigla_estado = input("Estado (Sigla): ")

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{sigla_estado.upper()}"

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(MESSAGES[LANG]["user_created_success"])

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    cpf = "".join(filter(str.isdigit, cpf))

    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        contas.append({"agencia": agencia, "numero": numero_conta, "usuario": usuario})
        print(MESSAGES[LANG]["account_created_success"])
    else:
        print(MESSAGES[LANG]["user_not_found_error"])

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
    print("==================================================")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        print(MESSAGES[LANG]["welcome"])
        opcao = input(textwrap.dedent(MESSAGES[LANG]["menu"])).lower()

        if opcao == "1":
            try:
                valor = float(input(MESSAGES[LANG]["deposit_prompt"]))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print(MESSAGES[LANG]["input_error"])

        elif opcao == "2":
            try:
                valor = float(input(MESSAGES[LANG]["withdraw_prompt"]))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except ValueError:
                print(MESSAGES[LANG]["input_error"])

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)
        
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(AGENCIA, numero_conta, usuarios, contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print(MESSAGES[LANG]["goodbye"])
            break

        else:
            print(MESSAGES[LANG]["invalid_option"])

if __name__ == "__main__":
    main()