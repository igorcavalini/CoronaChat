import tkinter as tk
import Client as Client


import os




def main(host, port):
    """
    Configuração do cliente e inicializa a interface gráfica.

    Atributos:
        host (str): Endereço IP do socket.
        port (int): Número da porta do socket.
    """
    # Janela
    client = Client.Client(host, port)  # INSTANCIA O CLIENTE
    cliente_start = client.start() # STARTA O CLIENTE
    window = tk.Tk()                    # INICIALIZA GUI
    window.title('CoronaChat')
    window.resizable(height=False, width=False)
    if os.name == 'nt':     # ALTERA O ICONE DA GUI PARA WINDOWS
        window.iconbitmap('img/icon.ico')

    window.config(background='#3c3939')

    # Componentes
    frm_messages = tk.Frame(master=window, bg='#3c3939') # CONTAINER
    scrollbar = tk.Scrollbar(master=frm_messages)  # ROLAGEM
    mensagens = tk.Listbox(master=frm_messages,    # LISTA DE ITENS
                          yscrollcommand=scrollbar.set,
                          fg='white',
                          bg='#3c3939',
                          borderwidth=0,
                          highlightthickness=0,
                          )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    mensagens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.mensagens = mensagens
    cliente_start.mensagens = mensagens


    frm_messages.pack(fill='both', expand=True, padx=10, pady=10)

    # INPUT
    frm_entry = tk.Frame(master=window)    # CONTAINER
    text_input = tk.Entry(master=frm_entry,  # RECEBE ENTRADA
                          borderwidth=18,
                          bg='#2f4f4f',
                          fg='white',
                          relief=tk.FLAT,
                          font='Times 10')
    text_input.pack(fill=tk.BOTH, expand=True)

    text_input.insert(0, "Digite algo e aperte enter.") # TEXTO DO INPUT
    text_input.bind("<Button-1>", # APAGA O TEXTO DO INPUT AO CLICAR
                    lambda x: text_input.delete(0, tk.END))
    text_input.bind("<Return>", # CHAMA A DEF SEND PASSANDO O QUE O USUÁRIO DIGITOU
                    lambda x: client.send(text_input))



    # Pack ou Grid
    frm_entry.pack(fill='both')

    # Configs
    width = 450
    heigth = 550
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (heigth // 2)
    window.geometry('{}x{}+{}+{}'.format(width, heigth, x, y))

    window.mainloop()



def redirect(host, port, window):
    """
    Redireciona o usuário para a sala de bate-papo.

    Atributos:
        host (str): Endereço IP do socket.
        port (int): Número da porta do socket.
        window (tk.Frame): Objeto tk.Frame que contém a interface GUI que será destruida para criação da tela da sala de bate papo.
    """

    window.destroy()
    main(host, port)


if __name__ == "__main__":
    window = tk.Tk() # CRIA A JANELA QUE PEDE O END DE HOST
    window.title('Cliente - Conexão ao Host')
    window.resizable(height=True, width=True)

    host_input = tk.Entry(master=window, # RECEBE A ENTRADA DO USUÁRIO
                          width='50',
                          borderwidth=18,
                          bg='#ccc',
                          relief=tk.FLAT,
                          font='Times 10')
    host_input.pack(fill=tk.BOTH, expand=True)

    host_input.insert( # TEXTO DO INPUT
        0, "Digite o endereço de Host que deseja se Conectar, ex: localhost")
    host_input.bind("<Button-1>", # DELETA O TEXTO DO INPUT AO CLICAR
                    lambda x: host_input.delete(0, tk.END))
    host_input.bind("<Return>", # CHAMA A DEF REDIRECT PASSANDO O HOST, A PORTA E A JANELA
                    lambda x: redirect(host_input.get(), 1060, window))

    width = 450
    heigth = 500
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (heigth // 2)
    window.geometry('{}x{}+{}+{}'.format(width, heigth, x, y))

    window.mainloop()




