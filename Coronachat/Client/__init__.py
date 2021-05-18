import socket
import tkinter as tk
from datetime import datetime

import pyautogui
import time
import pyperclip
from Coronachat.Client import  recebe



def get_name(entry, window, obj):
    """
    Captura o nome do usuário pela interface gráfica.

    Atributos:
        entry (tk.Entry): Campo de entrada para o nome do usuário.
        window (tk.Frame): Janela da interface gráfica onde é localizado o campo de entrada.
        obj (Client): Objeto do tipo Client.
    """
    obj.name = entry.get()
    window.destroy()


class Client:
    """
    Oferece suporte ao gerenciamento de conexões cliente-servidor.

    Atributos:
        host (str): Endereço IP do socket de escuta do servidor.
        port (int): Número da porta do socket de escuta do servidor.
        sock (socket.socket): Objeto socket conectado.
        name (str): Nome de usuário do cliente.
        mensagens (tk.Listbox): Objeto tk.Listbox que contém todas as mensagens exibidas na GUI.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.mensagens = None

    def start(self):
        """
        Estabelece a conexão cliente-servidor.

        """


        print(f'Tentando se conectar com {self.host}:{self.port}...')
        self.sock.connect((self.host, self.port))
        print(f'Conectado com sucesso a {self.host}:{self.port}\n')

        # INTERFACE
        window = tk.Tk()
        window.title('Cliente - Nome')
        window.resizable(height=False, width=False)

        host_input = tk.Entry(master=window,
                              width='50',
                              borderwidth=18,
                              bg='#ccc',
                              relief=tk.FLAT,
                              font='Times 10')
        host_input.pack(fill=tk.BOTH, expand=True)

        host_input.insert(0,
                          "Digite o nome desejado sem caracteres especiais.")
        host_input.bind("<Button-1>", lambda x: host_input.delete(0, tk.END))
        host_input.bind("<Return>",
                        lambda x: get_name(host_input, window, self))

        width = 350
        heigth = 50
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (heigth // 2)
        window.geometry('{}x{}+{}+{}'.format(width, heigth, x, y))

        window.mainloop()


        print(
            f'\nBem Vindo, {self.name}! Preparando para enviar mensagens...'
        )

        # CRIA A THREAD QUE RECEBE E ENVIA MENSAGENS
        receive = recebe.Recebe(self.sock, self.name)

        # STARTA A THREAD RECEBE
        receive.start()




        self.sock.sendall('Server: {} acabou de se juntar ao chat, diga ola!'.format(
            self.name).encode('ascii'))




        return receive

    def send(self, text_input):
        """
        Envia dados text_input da GUI.

        """

        #DATA E HORA ATUAL
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")

        #botchat
        casos = 'Tabatinga registrou 45 novos casos, nos últimos 7 dias!'
        ncasos= 45
        tcasos = 'Tabatinga chegou ao total de 1840 casos de covid-19!'
        ntcasos = 1840
        mortes = 'Tabatinga registra até o momento 49 óbitos por covid-19!'
        nmortes = 49
        curados = 'Em Tabatinga, 1286 pessoas foram curadas da covid-19!'
        ncurados = 1286
        suspeitos = 'Tabatinga possui 84 suspeitos de covid-19!'
        nsuspeitos = 84
        link_dicas = 'https://www.gov.br/saude/pt-br/coronavirus/como-se-proteger'
        link_email = 'https://mail.google.com/mail/u/0/#inbox'
        email = 'igorcavalini15@gmail.com'
        assunto = 'Boletim diário da covid-19'
        texto_email = f"""
        Prezados, bom dia
        
                     #Casos
        O número de casos registrados na cidade nos últimos 7 dias foi de: {ncasos} pessoas;
        O número total de casos chegou a marca de: {ntcasos} pessoas;
        ---------------------------------------------------------------------------------------
                     #Mortes
        O número de mortes por covid-19 na cidade já é de: {nmortes} pessoas;
        ---------------------------------------------------------------------------------------
                     #Curados
        O número de curados da covid-19 na cidade é de: {ncurados} pessoas;
        ---------------------------------------------------------------------------------------
                     #Suspeitos
        A cidade registra um total de {nsuspeitos} suspeitos de covid-19
        ---------------------------------------------------------------------------------------
        
        Abraços,
        Pay-tha-on
         
        
        """


        mensagem = text_input.get() # RECEBE A ENTRADA DO USUÁRIO
        text_input.delete(0, tk.END)


        self.mensagens.insert(   # INSERE A MENSAGEM NO CHAT
                tk.END,
                '{}: {}'.format('(' + str(timestamp) + ')' + ' ' + self.name,
                                mensagem).encode('ascii'))



        if mensagem == '!novoscasos':
            self.mensagens.insert(
                tk.END,
                '{}: {}'.format('(' + str(timestamp) + ')' + ' ' + 'Server',casos
                                ))
        if mensagem == '!casos':
            self.mensagens.insert(
                    tk.END,
                    '{}: {}'.format('(' + str(timestamp) + ')' + ' ' + 'Server', tcasos
                                    ))
        if mensagem == '!mortes':
                                self.mensagens.insert(
                                    tk.END,

                    '{}: {}'.format('(' + str(timestamp) + ')' + ' ' + 'Server', mortes
                                    ))
        if mensagem == '!curados':
            self.mensagens.insert(
                tk.END,
                '{}: {}'.format('(' + str(timestamp) + ')' + ' ' + 'Server', curados
                                ))
        if mensagem == '!suspeitos':
            self.mensagens.insert(
                tk.END,
                '{}: {}'.format('(' + str(timestamp) + ')' + ' ' + 'Server', suspeitos
                                ))
        if mensagem == '!dicas' :
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write('chrome')

            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            #pyautogui.click(414, 50)

            pyautogui.write(link_dicas)
            pyautogui.press('enter')

        if mensagem == '!enviar_relatorio':
            pyautogui.press('win')
            time.sleep(3)
            pyautogui.write('chrome')

            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(3)

            pyautogui.write(link_email)
            pyautogui.press('enter')
            time.sleep(8)

            pyautogui.click(50,200)
            time.sleep(8)

            pyautogui.write(email)
            pyautogui.press('tab')
            time.sleep(8)

            pyautogui.press('tab')
            pyperclip.copy(assunto)
            pyautogui.hotkey('ctrl','v')
            time.sleep(1)

            pyautogui.press('tab')
            pyperclip.copy(texto_email)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl','enter')



        if mensagem == 'quit':


            self.sock.sendall('Server: {} saiu do chat.'.format(
                self.name).encode('ascii'))


            print('\n Saindo...')
            self.sock.close()



        else:
            self.sock.sendall('{}: {}'.format(self.name,
                                              mensagem).encode('ascii'))