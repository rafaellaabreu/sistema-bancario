import os
from time import sleep
from datetime import date

# cores
c = ('\033[m',       #0 - sem cor
    '\033[0;31m',    #1 - vermelho
    '\033[0;32m',    #2 - verde
    '\033[0;33m',    #3 - amarelo
    '\033[0;36m',    #4 - azul
    '\033[0;30m',    #5 - branco
    '\033[0;34m',    #6 - roxo
     )


def menu():
    print(c[4])
    print('-='*20)
    print('\t   Sistema Bancário')
    print('-='*20, c[0])

    # Variável com as opções:
    menu = """    
    Menu de Opções
    --------------
    [d]  Depósito
    [s]  Sacar
    [e]  Extrato
    [u]  Criar Usuário
    [lu] Listar usuários
    [c]  Criar Conta
    [lc] Listar contas  
    [q]  Sair
    
    """

    return input(menu).lower().strip()[0]
    

def depositar(saldo, valor, extrato, /, cor=0):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito:\tR$ {valor:.2f}\n'
        print(c[2],'\n\tDepósito realizado com sucesso!\n', c[0])
    else:
        print(c[1],'\nOperação falhou! Valor informado é inválido.\n', c[0])
    sleep(1.5)
    os. system('cls')
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES, cor=0):
    if numero_saques < LIMITE_SAQUES:
        if valor < saldo:
            if valor <= limite:
                if valor > 0:
                    saldo -= valor
                    numero_saques += 1
                    extrato += f'Saque:\t\tR$ {valor:.2f}\n'
                    print(c[2],'\n\tSaque realizado com sucesso!\n', c[0])
                else:
                    print(c[1],'\nOperação falhou! O valor informado é inválido.\n', c[0])
            else:
                print(c[1],'\nOperação falhou! Limite máximo de R$ 500,00 por saque.\n', c[0])
        else:
            print(c[1],'\n\tOperação falhou! Saldo insuficiente!\n', c[0])
    else:
        print(c[1],'\nOperação falhou! Limite de saque diário excedido.\n', c[0])
    
    sleep(1.5)
    os. system('cls')
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato, cor=0):
    os. system('cls')
    print(c[3])
    print('-='*20)
    print('\t  Extrato Bancário')
    print('-='*20, c[0])
    print(c[6],f'\tData atual: {date.today()}\n', c[0])
    print('Não foram realizadas movimentações' if not extrato else extrato)
    print(f'\nSaldo: R$ {saldo:.2f}\n')
    print('-='*20)


def criar_usuario(usuarios):
    cpf = str(input('Informe o CPF [somente números]: ')).strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(c[1],'\n\nJá existe usuário com esse CPF.\n', c[0])
        return 
    
    nome = str(input('Informe o nome completo: ')).title().strip()
    data = str(input('Informe a data de nascimento [dd-mm-aaaa]: ')).strip()

    end = str(input('Informe o endereço: [logradouro, nro - bairro - cidade/estado.]: ')).strip()
       
    usuarios.append({'cpf':cpf, 'nome':nome, 'data':data, 'end':end})
    
    print(c[2],'\n\tCadastro realizado com sucesso!\n', c[0])
    
    sleep(2)
    os. system('cls')


def filtrar_usuario(cpf, usuarios):
    filtro = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return filtro[0] if filtro else None


def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(f'CPF:                {usuario['cpf']}\nNome:               {usuario['nome']}\nData de Nascimento: {usuario['data']}\nEndereço:           {usuario['end']}')
        print(c[4],'-='*30)
        print(c[0])
    

def criar_contas(agencia, contador_conta, usuarios):
    cpf = str(input('Informe o CPF [somente números]: ')).strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print(c[2],'\n\tConta criada com sucesso!\n', c[0])
        return {'agencia':agencia, 'contador_conta':contador_conta, 'usuario':usuario}
    else:
        print(c[1],'\n\tUsuário não encontrado\n', c[0])

    sleep(2)
    os. system('cls')
    

def listar_contas(contas):
    for conta in contas:
        print(f'Agência:\t{conta['agencia']}\nC/C:\t\t{conta['contador_conta']}\nTitular:\t{conta['usuario']['nome']}')
        print(c[4],'-='*20)
        print(c[0])
    

def main():
    # Variáveis diversas:
    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    LIMITE_SAQUES = 3 # Constante
    AGENCIA = '001'
    usuarios = list()
    contas = list()  
    contador_conta = 1

    while True:
        opcao = menu()

        # Função depositar
        if opcao == 'd':
            valor = float(input('Valor do depósito: R$ '))
            # Argumentos por posição
            saldo, extrato = depositar(saldo, valor, extrato)
            
        # Função sacar
        elif opcao == 's':
            valor = float(input('Valor que deseja sacar: R$ '))
            # Argumentos por nome
            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        
        # Função extrato
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
        
        # Função criar usuario
        elif opcao == 'u':
            criar_usuario(usuarios)

        # Função listar usuários
        elif opcao == 'lc':
            listar_usuarios(usuarios)

        # Função criar conta
        elif opcao == 'c':
            #contador_conta = len(contas) + 1
            conta = criar_contas(AGENCIA, contador_conta, usuarios)

            if conta:
                contas.append(conta)
                contador_conta += 1

        # Funçao listar contas
        elif opcao == 'lc':
            listar_contas(contas)

        # Opção SAIR
        elif opcao == 'q':
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



