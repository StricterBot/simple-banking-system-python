import pytest
from unittest.mock import patch
import textwrap
from datetime import datetime

import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from banksys import (
    depositar,
    sacar,
    exibir_extrato,
    criar_usuario,
    filtrar_usuario,
    criar_conta,
    listar_contas,
    MESSAGES,
    LANG
)

# --- Fixtures ---

@pytest.fixture
def sample_user_list():
    """Provides a sample list of users for testing."""
    return [
        {"nome": "João da Silva", "data_nascimento": "01-01-1990", "cpf": "12345678900", "endereco": "Rua Exemplo, 123 - Bairro Teste - Cidade/TS"},
    ]

@pytest.fixture
def sample_account_list(sample_user_list):
    """Provides a sample list of accounts linked to users."""
    return [
        {"agencia": "0001", "numero": 1, "usuario": sample_user_list[0]},
    ]

# --- Test Classes ---

class TestDepositar:
    def test_depositar_valor_positivo(self):
        saldo, extrato = depositar(100.0, 50.0, "")
        assert saldo == 150.0
        assert "Depósito:" in extrato
        assert "R$ 50.00" in extrato

    def test_depositar_valor_negativo(self, capsys):
        saldo, extrato = depositar(100.0, -50.0, "")
        captured = capsys.readouterr()
        assert saldo == 100.0
        assert extrato == ""
        assert MESSAGES[LANG]["deposit_error"] in captured.out

    def test_depositar_valor_zero(self, capsys):
        saldo, extrato = depositar(100.0, 0.0, "")
        captured = capsys.readouterr()
        assert saldo == 100.0
        assert extrato == ""
        assert MESSAGES[LANG]["deposit_error"] in captured.out

class TestSacar:
    def test_sacar_com_sucesso(self):
        saldo, extrato, numero_saques = sacar(
            saldo=1000.0,
            valor=100.0,
            extrato="",
            limite=500.0,
            numero_saques=0,
            limite_saques=3
        )
        assert saldo == 900.0
        assert "Saque:" in extrato
        assert "R$ 100.00" in extrato
        assert numero_saques == 1

    def test_sacar_sem_saldo(self, capsys):
        saldo, extrato, numero_saques = sacar(
            saldo=50.0,
            valor=100.0,
            extrato="",
            limite=500.0,
            numero_saques=0,
            limite_saques=3
        )
        captured = capsys.readouterr()
        assert saldo == 50.0
        assert extrato == ""
        assert numero_saques == 0
        assert MESSAGES[LANG]["balance_error"] in captured.out

    def test_sacar_acima_do_limite(self, capsys):
        saldo, extrato, numero_saques = sacar(
            saldo=1000.0,
            valor=600.0,
            extrato="",
            limite=500.0,
            numero_saques=0,
            limite_saques=3
        )
        captured = capsys.readouterr()
        assert saldo == 1000.0
        assert extrato == ""
        assert numero_saques == 0
        assert MESSAGES[LANG]["limit_error"] in captured.out

    def test_sacar_excedendo_limite_diario(self, capsys):
        saldo, extrato, numero_saques = sacar(
            saldo=1000.0,
            valor=100.0,
            extrato="",
            limite=500.0,
            numero_saques=3,
            limite_saques=3
        )
        captured = capsys.readouterr()
        assert saldo == 1000.0
        assert extrato == ""
        assert numero_saques == 3
        assert MESSAGES[LANG]["daily_limit_error"] in captured.out

    def test_sacar_valor_negativo(self, capsys):
        saldo, extrato, numero_saques = sacar(
            saldo=1000.0,
            valor=-100.0,
            extrato="",
            limite=500.0,
            numero_saques=0,
            limite_saques=3
        )
        captured = capsys.readouterr()
        assert saldo == 1000.0
        assert extrato == ""
        assert numero_saques == 0
        assert MESSAGES[LANG]["deposit_error"] in captured.out

class TestExtrato:
    def test_exibir_extrato_com_movimentacoes(self, capsys):
        saldo = 950.0
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato = f"[{timestamp}] Depósito:\t\tR$ 1000.00\n[{timestamp}] Saque:\t\t\tR$ 50.00\n"
        exibir_extrato(saldo, extrato=extrato)
        captured = capsys.readouterr()
        assert "EXTRATO" in captured.out
        assert "Depósito:" in captured.out
        assert "Saque:" in captured.out
        assert "Saldo atual: R$ 950.00" in captured.out

    def test_exibir_extrato_sem_movimentacoes(self, capsys):
        exibir_extrato(0.0, extrato="")
        captured = capsys.readouterr()
        assert "EXTRATO" in captured.out
        assert MESSAGES[LANG]["no_transactions"] in captured.out
        assert "Saldo atual: R$ 0.00" in captured.out

class TestUsuario:
    def test_filtrar_usuario_existente(self, sample_user_list):
        usuario = filtrar_usuario("12345678900", sample_user_list)
        assert usuario is not None
        assert usuario["cpf"] == "12345678900"

    def test_filtrar_usuario_inexistente(self, sample_user_list):
        usuario = filtrar_usuario("00000000000", sample_user_list)
        assert usuario is None

    @patch('builtins.input', side_effect=["98765432100", "Maria Souza", "02-02-1985", "Avenida Brasil", "456", "Centro", "Rio de Janeiro", "RJ"])
    def test_criar_usuario_sucesso(self, mock_input, capsys):
        usuarios = []
        criar_usuario(usuarios)
        captured = capsys.readouterr()
        
        assert len(usuarios) == 1
        assert usuarios[0]["cpf"] == "98765432100"
        assert usuarios[0]["nome"] == "Maria Souza"
        assert "Avenida Brasil, 456 - Centro - Rio de Janeiro/RJ" in usuarios[0]["endereco"]
        assert MESSAGES[LANG]["user_created_success"] in captured.out

    @patch('builtins.input', side_effect=["12345678900"])
    def test_criar_usuario_existente(self, mock_input, sample_user_list, capsys):
        usuarios = sample_user_list
        initial_len = len(usuarios)
        criar_usuario(usuarios)
        captured = capsys.readouterr()

        assert len(usuarios) == initial_len
        assert MESSAGES[LANG]["user_exists_error"] in captured.out

class TestConta:
    @patch('builtins.input', side_effect=["12345678900"])
    def test_criar_conta_sucesso(self, mock_input, sample_user_list, capsys):
        contas = []
        criar_conta("0001", 1, sample_user_list, contas)
        captured = capsys.readouterr()

        assert len(contas) == 1
        assert contas[0]["agencia"] == "0001"
        assert contas[0]["numero"] == 1
        assert contas[0]["usuario"]["cpf"] == "12345678900"
        assert MESSAGES[LANG]["account_created_success"] in captured.out

    @patch('builtins.input', side_effect=["11122233344"])
    def test_criar_conta_usuario_nao_encontrado(self, mock_input, sample_user_list, capsys):
        contas = []
        criar_conta("0001", 1, sample_user_list, contas)
        captured = capsys.readouterr()

        assert len(contas) == 0
        assert MESSAGES[LANG]["user_not_found_error"] in captured.out

    def test_listar_contas_existentes(self, sample_account_list, capsys):
        listar_contas(sample_account_list)
        captured = capsys.readouterr()
        
        conta = sample_account_list[0]
        expected_output = textwrap.dedent(f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero']}
            Titular:\t{conta['usuario']['nome']}
        """)
        
        assert "LISTA DE CONTAS" in captured.out
        # Normalize whitespace for a more robust comparison
        assert "".join(expected_output.split()) in "".join(captured.out.split())

    def test_listar_contas_vazio(self, capsys):
        listar_contas([])
        captured = capsys.readouterr()
        assert "Nenhuma conta cadastrada." in captured.out