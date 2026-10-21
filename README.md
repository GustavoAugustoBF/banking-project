# Banking Project

Simulador de banco em Python 3.10+, usando apenas a biblioteca padrão.

## Executar

Dentro da pasta `banking-project`:

```powershell
py -m banking
```

Em ambientes que usam o comando `python`, execute `python -m banking`.
Não é necessário instalar dependências para executar ou testar.

## Estrutura

```text
banking-project/
├── banking/
│   ├── __init__.py
│   ├── __main__.py       # Entrada do programa
│   ├── cli.py            # Menu de terminal
│   ├── exceptions.py     # Erros de negócio
│   ├── models.py         # Cliente, Conta e Transacao
│   └── services.py       # Cadastro e operações bancárias
├── tests/
│   └── test_banco.py
├── .gitignore
└── pyproject.toml
```

## Funcionalidades

- Cadastrar clientes com CPF único e abrir contas com saldo inicial zero.
- Consultar contas e saldos.
- Depositar, sacar e transferir entre contas.
- Consultar o histórico de transações.
- Validar valores positivos, centavos e saldo disponível.

Os valores monetários usam `Decimal`. Na API Python, passe valores como strings,
por exemplo `banco.depositar("000001", "100.50")`.
No terminal, o separador decimal pode ser vírgula ou ponto, sem separador de milhar.

## Testes

```powershell
py -m unittest discover -s tests -v
```

## Limites desta versão

Projeto didático: os dados ficam em memória e são perdidos ao encerrar o programa.
O CPF é validado pelo formato de 11 dígitos, sem cálculo dos dígitos verificadores.
Os modelos são mutáveis; use o serviço `Banco` para executar operações.
Não há autenticação, persistência ou suporte a operações concorrentes.
Uma evolução possível é adicionar SQLite, autenticação e uma API HTTP.
