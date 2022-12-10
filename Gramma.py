# Класс грамматика
class Gramma:

	# Коструктор класса грамматики
	# N - мноество нетерминалов - set()
	# T - множество терминалов - set()
	# P - словарь правил вывода - dict()
	# S - строковая аксиома - string
	def __init__(self, N, T, P, S):
		self.N = N
		self.T = T
		self.P = P
		self.S = S

	def printGramma(self):
		print('Нетерминалы : ', self.N)
		print('Терминалы : ', self.T)
		print('Правила вывода : ')
		for key in self.P:
			print('\t',key,' -> ', '|'.join(map(str, self.P[key])))
		print('Аксиома : ', self.S)