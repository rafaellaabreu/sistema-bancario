# Variável com as opções:
menu = """
Menu de Opções
--------------
[d] Depósito
[s] Sacar
[e] Extrato
[q] sair

"""

# Variáveis diversas:
saldo = 0
limite = 500
extrato = ''
numero_saques = numero_depositos = 0
LIMITE_SAQUES = 3 # Constante

while True:
    opcao = input(menu).strip()[0]

    if opcao == 'd':
        valor = float(input('Valor do depósito: R$ '))
        if valor > 0:
            saldo += valor
            numero_depositos += 1
            extrato += f'Depósito:\t[{numero_depositos}] = R$ {valor:.2f}\n'
            print('Depósito realizado com sucesso!')
        else:
            print('Operação falhou! Valor informado é inválido.')

    elif opcao == 's':
        '''Forma que fiz o código
        Avalia o número de saques
        if numero_saques < LIMITE_SAQUES:
            valor = float(input('Valor que deseja sacar: R$ '))
            # Avalia se o valor é maior que o limite
            if valor > limite:
                print('Operação falhou! Limite máximo de R$ 500,00 por saque.')
            else:
                # avalia se o valor é maior que o saldo
                if valor > 0:
                    if saldo >= valor:
                        saldo -= valor
                        numero_saques += 1
                        extrato += f'Saque:\t\t[{numero_saques}] = R$ {valor:.2f}\n'
                        print('Saque realizado com sucesso!')
                    else:
                        print('Operação falhou! Saldo insuficiente!')
                else:
                    print('Operação falhou! O valor informado é inválido.')
        else:
            print('Operação falhou! Limite de saque diário excedido.')'''
        
        valor = float(input('Valor que deseja sacar: R$ '))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print('Operação falhou! Saldo insuficiente!')
        elif excedeu_limite:
            print('Operação falhou! Limite máximo de R$ 500,00 por saque.')
        elif excedeu_saques:
            print('Operação falhou! Limite de saque diário excedido.')
        elif valor > 0:
            saldo -= valor
            numero_saques += 1
            extrato += f'Saque:\t\t[{numero_saques}] = R$ {valor:.2f}\n'
            print('Saque realizado com sucesso!')
        else:
            print('Operação falhou! O valor informado é inválido.')

    elif opcao == 'e':
        print('-='*10)
        print('  Extrato Bancário')
        print('-'*20)
        print('Não foram realizadas movimentações' if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}\n')
        print('-='*10)
    elif opcao == 'q':
        break
        
    else:
        print('Opção inválida! Por favor selecione a opção desejada.')
print('-='*20)
print('   Operação finalizada. Volte Sempre!')
print('-='*20)