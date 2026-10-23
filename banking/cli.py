"""Interface de terminal do simulador."""

from .exceptions import ErroBancario
from .services import Banco


def ler_valor() -> str:
    return input("Valor (ex.: 100,50): ").strip().replace(",", ".")


def abrir_conta_adicional(banco: Banco) -> None:
    clientes = banco.buscar_clientes_por_nome(input("Nome do cliente (ou parte dele): "))
    if not clientes:
        print("Nenhum cliente encontrado com esse nome.")
        return
    print("Clientes encontrados:")
    for indice, cliente in enumerate(clientes, start=1):
        numeros = ", ".join(conta.numero for conta in banco.listar_contas()
                            if conta.cliente.id == cliente.id)
        print(f"{indice} - {cliente.nome} | CPF: {cliente.cpf} | Contas: {numeros}")
    escolha = input("Selecione o cliente pelo número da lista (0 para cancelar): ").strip()
    if escolha == "0":
        print("Abertura cancelada.")
        return
    try:
        indice = int(escolha)
    except ValueError:
        print("Seleção inválida. Nenhuma conta foi aberta.")
        return
    if not 1 <= indice <= len(clientes):
        print("Seleção inválida. Nenhuma conta foi aberta.")
        return
    cliente = clientes[indice - 1]
    confirmacao = input(
        f"Abrir conta adicional para {cliente.nome}, CPF {cliente.cpf}? (s/n): "
    ).strip().casefold()
    if confirmacao not in ("s", "sim"):
        print("Abertura cancelada.")
        return
    conta = banco.abrir_conta(cliente.id)
    print(f"Conta adicional aberta: {conta.numero} | Titular: {cliente.nome}")


def main() -> None:
    banco = Banco()
    print(f"Bem-vindo ao {banco.nome}!")
    while True:
        print("\n1 - Cadastrar cliente e abrir conta\n2 - Abrir conta adicional\n3 - Listar contas"
              "\n4 - Depositar\n5 - Sacar\n6 - Transferir\n7 - Extrato\n0 - Sair")
        try:
            opcao = input("Opção: ").strip()
            if opcao == "0":
                break
            if opcao == "1":
                cliente = banco.cadastrar_cliente(input("Nome: "), input("CPF: "))
                conta = next(c for c in banco.listar_contas() if c.cliente.id == cliente.id)
                print(f"Cliente cadastrado: {cliente.nome} | CPF: {cliente.cpf}")
                print(f"Conta aberta automaticamente: {conta.numero}")
            elif opcao == "2":
                abrir_conta_adicional(banco)
            elif opcao == "3":
                contas = banco.listar_contas()
                if not contas:
                    print("Nenhuma conta cadastrada.")
                for conta in contas:
                    print(f"{conta.numero} | {conta.cliente.nome} | CPF: {conta.cliente.cpf} | R$ {conta.saldo:.2f}")
            elif opcao in ("4", "5"):
                numero = input("Conta: ").strip()
                operacao = banco.depositar if opcao == "4" else banco.sacar
                operacao(numero, ler_valor())
                print("Operação concluída.")
            elif opcao == "6":
                origem = input("Conta de origem: ").strip()
                destino = input("Conta de destino: ").strip()
                banco.transferir(origem, destino, ler_valor())
                print("Transferência concluída.")
            elif opcao == "7":
                numero = input("Conta: ").strip()
                for transacao in banco.extrato(numero):
                    data = transacao.data.astimezone().strftime("%d/%m/%Y %H:%M")
                    print(f"{data} | {transacao.tipo.value} | R$ {transacao.valor:.2f}")
                print(f"Saldo: R$ {banco.buscar_conta(numero).saldo:.2f}")
            else:
                print("Opção inválida.")
        except ErroBancario as exc:
            print(f"Erro: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o simulador.")
            break
