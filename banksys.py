import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

# ===============================================================================

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: 'Transacao'):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(self, conta: 'Conta'):
        pass

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta'):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta'):
        if conta._depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Conta:
    def __init__(self, numero: int, cliente: 'Cliente'):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> 'Cliente':
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def _sacar(self, valor: float) -> bool:
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
        return False

    def _depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: 'Cliente', limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        saques_realizados = [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]
        
        if valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite por transação. @@@")
        elif len(saques_realizados) >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")
        else:
            return super()._sacar(valor)

        return False

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Cliente(PessoaFisica):
    def __init__(self, endereco: str, cpf: str, nome: str, data_nascimento: str):
        super().__init__(cpf, nome, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

# ===============================================================================
# MENU

def menu() -> str:
    menu_texto = """
\n
================ MENU ================
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[4]\tNovo Cliente
[5]\tNova Conta
[6]\tListar Contas
[7]\tSair
=> """
    return input(textwrap.dedent(menu_texto))

def filtrar_cliente(cpf: str, clientes: list) -> Cliente | None:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente: Cliente) -> Conta | None:
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # Se o cliente só tem uma conta, retorna ela diretamente
    if len(cliente.contas) == 1:
        return cliente.contas[0]

    # Se tiver múltiplas, permite a escolha
    print("\nO cliente possui mais de uma conta. Por favor, selecione uma:")
    for i, conta in enumerate(cliente.contas):
        print(f"[{i+1}] Conta nº {conta.numero}, Agência {conta.agencia}")

    try:
        opcao = int(input("Digite o número da conta desejada: "))
        if 1 <= opcao <= len(cliente.contas):
            return cliente.contas[opcao - 1]
        else:
            print("\n@@@ Opção inválida! @@@")
            return None
    except ValueError:
        print("\n@@@ Entrada inválida! Por favor, digite um número. @@@")
        return None

def depositar_transacao(clientes: list):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n@@@ Erro de entrada. Insira apenas valores numéricos. @@@")

def sacar_transacao(clientes: list):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao)
    except ValueError:
        print("\n@@@ Erro de entrada. Insira apenas valores numéricos. @@@")

def exibir_extrato(clientes: list):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Nenhuma movimentação registrada."
    else:
        for transacao in transacoes:
            extrato += f"\n[{transacao['data']}] {transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes: list):
    cpf = input("Informe o CPF (somente número): ")
    cpf = "".join(filter(str.isdigit, cpf))
    
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = Cliente(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(novo_cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(clientes: list, contas: list):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas: list):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return
        
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print("-" * 50)
        print(textwrap.dedent(str(conta)))
    print("================================================")

# ===============================================================================
# MAIN

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar_transacao(clientes)
        elif opcao == "2":
            sacar_transacao(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            criar_conta(clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            print("\nObrigado por usar nossos serviços. Até a próxima!\n")
            break
        else:
            print("\n@@@ Opção inválida. Insira uma opção válida. @@@")

if __name__ == "__main__":
    main()