#!--*--coding:utf-8--*--

from form import equation
from convert_to_draw import find_equation_with
from convert_to_draw import direction
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
            print("nb Pieces : ", len(list_forms) - len(moved_forms))
            if form not in moved_forms:
                if len(list_forms) - len(moved_forms) == 1:
                    return True
                else:
                    for i in range(len(form.get_sommets())):
                        if form not in moved_forms:
                            sommet = form.get_sommets(form.forme.new_scale)[i]
                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                            sommet_sil_removed = []
                            for sommet_sil in silhouette.sommets:
                                if sommet_sil not in sommet_sil_removed:
                                    #print("forme :", find_equation_with(form, sommet, form.forme.new_scale))
                                    if form not in moved_forms:
                                        list_eq_sil = silhouette.find_equation_with(sommet_sil)
                                        #print("rotation de :", rotation*180/pi, "entre :", list_eq_form[0], " et ", list_eq_sil[0])
                                        rotation = 0
                                        if find_rotation(list_eq_form[0], list_eq_sil[0]) == find_rotation(list_eq_form[1], list_eq_sil[1]):
                                            rotation = find_rotation(list_eq_form[0], list_eq_sil[0])
                                            form.forme.rotation(rotation)
                                            print("forme :", list_forms.index(form), "rotation :", rotation*180/pi)
                                            sommet = form.get_sommets(form.forme.new_scale)[i]
                                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                        elif find_rotation(list_eq_form[0], list_eq_sil[1]) == find_rotation(list_eq_form[1], list_eq_sil[0]):
                                            rotation = find_rotation(list_eq_form[0], list_eq_sil[1])
                                            form.forme.rotation(rotation)
                                            print("forme :", list_forms.index(form), "rotation :", rotation*180/pi)
                                            sommet = form.get_sommets(form.forme.new_scale)[i]
                                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                        if are_para(list_eq_form[0], list_eq_sil[0]) and are_para(list_eq_form[1], list_eq_sil[1]):
                                            if direction(list_eq_form[0], sommet) == direction(list_eq_sil[0], sommet_sil) and direction(list_eq_form[1], sommet) == direction(list_eq_sil[1], sommet_sil):
                                                if (size(list_eq_form[0]) <= size(list_eq_sil[0])) and (size(list_eq_form[1]) <= size(list_eq_sil[1])):
                                                    form.move(sommet, sommet_sil, self.width, self.height)
                                                    saved_sommet = deepcopy(sommet)
                                                    sommet = form.get_sommets(form.forme.new_scale)[i]
                                                    print("sommet : ", sommet)
                                                    print("forme :", list_forms.index(form), "move :", form.get_sommets(form.forme.new_scale))
                                                    print("silhouette : ", silhouette.sommets)
                                                    list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                                    saved_silhouette = deepcopy(silhouette)
                                                    silhouette.remove(form, sommet)
                                                    sommet_sil_removed.append(sommet)
                                                    moved_forms.append(form)


                                                print("continue without : ", [list_forms.index(form) for form in moved_forms])
                                                if self.solve(silhouette, list_forms, moved_forms):
                                                    return True
                                                else:
                                                    print("backtrack sur forme : ", list_forms.index(form))
                                                    silhouette = deepcopy(saved_silhouette)
                                                    moved_forms.remove(form)
                                                    form.move(sommet_sil, saved_sommet, self.width, self.height)
                                                    form.forme.rotation(-rotation)
                                            else:
                                                form.forme.rotation(-rotation)
                                        
                                        elif are_para(list_eq_form[1], list_eq_sil[0]) and are_para(list_eq_form[0], list_eq_sil[1]):
                                            if direction(list_eq_form[1], sommet) == direction(list_eq_sil[0], sommet_sil) and direction(list_eq_form[0], sommet) == direction(list_eq_sil[1], sommet_sil):
                                                if (size(list_eq_form[1]) <= size(list_eq_sil[0])) and (size(list_eq_form[0]) <= size(list_eq_sil[1])):
                                                    form.move(sommet, sommet_sil, self.width, self.height)
                                                    saved_sommet = deepcopy(sommet)
                                                    sommet = form.get_sommets(form.forme.new_scale)[i]
                                                    print("sommet : ", sommet)
                                                    print("forme :", list_forms.index(form), "move :", form.get_sommets(form.forme.new_scale))
                                                    print("silhouette : ", silhouette.sommets)
                                                    list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                                    saved_silhouette = deepcopy(silhouette)
                                                    silhouette.remove(form, sommet)
                                                    sommet_sil_removed.append(sommet)
                                                    moved_forms.append(form)

                                                    print("continue without : ", [list_forms.index(form) for form in moved_forms])
                                                    if self.solve(silhouette, list_forms, moved_forms):
                                                        return True
                                                    else:
                                                        print("backtrack sur forme : ", list_forms.index(form))
                                                        silhouette = deepcopy(saved_silhouette)
                                                        moved_forms.remove(form)
                                                        form.move(sommet_sil, saved_sommet, self.width, self.height)
                                                        form.forme.rotation(-rotation)
                                                else:
                                                    form.forme.rotation(-rotation)
                                            else:
                                                form.forme.rotation(-rotation)

                                        else:
                                            form.forme.rotation(-rotation)
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
    result = (scal/(sizeVF*sizeVS)) // 1
    angle = acos(result)
    
    return angle