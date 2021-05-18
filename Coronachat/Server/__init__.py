import threading

import socket
import Coronachat.Server.ServerSocket as ServerSocket



class Server(threading.Thread):
    """
    Suporta gerenciamento de conexões de servidor.

    """



      # CONSTRUTOR
    def __init__(self, host, port):
        super().__init__()

        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        """
        Cria o socket de escuta. O socket de escuta usará a opção SO_REUSEADDR para
        permitir a ligação a um endereço de socket usado anteriormente.
        Para cada nova conexão, um thread ServerSocket é iniciado .
        Todos os objetos ServerSocket são armazenados no atributo connections.
        """
        # AF_INET: FAMILIA DE ENDEREÇOS
        # SOCK_STREAM: TIPO DE SOCKET
        # SOL_SOCKET:  REFERENCIA AO NIVEL DE SOQUETE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port)) # ASSOCIA O SOQUETE AO ENDEREÇO LOCAL

        sock.listen(1) # MAXIMO DE CONEXÃO EM ESPERA
        print(f'Ouvindo em {sock.getsockname()}')

        # ESCUTA POR NOVAS CONEXÕES
        while True:

            sc, sockname = sock.accept()
            print(
                f'Nova conexao de {sc.getpeername()} para {sc.getsockname()}'
            )

            # NOVA THREAD
            server_socket = ServerSocket.ServerSocket(sc=sc, sockname=sockname, server=self)
            # STARTA A THREAD
            server_socket.start()

            # ADICIONA A THREAD PARA INICIAR CONEXÕES
            self.connections.append(server_socket)
            print(f'Pronto para receber mensagens de {sc.getpeername()}')

    def broadcast(self, mensagem, source):
        """
        Envia uma mensagem para todos os clientes conectados,
        exceto a origem da mensagem.


        """
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(mensagem)

    def remove_connection(self, connection):
        """
        Remove uma thread ServerSocket do atributo connections.

        """
        self.connections.remove(connection)