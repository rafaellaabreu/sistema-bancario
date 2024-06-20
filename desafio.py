import textwrap
import os
from time import sleep
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

# cores
c = ('\033[m',       #0 - sem cor
    '\033[0;31m',    #1 - vermelho
    '\033[0;32m',    #2 - verde
    '\033[0;33m',    #3 - amarelo
    '\033[0;36m',    #4 - azul
    '\033[0;30m',    #5 - branco
    '\033[0;34m',    #6 - roxo
     )

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
    def __str__(self):
        return f"""\
            Nome:\t\t{self.nome}
            CPF:\t\t{self.cpf}
            Data de Nascimento:\t\t{self.data_nascimento}
            Endereço:\t\t{self.endereco}
        """

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(c[1],'\nOperação falhou! Você não tem saldo suficiente.\n', c[0])

        elif valor > 0:
            self._saldo -= valor
            print(c[4],'\n\tSaque realizado com sucesso!\n', c[0])
            sleep(1.5)
            os. system('cls')
            return True

        else:
            print(c[1],'\nOperação falhou! O valor informado é inválido.\n', c[0])

        sleep(1.5)
        os. system('cls')
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(c[4],'\n\tDepósito realizado com sucesso!\n', c[0])
        else:
            print(c[1],'\nOperação falhou! O valor informado é inválido.\n', c[0])
            sleep(1.5)
            os. system('cls')
            return False

        sleep(1.5)
        os. system('cls')
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(c[1],'\nOperação falhou! O valor do saque excede o limite.\n', c[0])

        elif excedeu_saques:
            print(c[1],'\nOperação falhou! Número máximo de saques excedido.\n', c[0])

        else:
            return super().sacar(valor)

        sleep(1.5)
        os. system('cls')
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                #"data": datetime.strftime("%d/%m/%Y %H:%M"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    print(c[4])
    print('-='*20)
    print('\t   Sistema Bancário')
    print('-='*20, c[0])

    # Variável com as opções:
    menu = """    
    
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNovo Usuário
    [5]\tListar Usuários
    [6]\tNova Conta
    [7]\tListar contas  
    [8]\tSair
    
    => """

    return input(menu).lower().strip()[0]
    

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(c[1],'\n\tCliente não possui conta!\n', c[0])
        sleep(1.5)
        os. system('cls')
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes, cor=0):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(c[1],'\n\tCliente não encontrado!\n', c[0])
        sleep(1.5)
        os. system('cls')
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes, cor=0):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(c[1],'\n\tCliente não encontrado!\n', c[0])
        sleep(1.5)
        os. system('cls')
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes, cor=0):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print(c[1],'\n\tCliente não encontrado!\n', c[0])
        sleep(1.5)
        os. system('cls')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    os. system('cls')
    print(c[3])
    print('-='*20)
    print('\t  Extrato ')
    print('-='*20, c[0])

    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print('-='*20)


def criar_cliente(clientes):
    cpf = str(input('Informe o CPF [somente números]: ')).strip()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(c[1],'\n\tJá existe cliente com esse CPF!\n', c[0])
        sleep(1.5)
        os. system('cls')
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print(c[2],'\n\tCliente criado com sucesso\n', c[0])
    sleep(1.5)
    os. system('cls')
    

def listar_usuarios(clientes):
    if len(clientes) == 0:
        print(c[1],'\n\tNão existe cliente cadastrado!\n', c[0])

    for usuario in clientes:
        print(textwrap.dedent(str(usuario)))
        print(c[4],'-='*20)
        print(c[0])
    
    sleep(3)
    os. system('cls')


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(c[1],'\n\tUsuário não encontrado\n', c[0])
        sleep(1.5)
        os. system('cls')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(c[2],'\n\tConta criada com sucesso!\n', c[0])
    sleep(1.5)
    os. system('cls')


def listar_contas(contas):
    if len(contas) == 0:
        print(c[1],'\n\tNão existe conta cadastrada!\n', c[0])

    for conta in contas:
        print(textwrap.dedent(str(conta)))
        print(c[4],'-='*20)
        print(c[0])
    
    sleep(2)
    os. system('cls')

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        # Função depositar
        if opcao == '1':
            depositar(clientes)
            
        # Função sacar
        elif opcao == '2':
            sacar(clientes)
        
        # Função extrato
        elif opcao == '3':
            exibir_extrato(clientes)
        
        # Função criar usuario
        elif opcao == '4':
            criar_cliente(clientes)

        # Função listar usuários
        elif opcao == '5':
            listar_usuarios(clientes)

        # Função criar conta
        elif opcao == '6':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        # Funçao listar contas
        elif opcao == '7':
            listar_contas(contas)

        # Opção SAIR
        elif opcao == '8':
            break
         
        # Caso a opção seja inválida   
        else:
            print(c[1],'\nOpção inválida! Por favor selecione a opção desejada.', c[0])
            sleep(1.5)
            os. system('cls')

    os. system('cls')
    print('\n\n\n')
    print(c[4],'-='*20)
    print('   Operação finalizada. Volte Sempre!')
    print('-='*20, c[0])

main()



