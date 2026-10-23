import unittest
from decimal import Decimal
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from banking import Banco
from banking.exceptions import ErroBancario, SaldoInsuficiente
from banking.cli import main


class BancoTests(unittest.TestCase):
    def setUp(self):
        self.banco = Banco()
        cliente = self.banco.cadastrar_cliente("Ana", "123.456.789-00")
        self.origem = self.banco.listar_contas()[0]
        self.destino = self.banco.abrir_conta(cliente.id)

    def test_deposito_saque_e_extrato(self):
        self.banco.depositar(self.origem.numero, "100.10")
        self.banco.sacar(self.origem.numero, "20.05")
        self.assertEqual(self.origem.saldo, Decimal("80.05"))
        self.assertEqual(len(self.banco.extrato(self.origem.numero)), 2)

    def test_transferencia_preserva_total(self):
        self.banco.depositar(self.origem.numero, "100")
        self.banco.transferir(self.origem.numero, self.destino.numero, "35.50")
        self.assertEqual(self.origem.saldo, Decimal("64.50"))
        self.assertEqual(self.destino.saldo, Decimal("35.50"))
        self.assertEqual(len(self.destino.transacoes), 1)

    def test_transferencia_sem_saldo_nao_altera_contas(self):
        with self.assertRaises(SaldoInsuficiente):
            self.banco.transferir(self.origem.numero, self.destino.numero, "1")
        self.assertEqual(self.origem.saldo + self.destino.saldo, 0)
        self.assertEqual(self.origem.transacoes, [])
        self.assertEqual(self.destino.transacoes, [])

    def test_valores_invalidos(self):
        for valor in ("0", "-1", "0.001", "NaN", "Infinity", "abc"):
            with self.subTest(valor=valor), self.assertRaises(ErroBancario):
                self.banco.depositar(self.origem.numero, valor)
        self.assertEqual(self.origem.saldo, 0)

    def test_cpf_duplicado(self):
        with self.assertRaises(ErroBancario):
            self.banco.cadastrar_cliente("Outra Ana", "12345678900")

    def test_cadastro_abre_conta_e_normaliza_cpf(self):
        self.assertEqual(self.origem.cliente.cpf, "12345678900")
        self.assertEqual(self.origem.numero, "000001")
        self.assertEqual(self.origem.saldo, Decimal("0.00"))
        self.assertEqual(self.origem.transacoes, [])

    def test_numeracao_incremental_entre_clientes_e_contas_adicionais(self):
        cliente = self.banco.cadastrar_cliente("Bruno", "98765432100")
        adicional = self.banco.abrir_conta(cliente.id)
        self.assertEqual(cliente.id, 2)
        self.assertEqual(adicional.numero, "000004")
        self.assertEqual([c.numero for c in self.banco.listar_contas()],
                         ["000001", "000002", "000003", "000004"])

    def test_cadastro_invalido_nao_cria_cliente_ou_conta(self):
        for nome, cpf in (("", "98765432100"), ("Ana", ""),
                          ("Ana", "123"), ("Ana", "abcdefghijk"),
                          ("Ana", "12345678900")):
            with self.subTest(nome=nome, cpf=cpf), self.assertRaises(ErroBancario):
                self.banco.cadastrar_cliente(nome, cpf)
        cliente = self.banco.cadastrar_cliente("Bruno", "98765432100")
        self.assertEqual(cliente.id, 2)
        self.assertEqual(self.banco.listar_contas()[-1].numero, "000003")

    def test_cliente_inexistente_nao_consume_numero_da_conta(self):
        with self.assertRaises(ErroBancario):
            self.banco.abrir_conta(999)
        self.assertEqual(self.banco.abrir_conta(self.origem.cliente.id).numero, "000003")

    def test_cli_cadastro_seguido_de_listagem(self):
        saida = StringIO()
        with patch("builtins.input", side_effect=["1", "Ana", "123.456.789-00", "3", "0"]), redirect_stdout(saida):
            main()
        self.assertIn("Conta aberta automaticamente: 000001", saida.getvalue())
        self.assertIn("000001 | Ana | CPF: 12345678900 | R$ 0.00", saida.getvalue())

    def test_cli_listagem_vazia(self):
        saida = StringIO()
        with patch("builtins.input", side_effect=["3", "0"]), redirect_stdout(saida):
            main()
        self.assertIn("Nenhuma conta cadastrada.", saida.getvalue())

    def test_destino_inexistente_nao_debita(self):
        self.banco.depositar(self.origem.numero, "10")
        with self.assertRaises(ErroBancario):
            self.banco.transferir(self.origem.numero, "999999", "5")
        self.assertEqual(self.origem.saldo, Decimal("10.00"))

    def test_saque_sem_saldo(self):
        with self.assertRaises(SaldoInsuficiente):
            self.banco.sacar(self.origem.numero, "1")

    def test_transferencia_para_mesma_conta(self):
        with self.assertRaises(ErroBancario):
            self.banco.transferir(self.origem.numero, self.origem.numero, "1")


if __name__ == "__main__":
    unittest.main()
