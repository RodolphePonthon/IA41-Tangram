#!--*--coding:utf-8--*--

from form import equation as make_eq, equation_solve

def convert_to_draw(list_gForms):
    size = list_gForms[0].forme.new_scale
    points = []
    couples = []
    for i in range(len(list_gForms)):
        actualForm = list_gForms[i]
        for sommet in actualForm.get_sommets(size):
            first_eq = []
            last_eq = []
            for eq in find_equation_with(actualForm, sommet, actualForm.forme.new_scale):
                if eq[-1] == sommet:
                    first_eq = eq
                else:
                    last_eq = eq
            equations = [first_eq, last_eq]
            eqMerged  = 0
            eqAligned = 0
            notToAdd = []

            for j in range(len(list_gForms)):
                if i != j:
                    formToTest = list_gForms[j]
                    equationsToTest = find_equation_with(formToTest, sommet, formToTest.forme.new_scale)

                    for eq in equations:
                        for eqTest in equationsToTest:
                            if areMerged(eq, eqTest, sommet):
                                eqMerged += 1
                                notToAdd.append(eq)

                            elif areAligned(eq, eqTest):
                                eqAligned +=1
            if eqMerged == 2:
                pass
            elif eqMerged == 1:
                if eqAligned == 1:
                    pass
                else:
                    if sommet not in points:
                        points.append(sommet)
                    for eq in equations:
                        if eq not in notToAdd:
                            if [eq[-2], eq[-1]] not in couples:
                                couples.append([eq[-2], eq[-1]])
                                couples = clean_couples(couples)
            else:
                if sommet not in points:
                    points.append(sommet)
                for eq in equations:
                    if eq not in notToAdd:
                        couples.append([eq[-2], eq[-1]])
                        couples = clean_couples(couples)

    print(len(points))

    for point in points:
        print(point)

    for couple in couples:
        print(couple)

    return points

#return the equations of a form from a given sommet
def find_equation_with(form, sommet, size):
    equations = []
    for eq in form.build_equations(size):
        if sommet in eq:
            equations.append(eq)

    return equations

#return the direction of an equation from a given point on the equation
def direction(eq, point):
    direction = 0
    if len(eq) == 3:
        if eq[1] == point:
            direction = (eq[2][1] - point[1]) / abs(eq[2][1] - point[1])
        elif eq[2] == point:
            direction = (eq[1][1] - point[1]) / abs(eq[1][1] - point[1])
    else:
        if eq[2] == point:
            direction = (eq[3][0] - point[0]) / abs(eq[3][0] - point[0])
        elif eq[3] == point:
            direction = (eq[2][0] - point[0]) / abs(eq[2][0] - point[0])
    
    return direction

#Test if two equations are Aligned
def areAligned(eq1, eq2):
    if len(eq1) == len(eq2):
        if len(eq1) == 3:
            if eq1[0] == eq2[0]:
                return True
        if len(eq1) == 4:
            if eq1[0] == eq2[0] and eq1[1] == eq2[1]:
                return True

    return False

#Test if two equations are full merged
def areMerged(eq1, eq2, point):
    sameDirection = False
    direction1 = direction(eq1, point)
    direction2 = direction(eq2, point)

    if(direction1 == direction2):
        sameDirection = True
    
    return sameDirection and areAligned(eq1, eq2)

#Test if two equations are merged but not full merged
def areHalfMerged(eq1, eq2, point):
    halfMerged = False

    if areAligned(eq1, eq2):
        if belongsTo(point, eq1) and belongsTo(point, eq2):
            halfMerged = True
    
    return halfMerged

#Test if point belongs to the are of an equation
def belongsTo(point, eq):
    p1, p2 = eq[-2], eq[-1]
    belongsX = p1[0] <= point[0] <= p2[0] or p1[0] >= point[0] >= p2[0]
    belongsY = p1[1] <= point[1] <= p2[1] or p1[1] >= point[1] >= p2[1]

    return belongsY and belongsX
    
#Test if a given point is on a given equation
def isOnEq(point, eq):
    if len(eq) == 3:
        return belongsTo(point, eq)
    else:
        return equation_solve(eq, point[0]) == point[1] and belongsTo(point, eq)