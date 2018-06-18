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
        memories = [[], [], [], [], [], [], []]
        priority = "fullSize"
        for i in range(3):
            for form in list_forms:
                if form not in moved_forms:
                    if len(list_forms) - len(moved_forms) == 1:
                        if len(silhouette.sommets) == len(form.get_sommets()):
                            sommet = form.get_sommets(form.forme.new_scale)[0]
                            first_eq = []
                            last_eq = []
                            for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                if eq[-1] == sommet:
                                    first_eq = eq
                                else:
                                    last_eq = eq
                            list_eq_form = [first_eq, last_eq]
                            for sommet_sil in silhouette.sommets:
                                first_eq = []
                                last_eq = []
                                for eq in silhouette.find_equation_with(sommet_sil):
                                    if eq[-1] == sommet_sil:
                                        first_eq = eq
                                    else:
                                        last_eq = eq
                                list_eq_sil = [first_eq, last_eq]
                                if is_possible_sommet(list_eq_sil, sommet_sil):
                                    if find_rotation(list_eq_form[0], list_eq_form[1]) == find_rotation(list_eq_sil[0], list_eq_sil[1]):
                                        if (size(list_eq_form[0]) == size(list_eq_sil[0])) and (size(list_eq_form[1]) == size(list_eq_sil[1])):
                                            rotation = find_rotation(list_eq_form[0], list_eq_sil[0])
                                            form.forme.rotation(rotation)
                                            sommet = form.get_sommets(form.forme.new_scale)[0]
                                            list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                            form.move(sommet, sommet_sil, self.width, self.height)
                                            
                                            if silhouette.complete(form):
                                                return True
                                            else:
                                                form.move(sommet_sil, sommet, self.width, self.height)
                                                form.forme.rotation(-rotation)
                            return False
                        else:
                            return False
                    else:
                        for i in range(len(form.get_sommets())):
                            if form not in moved_forms:
                                sommet = form.get_sommets(form.forme.new_scale)[i]
                                first_eq = []
                                last_eq = []
                                for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                    if eq[-1] == sommet:
                                        first_eq = eq
                                    else:
                                        last_eq = eq
                                list_eq_form = [first_eq, last_eq]
                                for sommet_sil in silhouette.sommets:
                                    if len(silhouette.find_equation_with(sommet_sil)) > 2:
                                        continue
                                    first_eq = []
                                    last_eq = []
                                    for eq in silhouette.find_equation_with(sommet_sil):
                                        if eq[-1] == sommet_sil:
                                            first_eq = eq
                                        else:
                                            last_eq = eq
                                    list_eq_sil = [first_eq, last_eq]
                                    if is_possible_sommet(list_eq_sil, sommet_sil):
                                        if form not in moved_forms:
                                            rotation = 0
                                            if find_rotation(list_eq_form[0], list_eq_form[1]) == find_rotation(list_eq_sil[0], list_eq_sil[1]):
                                                rotation = find_rotation(list_eq_form[0], list_eq_sil[0])
                                                form.forme.rotation(rotation)
                                                sommet = form.get_sommets(form.forme.new_scale)[i]
                                                first_eq = []
                                                last_eq = []
                                                for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                                    if eq[-1] == sommet:
                                                        first_eq = eq
                                                    else:
                                                        last_eq = eq
                                                list_eq_form = [first_eq, last_eq]
                                                if valid_size(list_eq_form, list_eq_sil, silhouette, priority):
                                                    form.move(sommet, sommet_sil, self.width, self.height)
                                                    if authorized_move(form, moved_forms, silhouette, form.get_sommets(form.forme.new_scale)[i], list_eq_form, sommet_sil, memories[list_forms.index(form)]):
                                                        saved_sommet = deepcopy(sommet)
                                                        sommet = form.get_sommets(form.forme.new_scale)[i]
                                                        list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                                        saved_silhouette = deepcopy(silhouette)
                                                        saved_silhouette.remove(form, sommet)
                                                        moved_forms.append(form)

                                                        memories[list_forms.index(form)].append(form.get_sommets(form.forme.new_scale))
                                                        if self.solve(saved_silhouette, list_forms, moved_forms):
                                                            return True
                                                        else:
                                                            moved_forms.remove(form)
                                                            form.move(sommet_sil, saved_sommet, self.width, self.height)
                                                            form.forme.rotation(-rotation)
                                                            sommet = form.get_sommets(form.forme.new_scale)[i]
                                                            first_eq = []
                                                            last_eq = []
                                                            for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                                                if eq[-1] == sommet:
                                                                    first_eq = eq
                                                                else:
                                                                    last_eq = eq
                                                            list_eq_form = [first_eq, last_eq]
                                                    else:
                                                        form.move(sommet_sil, sommet, self.width, self.height)
                                                        form.forme.rotation(-rotation)
                                                else:
                                                    form.forme.rotation(-rotation)
                                                    sommet = form.get_sommets(form.forme.new_scale)[i]
                                                    first_eq = []
                                                    last_eq = []
                                                    for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                                        if eq[-1] == sommet:
                                                            first_eq = eq
                                                        else:
                                                            last_eq = eq
                                                    list_eq_form = [first_eq, last_eq]
                                            else:
                                                form.forme.rotation(-rotation)
                                                sommet = form.get_sommets(form.forme.new_scale)[i]
                                                first_eq = []
                                                last_eq = []
                                                for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                                    if eq[-1] == sommet:
                                                        first_eq = eq
                                                    else:
                                                        last_eq = eq
                                                list_eq_form = [first_eq, last_eq]
            if priority == "fullSize":
                priority = "halfSize"
            elif priority == "halfSize":
                priority = "all"
        return False
                        
def size(eq):
    pt1, pt2 = eq[-2], eq[-1]
    return sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)
    
def is_possible_sommet(list_eq_sil, sommet):
    first_eq = []
    last_pt = []
    for eq in list_eq_sil:
        if eq[-1] == sommet:
            first_eq = eq
        else:
            last_pt = eq[-1]
    
    vect_origine = [first_eq[-1][0] - first_eq[-2][0], first_eq[-1][1] - first_eq[-2][1]]
    vect_test = [last_pt[0] - first_eq[-2][0], last_pt[1] - first_eq[-2][1]]
    
    det = vect_origine[0] * vect_test[1] - vect_origine[1] * vect_test[0]
    
    return det > 0
    
def find_rotation(eq_forme, eq_sil):
    p1, p2 = eq_forme[-2], eq_forme[-1]
    p3, p4 = eq_sil[-2], eq_sil[-1]
    vectF = [p2[0] - p1[0], p2[1] - p1[1]]
    vectS = [p4[0] - p3[0], p4[1] - p3[1]]
    sizeVF = sqrt(vectF[0]**2 + vectF[1]**2)
    sizeVS = sqrt(vectS[0]**2 + vectS[1]**2)
    scal = vectF[0]*vectS[0] + vectF[1]*vectS[1]
    result = (scal/(sizeVF*sizeVS))
    if result > 1:
        result = 1
    elif result < -1:
        result = -1
    angle = acos(result)
    angle = round(angle*180/pi) #On ne peut faire que des rotations d'un degré minimum donc on transfert en deg, on le round, et on le retransfere en rads
    
    det = vectF[0] * vectS[1] - vectF[1] * vectS[0]
    
    if det < 0:
        angle = -angle
    
    return angle*pi/180
    
def authorized_move(form, list_form, silhouette, sommet, list_eq_form, sommet_sil, memories_form):
    if sommet != sommet_sil:
        return False
    
    size = form.forme.new_scale
    sommets = set(tuple(s) for s in form.get_sommets(size))
    
    for memory in memories_form:
        if set(tuple(s) for s in memory) - sommets:
            return False
    
    if len(form.get_sommets(size)) == 4:
        pt1, pt2 = list_eq_form[0][-2], list_eq_form[1][-1]
        if pt1 in silhouette.sommets and not is_possible_sommet(silhouette.find_equation_with(pt1), pt1):
            return False
        if pt2 in silhouette.sommets and not is_possible_sommet(silhouette.find_equation_with(pt2), pt2):
            return False
    
    return True
    
def valid_size(list_eq_form, list_eq_sil, silhouette, priority):
    
    if priority == "fullSize":
        if size(list_eq_form[0]) == size(list_eq_sil[0]) and size(list_eq_form[1]) == size(list_eq_sil[1]):
            return True
            
    elif priority == "halfSize":
        if size(list_eq_form[0]) == size(list_eq_sil[0]) and size(list_eq_form[1]) <= size(list_eq_sil[1]):
            return True
        elif size(list_eq_form[0]) <= size(list_eq_sil[0]) and size(list_eq_form[1]) == size(list_eq_sil[1]):
            return True
        elif size(list_eq_form[0]) > size(list_eq_sil[0]) and size(list_eq_form[1]) == size(list_eq_sil[1]):
            return not is_possible_sommet(silhouette.find_equation_with(list_eq_sil[0][-2]), list_eq_sil[0][-2])
        elif size(list_eq_form[0]) == size(list_eq_sil[0]) and size(list_eq_form[1]) > size(list_eq_sil[1]):
            return not is_possible_sommet(silhouette.find_equation_with(list_eq_sil[1][-2]), list_eq_sil[1][-2])
            
    else:
        if size(list_eq_form[0]) <= size(list_eq_sil[0]) and size(list_eq_form[1]) <= size(list_eq_sil[1]):
            return True
        elif size(list_eq_form[0]) > size(list_eq_sil[0]) and size(list_eq_form[1]) <= size(list_eq_sil[1]):
            return not is_possible_sommet(silhouette.find_equation_with(list_eq_sil[0][-2]), list_eq_sil[0][-2])
        elif size(list_eq_form[0]) <= size(list_eq_sil[0]) and size(list_eq_form[1]) > size(list_eq_sil[1]):
            return not is_possible_sommet(silhouette.find_equation_with(list_eq_sil[1][-2]), list_eq_sil[1][-2])