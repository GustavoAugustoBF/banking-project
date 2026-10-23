# Banking Project

Simulador de banco em Python 3.10+, usando apenas a biblioteca padrão.

## Executar

Dentro da pasta `banking-project`:

```powershell
py -m banking
```

Você também pode abrir `main.py` no VS Code e selecionar **Run Python File in
Terminal** (Executar Arquivo Python no Terminal), ou executar `py main.py`.

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

- Cadastrar clientes com CPF obrigatório e único, abrindo automaticamente a primeira conta com saldo zero.
- Gerar IDs de clientes e números de contas automaticamente, em sequência (contas: `000001`, `000002`, ...).
- Exibir o número da primeira conta logo após cadastrar o cliente.
- Abrir contas adicionais buscando o nome completo ou parte dele, selecionando o titular na lista com CPF e contas existentes e confirmando a abertura. Não é necessário saber o ID interno do cliente.
- Listar contas com número, nome do titular, CPF e saldo, inclusive logo após o cadastro.
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
A numeração é sequencial durante a execução e reinicia ao abrir o programa novamente.
O CPF é validado pelo formato de 11 dígitos, sem cálculo dos dígitos verificadores.
Os modelos são mutáveis; use o serviço `Banco` para executar operações.
Não há autenticação, persistência ou suporte a operações concorrentes.
Uma evolução possível é adicionar SQLite, autenticação e uma API HTTP.
