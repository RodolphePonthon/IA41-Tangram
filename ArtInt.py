#!--*--coding:utf-8--*--

from form import equation

class Ia :
    def __init__(self, silhouette, list_form):
        self.silhouette = silhouette
        self.list_form = list_form
        self.solve(self.list_form, 0)
    
    
    def find_equation_para(eq_forme, list_eq_silhouette):
        list_f = []
        if len(eq_forme) == 3:
            for eq_silh in list_eq_silhouette:
                if len(eq_silh) == 3:
                    list_f.append(eq_silh)
                    
        else:
            for eq_silh in list_eq_silhouette:
                if eq_silh[0] == eq_forme[0]:
                    list_f.append(eq_silh)
                    
        return list_f
    
    
    def solve(self, list_form, i, deg = 0):
        if i == len(list_form)-1:
            