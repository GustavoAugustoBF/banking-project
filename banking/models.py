"""Modelos de domínio. Valores monetários usam Decimal, nunca float."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TipoTransacao(str, Enum):
    DEPOSITO = "depósito"
    SAQUE = "saque"
    TRANSFERENCIA_ENVIADA = "transferência enviada"
    TRANSFERENCIA_RECEBIDA = "transferência recebida"


@dataclass(frozen=True)
class Cliente:
    id: int
    nome: str
    cpf: str


@dataclass(frozen=True)
class Transacao:
    id: str
    tipo: TipoTransacao
    valor: Decimal
    data: datetime
    conta_relacionada: str | None = None


@dataclass
class Conta:
    numero: str
    cliente: Cliente
    saldo: Decimal = Decimal("0.00")
    transacoes: list[Transacao] = field(default_factory=list)
