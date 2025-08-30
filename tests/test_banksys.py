import sys
import os
import pytest
from unittest.mock import patch

# Precisei adicionar essa linha no meu ambiente pois não estava achando o arquivo na pasta raiz. Mas talvez você não precise.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from banksys import (
    Cliente,
    ContaCorrente,
    Deposito,
    Saque,
    criar_cliente,
    criar_conta,
    listar_contas
)

# --- Fixtures para criar objetos de teste ---

@pytest.fixture
def cliente_fixture():
    return Cliente(
        cpf="12345678900",
        nome="João da Silva",
        data_nascimento="01-01-1990",
        endereco="Rua Teste, 123"
    )

@pytest.fixture
def conta_fixture(cliente_fixture):
    """Fornece um objeto ContaCorrente padrão, já associado a um Cliente."""
    return ContaCorrente.nova_conta(cliente=cliente_fixture, numero=1)

# --- Testes das Classes ---

class TestContaCorrente:
    def test_deposito_sucesso(self, conta_fixture):
        Deposito(100.50).registrar(conta_fixture)
        assert conta_fixture.saldo == 100.50
        assert len(conta_fixture.historico.transacoes) == 1

    def test_deposito_valor_negativo(self, conta_fixture, capsys):
        sucesso = conta_fixture._depositar(-50)
        captured = capsys.readouterr()
        assert sucesso is False
        assert conta_fixture.saldo == 0
        assert "valor informado é inválido" in captured.out

    def test_saque_sucesso(self, conta_fixture):
        Deposito(1000).registrar(conta_fixture)
        Saque(200).registrar(conta_fixture)
        assert conta_fixture.saldo == 800
        assert len(conta_fixture.historico.transacoes) == 2

    def test_saque_sem_saldo(self, conta_fixture, capsys):
        sucesso = conta_fixture.sacar(100)
        captured = capsys.readouterr()
        assert sucesso is False
        assert conta_fixture.saldo == 0
        assert "não tem saldo suficiente" in captured.out

    def test_saque_excede_limite_valor(self, conta_fixture, capsys):
        Deposito(1000).registrar(conta_fixture)
        sucesso = conta_fixture.sacar(600)
        captured = capsys.readouterr()
        assert sucesso is False
        assert conta_fixture.saldo == 1000
        assert "excede o limite por transação" in captured.out

    def test_saque_excede_limite_diario(self, conta_fixture, capsys):
        Deposito(1000).registrar(conta_fixture)
        Saque(10).registrar(conta_fixture)
        Saque(10).registrar(conta_fixture)
        Saque(10).registrar(conta_fixture)
        sucesso = conta_fixture.sacar(10)
        captured = capsys.readouterr()
        assert sucesso is False
        assert conta_fixture.saldo == 970
        assert "Número máximo de saques diários excedido" in captured.out

class TestTransacao:
    def test_registro_transacao_deposito(self, conta_fixture):
        Deposito(200).registrar(conta_fixture)
        assert conta_fixture.saldo == 200
        assert len(conta_fixture.historico.transacoes) == 1

    def test_registro_transacao_saque(self, conta_fixture):
        Deposito(500).registrar(conta_fixture)
        Saque(150).registrar(conta_fixture)
        assert conta_fixture.saldo == 350
        assert len(conta_fixture.historico.transacoes) == 2

# --- Testes das Funções do Menu ---
class TestFuncoesMenu:
    @patch('builtins.input', side_effect=["98765432100", "Maria Souza", "02-02-1985", "Avenida Brasil, 456"])
    def test_criar_cliente_sucesso(self, mock_input, capsys):
        clientes = []
        criar_cliente(clientes)
        assert len(clientes) == 1
        assert isinstance(clientes[0], Cliente)
        assert clientes[0].cpf == "98765432100"

    @patch('builtins.input', side_effect=["12345678900"])
    def test_criar_conta_sucesso(self, mock_input, cliente_fixture, capsys):
        clientes = [cliente_fixture]
        contas = []
        criar_conta(clientes, contas)
        assert len(contas) == 1
        assert len(cliente_fixture.contas) == 1

    def test_listar_contas(self, conta_fixture, capsys):
        contas = [conta_fixture]
        listar_contas(contas)
        captured = capsys.readouterr()
        assert "LISTA DE CONTAS" in captured.out
        assert "Titular:\tJoão da Silva" in captured.out
        
    @patch('builtins.input', side_effect=["12345678900", "12345678900"])
    def test_criar_multiplas_contas_para_mesmo_cliente(self, mock_input, cliente_fixture):
        clientes = [cliente_fixture]
        contas = []
        criar_conta(clientes, contas)
        criar_conta(clientes, contas)
        assert len(contas) == 2
        assert len(cliente_fixture.contas) == 2
        assert contas[1].numero == 2
        assert contas[1].cliente == cliente_fixture

# --- Testes de Cenários Complexos ---
class TestCenarioMultiplasContas:
    def test_operacoes_independentes_em_contas_diferentes(self, cliente_fixture):
        conta1 = ContaCorrente.nova_conta(cliente=cliente_fixture, numero=1)
        conta2 = ContaCorrente.nova_conta(cliente=cliente_fixture, numero=2)
        cliente_fixture.adicionar_conta(conta1)
        cliente_fixture.adicionar_conta(conta2)

        Deposito(1000.0).registrar(conta1)
        Saque(150.0).registrar(conta1)
        Deposito(500.0).registrar(conta2)

        assert conta1.saldo == 850.0
        assert len(conta1.historico.transacoes) == 2
        assert conta2.saldo == 500.0
        assert len(conta2.historico.transacoes) == 1