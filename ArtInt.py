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
            # print("sommets nouvelle forme : ", form.get_sommets(form.forme.new_scale))
            # print("nb Pieces : ", len(list_forms) - len(moved_forms))
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
                                    if find_rotation(list_eq_form[0], list_eq_sil[0]) == find_rotation(list_eq_form[1], list_eq_sil[1]):
                                        if (size(list_eq_form[0]) <= size(list_eq_sil[0])) and (size(list_eq_form[1]) <= size(list_eq_sil[1])):
                                            rotation = find_rotation(list_eq_form[0], list_eq_sil[0])
                                            rotation = -rotation
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
                            sommet_sil_removed = []
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
                                if sommet_sil not in sommet_sil_removed and is_possible_sommet(list_eq_sil, sommet_sil):
                                    # print("forme :", list_eq_form)
                                    if form not in moved_forms:
                                        # print("rotation de :", rotation*180/pi, "entre :", list_eq_form[0], " et ", list_eq_sil[0])
                                        rotation = 0
                                        if abs(find_rotation(list_eq_form[0], list_eq_form[1])) == abs(find_rotation(list_eq_sil[0], list_eq_sil[1])):
                                            if find_rotation(list_eq_form[0], list_eq_sil[0]) == find_rotation(list_eq_form[1], list_eq_sil[1]):
                                                rotation = find_rotation(list_eq_form[0], list_eq_sil[0])
                                                form.forme.rotation(rotation)
                                                # print(list_eq_form[0], " et ", list_eq_sil[0], " egal a ", list_eq_form[1], " et ", list_eq_sil[1])
                                                # print("forme :", list_forms.index(form), "rotation :", rotation*180/pi)
                                                sommet = form.get_sommets(form.forme.new_scale)[i]
                                                first_eq = []
                                                last_eq = []
                                                for eq in find_equation_with(form, sommet, form.forme.new_scale):
                                                    if eq[-1] == sommet:
                                                        first_eq = eq
                                                    else:
                                                        last_eq = eq
                                                list_eq_form = [first_eq, last_eq]
                                                # print("Nouveaux sommets apres rotation : ", list_eq_form)
                                        if are_para(list_eq_form[0], list_eq_sil[0]) and are_para(list_eq_form[1], list_eq_sil[1]):
                                            if direction(list_eq_form[0], sommet) == direction(list_eq_sil[0], sommet_sil) and direction(list_eq_form[1], sommet) == direction(list_eq_sil[1], sommet_sil):
                                                if valid_size(list_eq_form, list_eq_sil, silhouette):
                                                    # print("sommet sil : ",sommet_sil)
                                                    # print("sommet : ", sommet)
                                                    # print("form.get_sommets(form.forme.new_scale)[",i,"] : ", form.get_sommets(form.forme.new_scale)[i])
                                                    form.move(sommet, sommet_sil, self.width, self.height)
                                                    if authorized_move(form, moved_forms, silhouette, form.get_sommets(form.forme.new_scale)[i], list_eq_form, sommet_sil):
                                                        saved_sommet = deepcopy(sommet)
                                                        sommet = form.get_sommets(form.forme.new_scale)[i]
                                                        #print("sommet : ", sommet)
                                                        # print("forme :", list_forms.index(form), "move :", form.get_sommets(form.forme.new_scale))
                                                        # print("silhouette : ", silhouette.sommets)
                                                        list_eq_form = find_equation_with(form, sommet, form.forme.new_scale)
                                                        saved_silhouette = deepcopy(silhouette)
                                                        saved_silhouette.remove(form, sommet)
                                                        # print("new coords silhouette : ", silhouette.sommets)
                                                        sommet_sil_removed.append(sommet)
                                                        moved_forms.append(form)

                                                        # print("continue without : ", [list_forms.index(form) for form in moved_forms])
                                                        # if list_forms.index(form) == 5:
                                                            # exit()
                                                        if self.solve(saved_silhouette, list_forms, moved_forms):
                                                            print("forme :", list_forms.index(form), "move :", form.get_sommets(form.forme.new_scale))
                                                            print("rotation de :", rotation*180/pi)
                                                            print("couples silhouette : ", silhouette.couples)
                                                            # print("saved sil : ", saved_silhouette.couples)
                                                            return True
                                                        else:
                                                            print("backtrack sur forme : ", list_forms.index(form))
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
                                                        # print("PAS AUTORISE")
                                                        form.move(sommet_sil, sommet, self.width, self.height)
                                                        form.forme.rotation(-rotation)
                                                else:
                                                    # print("PAS MEME TAILLE")
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
                                                # print("PAS MEME DIRECTION")
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
                                            # print("ON EST PAS PARALLELE")
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
        return False
                        
def size(eq):
    pt1, pt2 = eq[-2], eq[-1]
    return sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)
    
def is_possible_sommet(list_eq_sil, sommet):
    # print("equations silhouette envoyees dans la verif de validite : ",list_eq_sil)
    # print("sommet associé : ", sommet)
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
    
def authorized_move(form, list_form, silhouette, sommet, list_eq_form, sommet_sil):
    if sommet != sommet_sil:
        return False
        
    size = form.forme.new_scale
    for form_test in list_form:
        if form.isCutting(form_test, size) or form_test.isCutting(form, size):
            return False
    
    if len(form.get_sommets(size)) == 4:
        pt1, pt2 = list_eq_form[0][-2], list_eq_form[1][-1]
        if pt1 in silhouette.sommets and not is_possible_sommet(silhouette.find_equation_with(pt1), pt1):
            return False
        if pt2 in silhouette.sommets and not is_possible_sommet(silhouette.find_equation_with(pt2), pt2):
            return False
            
    return True
    
def valid_size(list_eq_form, list_eq_sil, silhouette):
    if size(list_eq_form[0]) <= size(list_eq_sil[0]) and size(list_eq_form[1]) <= size(list_eq_sil[1]):
        return True
    elif size(list_eq_form[0]) > size(list_eq_sil[0]) and size(list_eq_form[1]) <= size(list_eq_sil[1]):
        return not is_possible_sommet(silhouette.find_equation_with(list_eq_sil[0][-2]), list_eq_sil[0][-2])
    elif size(list_eq_form[0]) <= size(list_eq_sil[0]) and size(list_eq_form[1]) > size(list_eq_sil[1]):
        return not is_possible_sommet(silhouette.find_equation_with(list_eq_sil[1][-2]), list_eq_sil[1][-2])