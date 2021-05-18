import threading


class ServerSocket(threading.Thread):
	"""
	Suporta comunicações com um cliente conectado.

	Atributos:
		sc (socket.socket): Socket conectado.
		sockname (tuple): Endereço do socket do client.
		server (Server): Thread pai.
	"""
	def __init__(self, sc, sockname, server):
		super().__init__()
		self.sc = sc
		self.sockname = sockname
		self.server = server

	def run(self):
		"""
		Recebe dados do cliente conectado e transmite a mensagem para todos os outros clientes.
		Se o cliente saiu da conexão, fecha o socket conectado e remove a si mesmo da lista
		de threads ServerSocket no thread de servidor pai.
		"""
		while True:
			mensagem = self.sc.recv(1024).decode('ascii')
			if mensagem:
				print(f'{self.sockname} diz {mensagem}')
				self.server.broadcast(mensagem, self.sockname)
			else:
				print(f'{self.sockname} fechou a conexão.')
				self.sc.close()
				self.server.remove_connection(self)
				return

	def send(self, mensagem):
		"""
		Envia uma mensagem ao servidor conectado

		"""
		self.sc.sendall(mensagem.encode('ascii'))