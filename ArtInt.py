#!--*--coding:utf-8--*--

from form import equation
from convert_to_draw import find_equation_with
from math import acos, sqrt, pi
from Silhouette import silhouette, are_para
from copy import deepcopy

class Ia :
    def __init__(self, silhouette, list_form, width, height):
        self.width = width
        self.height = height
        self.silhouette = silhouette
        self.list_form = list_form
        self.solve(silhouette, list_form, [])
    
    def solve(self, silhouette, list_forms, moved_forms):
        for form in list_forms:
            print("sommets nouvelle forme : ", form.get_sommets(form.forme.new_scale))
            if form not in moved_forms:
                if len(list_forms) - len(moved_forms) == 1:
                    return True
                else:
                    for i in range(len(form.get_sommets())):
                        if form not in moved_forms:
                            sommet = form.get_sommets(form.forme.new_scale)[i]
                            print(find_equation_with(form, sommet, form.forme.new_scale))
                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                            for sommet_sil in silhouette.sommets:
                                print("forme :", find_equation_with(form, sommet, form.forme.new_scale))
                                print("silhouette :", silhouette.find_equation_with(sommet_sil))
                                if form not in moved_forms:
                                    list_eq_sil = silhouette.find_equation_with(sommet_sil)
                                    rotation = find_rotation(list_eq_form[0], list_eq_sil[0])
                                    print("rotation de :", rotation*180/pi, "entre :", list_eq_form[0], " et ", list_eq_sil[0])
                                    if rotation == find_rotation(list_eq_form[1], list_eq_sil[1]):
                                        form.forme.rotation(rotation)
                                        sommet = form.get_sommets(form.forme.new_scale)[i]
                                        list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                    elif find_rotation(list_eq_form[0], list_eq_sil[1]) == find_rotation(list_eq_form[1], list_eq_sil[0]):
                                        form.forme.rotation(find_rotation(list_eq_form[0], list_eq_sil[1]))
                                        sommet = form.get_sommets(form.forme.new_scale)[i]
                                        list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                    if are_para(list_eq_form[0], list_eq_sil[0]) and are_para(list_eq_form[1], list_eq_sil[1]):
                                        if (size(list_eq_form[0]) <= size(list_eq_sil[0])) and (size(list_eq_form[1]) <= size(list_eq_sil[1])):
                                            form.move(sommet, sommet_sil, self.width, self.height)
                                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                            saved_silhouette = deepcopy(silhouette)
                                            silhouette.remove(form, sommet_sil)
                                            moved_forms.append(form)

                                            if self.solve(silhouette, list_forms, moved_forms):
                                                return True
                                            else:
                                                silhouette = deepcopy(saved_silhouette)
                                                moved_forms.remove(form)
                                    
                                    elif are_para(list_eq_form[1], list_eq_sil[0]) and are_para(list_eq_form[0], list_eq_sil[1]):
                                        if (size(list_eq_form[1]) <= size(list_eq_sil[0])) and (size(list_eq_form[0]) <= size(list_eq_sil[1])):
                                            form.move(sommet, sommet_sil, self.width, self.height)
                                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                            saved_silhouette = deepcopy(silhouette)
                                            silhouette.remove(form, sommet)
                                            moved_forms.append(form)
                                            if self.solve(silhouette, list_forms, moved_forms):
                                                return True
                                            else:
                                                silhouette = deepcopy(saved_silhouette)
                                                moved_forms.remove(form)
        return False
                        
def size(eq):
    pt1, pt2 = eq[-2], eq[-1]
    return sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)
    
def find_rotation(eq_forme, eq_sil):
    p1, p2 = eq_forme[-2], eq_forme[-1]
    p3, p4 = eq_sil[-2], eq_sil[-1]
    vectF = [p1[0] - p2[0], p1[1] - p2[1]]
    vectS = [p3[0] - p4[0], p3[1] - p4[1]]
    sizeVF = sqrt(vectF[0]**2 + vectF[1]**2)
    sizeVS = sqrt(vectS[0]**2 + vectS[1]**2)
    scal = vectF[0]*vectS[0] + vectF[1]*vectS[1]
    angle = acos(scal/(sizeVF*sizeVS))
    
    return angle