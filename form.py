#!--*--coding:utf-8--*--

from math import cos, sin
import copy

class Form:

    def __init__(self, sommets, new_scale = 100):
        self.scale = 100
        self.initial_sommets = sommets
        self.sommets = sommets
        self.new_scale = new_scale

    def initialize(self):
        self.sommets = self.initial_sommets

    def get_sommets(self, size = 100):
        sommets = []
        size = float(size)/self.scale
        for sommet in self.sommets:
            sommets.append([round(sommet[0]*size), round(sommet[1]*size)])
        return sommets

    def ptMoyen(self, size = 100):
        x, y = 0, 0

        for sommet in self.get_sommets(size):
            x += sommet[0]
            y += sommet[1]

        l = len(self.sommets)
        y /= l
        x /= l
        return[round(x), round(y)]

    def isCornerSelected(self, p, size = 100):
        x = p[0]
        y = p[1]
        r = 20
        isSelected = False
        sommets = self.get_sommets(size)
        for sommet in sommets:
            if (sommet[0] - x)**2 + (sommet[1] - y)**2  <= r**2:
                isSelected = True
                break

        return isSelected
        
    def getCornerSelected(self, p, size = 100):
        x = p[0]
        y = p[1]
        r = 20
        sommetSelected = []
        sommets = self.get_sommets(size)
        for sommet in sommets:
            if (sommet[0] - x)**2 + (sommet[1] - y)**2  <= r**2:
                sommetSelected = copy.deepcopy(sommet)
                break

        return sommetSelected

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

    def rotation(self, w):
        rotatedSommets = []
        p = [self.scale/2, self.scale/2]

        for i in range(len(self.sommets)):
            x = (self.sommets[i][0] - p[0]) * cos(w) - sin(w) * (self.sommets[i][1] - p[1]) + p[0]
            y = (self.sommets[i][0] - p[0]) * sin(w) + cos(w) * (self.sommets[i][1] - p[1]) + p[1]
            rotatedSommets.append([x, y])

        self.sommets = rotatedSommets

def equation(first_point, second_point):
    if second_point[0] == first_point[0]:
        equation = [second_point[0], first_point, second_point]
    elif second_point[1] == first_point[1]:
        equation = [0, second_point[1], first_point, second_point]
    elif first_point[0] == 0:
        b = first_point[1]
        a = (second_point[1] - b) / second_point[0]
        equation = [a,b, first_point, second_point]
    elif second_point[0] == 0:
        b = second_point[1]
        a = (first_point[1] - b) / first_point[0]
        equation = [a,b, first_point, second_point]
    else:
        a = (second_point[1] - first_point[1]) / (second_point[0] - first_point[0])
        b = first_point[1] - a * first_point[0]
        equation = [round(a),round(b), first_point, second_point]

    return equation

def equation_analyze(eq, p):
    vect_eq = [eq]
    dir_x, dir_y = 0, 0

    if len(eq) == 3:
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

def equation_solve(eq, x):
    a = eq[0]
    b = eq[1]
    return a*x + b