"""Regras bancárias e armazenamento temporário em memória."""

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from uuid import uuid4

from .exceptions import ErroBancario, SaldoInsuficiente
from .models import Cliente, Conta, TipoTransacao, Transacao


def validar_valor(valor: str | Decimal | int) -> Decimal:
    try:
        quantia = Decimal(str(valor))
        if not quantia.is_finite() or quantia <= 0:
            raise ErroBancario("O valor deve ser positivo e finito.")
        arredondado = quantia.quantize(Decimal("0.01"))
        if quantia != arredondado:
            raise ErroBancario("Use no máximo duas casas decimais.")
        return arredondado
    except InvalidOperation as exc:
        raise ErroBancario("Valor monetário inválido.") from exc


class Banco:
    def __init__(self, nome: str = "Banco Python") -> None:
        self.nome = nome
        self._clientes: dict[int, Cliente] = {}
        self._contas: dict[str, Conta] = {}

    def cadastrar_cliente(self, nome: str, cpf: str) -> Cliente:
        nome = nome.strip()
        cpf = cpf.strip().replace(".", "").replace("-", "")
        if not nome:
            raise ErroBancario("Informe o nome do cliente.")
        if len(cpf) != 11 or not cpf.isascii() or not cpf.isdigit():
            raise ErroBancario("O CPF deve conter 11 dígitos.")
        if any(cliente.cpf == cpf for cliente in self._clientes.values()):
            raise ErroBancario("CPF já cadastrado.")
        cliente = Cliente(len(self._clientes) + 1, nome, cpf)
        self._clientes[cliente.id] = cliente
        return cliente

    def abrir_conta(self, cliente_id: int) -> Conta:
        cliente = self._clientes.get(cliente_id)
        if cliente is None:
            raise ErroBancario("Cliente não encontrado.")
        numero = f"{len(self._contas) + 1:06d}"
        conta = Conta(numero, cliente)
        self._contas[numero] = conta
        return conta

    def buscar_conta(self, numero: str) -> Conta:
        if numero not in self._contas:
            raise ErroBancario("Conta não encontrada.")
        return self._contas[numero]

    def listar_contas(self) -> tuple[Conta, ...]:
        return tuple(self._contas.values())

    def depositar(self, numero: str, valor: str | Decimal | int) -> None:
        conta = self.buscar_conta(numero)
        quantia = validar_valor(valor)
        conta.saldo += quantia
        self._registrar(conta, TipoTransacao.DEPOSITO, quantia)

    def sacar(self, numero: str, valor: str | Decimal | int) -> None:
        conta = self.buscar_conta(numero)
        quantia = validar_valor(valor)
        if conta.saldo < quantia:
            raise SaldoInsuficiente("Saldo insuficiente.")
        conta.saldo -= quantia
        self._registrar(conta, TipoTransacao.SAQUE, quantia)

    def transferir(self, origem: str, destino: str, valor: str | Decimal | int) -> None:
        if origem == destino:
            raise ErroBancario("Escolha contas diferentes para a transferência.")
        remetente = self.buscar_conta(origem)
        destinatario = self.buscar_conta(destino)
        quantia = validar_valor(valor)
        if remetente.saldo < quantia:
            raise SaldoInsuficiente("Saldo insuficiente.")
        remetente.saldo -= quantia
        destinatario.saldo += quantia
        self._registrar(remetente, TipoTransacao.TRANSFERENCIA_ENVIADA, quantia, destino)
        self._registrar(destinatario, TipoTransacao.TRANSFERENCIA_RECEBIDA, quantia, origem)

    def extrato(self, numero: str) -> tuple[Transacao, ...]:
        return tuple(self.buscar_conta(numero).transacoes)

    @staticmethod
    def _registrar(conta: Conta, tipo: TipoTransacao, valor: Decimal,
                   relacionada: str | None = None) -> None:
        conta.transacoes.append(Transacao(
            str(uuid4()), tipo, valor, datetime.now(timezone.utc), relacionada
        ))
