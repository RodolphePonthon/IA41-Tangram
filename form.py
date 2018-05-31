#!--*--coding:utf-8--*--

class Form:

	def __init__(self, sommets):
		self.sommets = sommets
		self.scale = 100

	def get_sommets(self):
		return self.sommets

	def get_sommets_size(self, size):
		sommets = []
		size = float(size)/self.scale
		for sommet in self.sommets:
			sommets.append([sommet[0]*size, sommet[1]*size])
		return sommets

	def borderControl(self):
		equations = []
		for i in range(len(self.sommets)-1):
			first_point = self.sommets[i]
			second_point = self.sommets[i+1]
			equations.append(equation(first_point, second_point))

		equations.append(equation(self.sommets[i+1], self.sommets[0]))

		return equations

def equation(first_point, second_point):
	if second_point[0] == first_point[0]:
		equation = [second_point[0]]
	elif second_point[1] == first_point[1]:
		equation = [0, second_point[1]]
	elif first_point[0] == 0:
		b = first_point[1]
		a = (second_point[1] - b) / second_point[0]
		equation = [a,b]
	elif second_point[0] == 0:
		b = second_point[1]
		a = (first_point[1] - b) / first_point[0]
		equation = [a,b]
	else:
		a = (second_point[1] - first_point[1]) / (second_point[0] - first_point[0])
		b = first_point[1] - a * first_point[0]
		equation = [a,b]

	return equation