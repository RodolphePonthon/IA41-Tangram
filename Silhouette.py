#!--*--coding:utf-8--*--

from form import equation
from convert_to_draw import find_equation_with
from copy import deepcopy

class silhouette:
    def __init__(self, list_pts_form):
        list_pts_form_cpy = [deepcopy(pt) for pt in list_pts_form]
        self.couples = creation_couples(list_pts_form_cpy)
        del list_pts_form_cpy[-1]
        self.sommets = list_pts_form_cpy
       
    def clean_couples(self):
        toRemove = []
        toAppend = []
        # print("couples before cleaning : ", self.couples)
        for couple in self.couples:
            for couple_test in self.couples:
                if couple != couple_test:
                    if couple[1] == couple_test[0]:
                        if are_para(equation(couple[0], couple[1]), equation(couple_test[0], couple_test[1])):
                            toRemove.append(couple)
                            toRemove.append(couple_test)
                            if [couple_test[1], couple[0]] not in toAppend:
                                toAppend.append([couple[0], couple_test[1]])
                    elif couple[0] == couple_test[1]:
                        if are_para(equation(couple[1], couple[0]), equation(couple_test[1], couple_test[0])):
                            toRemove.append(couple)
                            toRemove.append(couple_test)
                            if [couple[1], couple_test[0]] not in toAppend:
                                toAppend.append([couple_test[0], couple[1]])
        
        self.couples = [couple for couple in self.couples if couple not in toRemove]
            
        self.couples += toAppend

    def remove(self, forme, sommet):
        eq_sil = self.find_equation_with(sommet)
        eq_form = find_equation_with(forme, sommet, forme.forme.new_scale)
        
        # print("sommet :", sommet)
        # print("silhouette : ", self.sommets)
        # print("couples b : ", self.couples)

        for eq in eq_sil:
            for eq_test in eq_form:
                if are_para(eq, eq_test):
                    if eq[-1] == eq_test[-1] and eq[-2] != eq_test[-2]:
                        self.couples.append([eq[-2], eq_test[-2]])
                    
                    elif eq[-2] == eq_test[-2] and eq[-1] != eq_test[-1]:
                        self.couples.append([eq_test[-1], eq[-1]])

        firstPoint = []
        secondPoint = []

        if len(forme.forme.sommets) == 3:
            for eq in eq_form:
                if sommet == eq[-1]:
                    firstPoint = eq[-2]
                else:
                    secondPoint = eq[-1]
            self.couples.append([firstPoint, secondPoint])
        else:
            for eq in forme.build_equations(forme.forme.new_scale):
                if sommet not in eq:
                    self.couples.append([eq[-1], eq[-2]])

        self.couples = [couple for couple in self.couples if sommet not in couple]
        
        self.clean_couples()
        self.clean_couples()
        
        listTmp = []
        
        for couple in self.couples:
            if couple not in listTmp and couple[1] != couple[0]:
                listTmp.append(couple)
        
        self.couples = listTmp
        
        self.sommets = []
        self.sommets = [couple[0] for couple in self.couples if couple[0] not in self.sommets]

        # print("couples a : ",self.couples)
        # print("sommets new silhouette : ", self.sommets)
        
    def build_equations(self):
        equations = []

        for couple in self.couples:
            equations.append(equation(couple[0], couple[1]))
            
        return equations
        
    def find_equation_with(self, sommet):
        equations = []
        for eq in self.build_equations():
            if sommet in eq:
                equations.append(eq)

        return equations
        
    def complete(self, form):
        # print("sommets forme : ", form.get_sommets(form.forme.new_scale))
        # print("sommets sil : ", self.sommets)
        test = deepcopy(self.sommets)
        for sommet in form.get_sommets(form.forme.new_scale):
            if sommet in self.sommets:
                test.remove(sommet)
        return test == []
    
def creation_couples(list_pts):
    list_cpl = []
    for i in range(len(list_pts)-1):
        list_cpl.append([list_pts[i], list_pts[i+1]])
    return list_cpl
    
def are_para(eq, eq_test):
    if len(eq) == len(eq_test):
        if len(eq) == 3:
            return True
        
        else:
            return eq[0] == eq_test[0]

    return False