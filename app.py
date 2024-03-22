from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
from colorama import Fore, init

init(autoreset=True,convert=True)

api = IQ_Option('xxxxxxx0@gmail.com','(xxxxxxx)',('PRATICE'))
api.connect()


if api.check_connect():
    print('[IQOption]: conectado')
else:
    print('[IQOption]: Email/Senha Inválidos...')    

#$ Pegando Informações do usuário
par = input('Digite o ativo para operar MHI:')
investimento = input('Digite o valor das suas entradas:')
timeframe = int(input('Digite o timeframe(exemplo: 1,5,15...):'))
    

while True:
    horario = float(datetime.now().strftime('%M.%S')[1:])
    entrar = True if (horario >= 4.58 and horario <= 5.0 or horario >= 9.58) else False
    print('Aguardando operação MHI, tempo:', horario)
    
    if entrar:
        print(f'\n[ {Fore.GREEN}*{Fore.RESET} ]: Operação MHI(tempo atingido)')
        print('Analisando cores[IqOption]:',end='')
        
        dir = None
        
        vela = api.get_candles(par,timeframe*60,3,time.time())
        
        #$ Análise das velas
        vela[0] = 'g' if vela[0]['open'] < vela[0]['close'] else 'r' if vela[0]['open'] > vela[0]['close'] else 'd'
        vela[1] = 'g' if vela[1]['open'] < vela[1]['close'] else 'r' if vela[1]['open'] > vela[1]['close'] else 'd'
        vela[2] = 'g' if vela[2]['open'] < vela[2]['close'] else 'r' if vela[2]['open'] > vela[2]['close'] else 'd'
        
        cores = vela[0] + ' ' + vela[1] + ' ' + vela[2]
        print(cores)
        
        
        if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = 'PUT' 
        if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = 'CALL'
        
        if dir != None:
            status, id = api.buy_digital_spot_v2(par,investimento,dir,timeframe)
            if status == True:
                print(f'{Fore.GREEN}operação realizada, aguardando resultado{Fore.RESET}')
                
                while True:
                    status, lucro = api.check_win_digital_v2(id)
                    if status == True:
                        if lucro > 0:
                            print(f'Resultado da operação: {Fore.GREEN}Win{Fore.RESET}')
                            print('Lucro:', round(lucro,2),'\n')
                            break
                        else:                            
                            print('Resultado da operação: {Fore.RED}Loss{Fore.RESET}')
                            print('Perda:', round(lucro,2),'\n')
                            break
                    
                    
            else: 
                print(f'{Fore.RED}Operação não realizada, ocorreou algum erro{Fore.RESET}')
                
    time.sleep(1)            
    
    
