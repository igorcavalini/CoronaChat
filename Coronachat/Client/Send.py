import threading
import socket
import sys


class Send(threading.Thread):
	'''
	Thread de envio que espera a entrada do usuário na CLI.

	Attributes:
		sock (socket.socket): Objeto socket conectado.
		name (str): Nome de usuário fornecido pelo usuário.
	'''
	def __init__(self, sock, name):
		super().__init__()
		self.sock = sock
		self.name = name


	def run(self):
		'''
		Espera a entrada do usuário na CLI e a envia ao servidor.
		Digitar 'QUIT' fechará a conexão e sairá do aplicativo.
		'''
		while True:
			self.message = input(f'{self.name}: ')
			sys.stdout.flush()
			self.message = sys.stdin.readline()[:-1]

			# leave of app typing 'QUIT'
			if self.message == 'QUIT':
				self.sock.sendall(f'Server: {self.name} saiu do chat.')
				break
			else:
				self.sock.sendall(f'{self.name}: {self.message}')

		print('\nSaindo...')
		self.sock.close()
