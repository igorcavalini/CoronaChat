import threading
import socket
import tkinter as tk
from datetime import datetime
from win10toast import ToastNotifier
from winsound import *
import os



class Recebe(threading.Thread):
	"""
	A thread de recebimento escuta as mensagens recebidas do servidor.

	Attributes:
		sock (socket.socket): Objeto socket conectado.
		name (str): Nome de usuário fornecido pelo usuário.
		mensagens (tk.Listbox): Objeto tk.Listbox que contém todas as mensagens exibidas na GUI.
	"""
	def __init__(self, sock, name):
		super().__init__()
		self.sock = sock
		self.name = name
		self.mensagens = None

	def run(self):
		"""
		Recebe dados do CLIENTE e os exibe na GUI.
		Sempre escuta os dados de entrada até que uma das extremidades feche o socket.
		"""
		while True:
			self.mensagem = self.sock.recv(1024).decode('ascii')
			if self.mensagem == 'quit':
				self.sock.close()


			if self.mensagem:

				if self.mensagens:


					now = datetime.now()
					timestamp = now.strftime("%H:%M:%S")
					self.mensagens.insert(
					    tk.END, '(' + str(timestamp) + ')' + ' ' + self.mensagem)

					# Notificação windows
					if os.name == 'nt':
						PlaySound('notification.wav', SND_FILENAME)
						toaster = ToastNotifier()
						toaster.show_toast(self.mensagem)


				else:
					print('\r{}\n{}: '.format(self.mensagem,
											  self.name).encode('ascii'),
					      end='')
			else:
				# Server has closed the socket, exit the program
				print('\nOh não, perdemos conexão com o server.')
				print('\nSaindo...')
				self.sock.close()