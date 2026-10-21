"""Erros esperados nas operações bancárias."""


class ErroBancario(ValueError):
    """Uma regra de negócio não foi atendida."""


class SaldoInsuficiente(ErroBancario):
    """A conta não possui saldo para a operação."""
