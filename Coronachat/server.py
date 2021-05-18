import threading
import tkinter as tk
import utils as utils

import Coronachat.Server as Server




def start_server(host, window):

    #Inicia o servidor com base no host passado na GUI.


    window.destroy() # FINALIZA A JANELA QUE PEDIU O HOST
    server = Server.Server(host, 1060) # INICIA O SERVER PASSANDO O HOST E PORTA
    server.start() # STARTA O SERVER

    exit = threading.Thread(target=utils.exit, args=(server,))
    exit.start() #THREAD QUE PERMITE AO ADM DO SERVER FINALIZAR A CONEXÃO



if __name__ == "__main__":
    window = tk.Tk()  # CRIA A JANELA QUE VAI SOLICITAR O ENDEREÇO DE HOST
    window.title('Conexão do Server')
    window.resizable(height=False, width=False)

    host_input = tk.Entry(master=window,   # RECEBE A ENTRADA DO USUÁRIO
                          width='50',
                          borderwidth=18,
                          bg='#ccc',
                          relief=tk.FLAT,
                          font='Times 10')
    host_input.pack(fill=tk.BOTH, expand=True)

    host_input.insert(0,  # TEXTO DO INPUT
                      "Digite o endereço de host para o servidor: localhost")

    host_input.bind("<Button-1>", # DELETA O TEXTO DO INPUT AO CLICAR
                    lambda x: host_input.delete(0, tk.END))
    host_input.bind("<Return>",# CHAMA A DEF START SERV PASSANDO O HOST E A JANELA
                    lambda x: start_server(host_input.get(), window))

    width = 450
    heigth = 50
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (heigth // 2)
    window.geometry('{}x{}+{}+{}'.format(width, heigth, x, y))

    window.mainloop()

