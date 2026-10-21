import unittest
from decimal import Decimal

from banking import Banco
from banking.exceptions import ErroBancario, SaldoInsuficiente


class BancoTests(unittest.TestCase):
    def setUp(self):
        self.banco = Banco()
        cliente = self.banco.cadastrar_cliente("Ana", "123.456.789-00")
        self.origem = self.banco.abrir_conta(cliente.id)
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
