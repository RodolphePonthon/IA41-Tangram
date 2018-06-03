def convert_to_draw(list_gForms):
    size = list_gForms[0].forme.new_scale
    points = []
    for i in range(len(list_gForms)):
        actualForm = list_gForms[i]
        for sommet in actualForm.get_sommets(size):
            if sommet not in points:
                equations = find_equation_with(actualForm, sommet, size)
                eqMerged  = 0
                eqAligned = 0

                for j in range(len(list_gForms)):
                    if i != j:
                        formToTest = list_gForms[j]
                        equationsToTest = find_equation_with(formToTest, sommet, size)

                        for eq in equations:
                            for eqTest in equationsToTest:
                                if areMerged(eq, eqTest, sommet):
                                    eqMerged += 1

                                elif areAligned(eq, eqTest, sommet):
                                    eqAligned +=1
                if eqMerged == 2:
                    pass
                elif eqMerged == 1:
                    if eqAligned == 1:
                        pass
                    else:
                        points.append(sommet)
                else:
                    points.append(sommet)

    points = sorted(points, key = lambda sommet: sommet[1])
    points = sorted(points, key = lambda sommet: sommet[0])  

    for point in points:
        print(point)

    print(len(points))

    return points

def find_equation_with(form, sommet, size):
    equations = []
    for eq in form.build_equations(size):
        if sommet in eq:
            equations.append(eq)

    return equations

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

def areAligned(eq1, eq2, point):
    if len(eq1) == len(eq2):
        if len(eq1) == 3:
            if eq1[0] == eq2[0]:
                return True
        if len(eq1) == 4:
            if eq1[0] == eq2[0] and eq1[1] == eq2[1]:
                return True

    return False

def areMerged(eq1, eq2, point):
    sameDirection = False
    direction1 = direction(eq1, point)
    direction2 = direction(eq2, point)

    if(direction1 == direction2):
        sameDirection = True
    
    return sameDirection and areAligned(eq1, eq2, point)