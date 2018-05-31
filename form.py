#!--*--coding:utf-8--*--

class Form:

	def __init__(self, sommets):
		self.scale = 100
		self.sommets = sommets

	def get_sommets(self, size = 100):
		sommets = []
		size = float(size)/self.scale
		for sommet in self.sommets:
			sommets.append([sommet[0]*size, sommet[1]*size])
		return sommets

	def ptMoyen(self, size = 100):
	    x, y = 0, 0

	    for sommet in self.get_sommets(size):
	        x += sommet[0]
	        y += sommet[1]

	    l = len(self.sommets)
	    y /= l
	    x /= l
	    return[x, y]

	def build_equations(self, size = 100):
		equations = []
		sommets = self.get_sommets(size)

		for i in range(len(sommets)-1):
			first_point = sommets[i]
			second_point = sommets[i+1]
			equations.append(equation(first_point, second_point))

		equations.append(equation(sommets[i+1], sommets[0]))

		return equations

	def build_vect_equations(self, size = 100):
		equations = self.build_equations(size)
		vect_eq = []
		for eq in equations:
			vect_eq.append(equation_analyze(eq, self.ptMoyen()))

		return vect_eq

	def isOn(self, p, size = 100):
		equations = self.build_equations(size)
		isOn = True
		sommets = self.get_sommets(size)

		for eq in equations:
			isOn &= equation_analyze(eq, self.ptMoyen(size)) == equation_analyze(eq, p)

		return isOn

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

def equation_analyze(eq, p):
	vect_eq = [eq]
	dir_x, dir_y = 0, 0

	if len(eq) == 1:
		diff_x = (p[0] - eq[0])
		dir_x = diff_x / abs(diff_x) if diff_x != 0 else 0
		dir_y = 0
	elif eq[0] == 0:
		diff_y = p[1] - eq[1]
		dir_x = 0
		dir_y = diff_y / abs(diff_y) if diff_y != 0 else 0
	else:
		new_x = (p[1] - eq[1]) / eq[0]
		new_y = eq[0] * p[0] + eq[1]
		diff_x = p[0] - new_x
		diff_y = p[1] - new_y
		dir_x = diff_x / abs(diff_x) if diff_x != 0 else 0
		dir_y = (diff_y) / abs(diff_y) if diff_y != 0 else 0
	return[eq, dir_x, dir_y]