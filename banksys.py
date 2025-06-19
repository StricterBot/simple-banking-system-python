from datetime import datetime

LANG = "EN"  # Troque para "PT" para português

MESSAGES = {
    "EN": {
        "welcome": "Welcome, {user}!",
        "menu": """\nPlease select operation:\n
[1] Deposit
[2] Withdraw
[3] Statement
[4] Exit

=> """,
        "deposit_selected": "Deposit selected.",
        "deposit_prompt": "Enter the deposit amount: R$ ",
        "deposit_success": "Your deposit was successful.",
        "deposit_error": "Invalid operation. Please enter a positive value.",
        "withdraw_selected": "Withdraw selected.",
        "withdraw_limit_info": "Withdraw limit is R$ {limit:.2f} per transaction. Withdrawals today: {used}/{limit_total}.",
        "withdraw_prompt": "Enter the withdraw amount: R$ ",
        "withdraw_success": "Your withdrawal was successful.",
        "withdraw_error": "Invalid operation. Please check values and try again.",
        "withdraw_limit_reached": "You have reached the daily withdrawal limit.",
        "statement_selected": "Account Statement selected.",
        "statement_header": "==== STATEMENT ====",
        "no_transactions": "No transactions yet.",
        "balance": "Current Balance: R$ {balance:.2f}",
        "statement_footer": "===================",
        "goodbye": "Thank you, {user}, for using our services. See you next time!",
        "invalid_option": "Invalid option. Please enter a valid input.",
        "input_error": "Input error. Please enter numeric values only.",
        "divider": "=" * 40,
    },
    "PT": {
        "welcome": "Bem-vindo(a), {user}!",
        "menu": """\nSelecione a operação:\n
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """,
        "deposit_selected": "Depósito selecionado.",
        "deposit_prompt": "Informe o valor do depósito: R$ ",
        "deposit_success": "Depósito realizado com sucesso.",
        "deposit_error": "Operação inválida. Insira um valor positivo.",
        "withdraw_selected": "Saque selecionado.",
        "withdraw_limit_info": "Limite de R$ {limit:.2f} por saque. Saques hoje: {used}/{limit_total}.",
        "withdraw_prompt": "Informe o valor do saque: R$ ",
        "withdraw_success": "Saque realizado com sucesso.",
        "withdraw_error": "Operação inválida. Verifique os valores e tente novamente.",
        "withdraw_limit_reached": "Você atingiu o limite diário de saques.",
        "statement_selected": "Extrato selecionado.",
        "statement_header": "==== EXTRATO ====",
        "no_transactions": "Nenhuma movimentação registrada.",
        "balance": "Saldo atual: R$ {balance:.2f}",
        "statement_footer": "===================",
        "goodbye": "Obrigado, {user}, por usar nossos serviços. Até a próxima!",
        "invalid_option": "Opção inválida. Insira uma opção válida.",
        "input_error": "Erro de entrada. Insira apenas valores numéricos.",
        "divider": "=" * 40,
    }
}

USER = "Test_User"
BALANCE = 0
WITHDRAW_LIMIT = 500
transactions = []
withdraw_count = 0
WITHDRAW_LIMIT_COUNT = 3

def print_divider():
    print(MESSAGES[LANG]["divider"])

print(MESSAGES[LANG]["welcome"].format(user=USER))

while True:
    option = input(MESSAGES[LANG]["menu"])

    if option == "1":
        print(MESSAGES[LANG]["deposit_selected"])
        try:
            deposit_amount = float(input(MESSAGES[LANG]["deposit_prompt"]))
        except ValueError:
            print(MESSAGES[LANG]["input_error"])
            continue

        if deposit_amount > 0:
            BALANCE += deposit_amount
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            transactions.append(f"[{timestamp}] [Deposit] +R$ {deposit_amount:.2f}")
            print(MESSAGES[LANG]["deposit_success"])
            print(MESSAGES[LANG]["balance"].format(balance=BALANCE))
        else:
            print(MESSAGES[LANG]["deposit_error"])

        print_divider()

    elif option == "2":
        print(MESSAGES[LANG]["withdraw_selected"])
        print(MESSAGES[LANG]["withdraw_limit_info"].format(
            limit=WITHDRAW_LIMIT,
            used=withdraw_count,
            limit_total=WITHDRAW_LIMIT_COUNT
        ))
        if withdraw_count < WITHDRAW_LIMIT_COUNT:
            try:
                withdraw_amount = float(input(MESSAGES[LANG]["withdraw_prompt"]))
            except ValueError:
                print(MESSAGES[LANG]["input_error"])
                continue

            if (0 < withdraw_amount <= WITHDRAW_LIMIT) and (withdraw_amount <= BALANCE):
                BALANCE -= withdraw_amount
                withdraw_count += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                transactions.append(f"[{timestamp}] [Withdraw] -R$ {withdraw_amount:.2f}")
                print(MESSAGES[LANG]["withdraw_success"])
                print(MESSAGES[LANG]["balance"].format(balance=BALANCE))
            else:
                print(MESSAGES[LANG]["withdraw_error"])
        else:
            print(MESSAGES[LANG]["withdraw_limit_reached"])

        print_divider()

    elif option == "3":
        print(MESSAGES[LANG]["statement_selected"])
        print(MESSAGES[LANG]["statement_header"])
        if transactions:
            for operation in transactions:
                print(operation)
        else:
            print(MESSAGES[LANG]["no_transactions"])
        print(MESSAGES[LANG]["balance"].format(balance=BALANCE))
        print(MESSAGES[LANG]["statement_footer"])
        print_divider()

    elif option == "4":
        print(MESSAGES[LANG]["goodbye"].format(user=USER))
        break

    else:
        print(MESSAGES[LANG]["invalid_option"])
        print_divider()