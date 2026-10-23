"""Interface de terminal do simulador."""

from .exceptions import ErroBancario
from .services import Banco


def ler_valor() -> str:
    return input("Valor (ex.: 100,50): ").strip().replace(",", ".")


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
                print(f"Cliente cadastrado. ID: {cliente.id}")
                print(f"Conta aberta automaticamente: {conta.numero}")
            elif opcao == "2":
                conta = banco.abrir_conta(int(input("ID do cliente: ")))
                print(f"Conta aberta: {conta.numero}")
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
        except ValueError:
            print("Informe um ID numérico válido.")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o simulador.")
            break
