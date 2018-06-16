from form import equation as make_eq

def convert_to_draw(list_gForms):
    size = list_gForms[0].forme.new_scale
    points = []
    eqKeep = []
    eqTmp = []
    criticalPoints = []
    for i in range(len(list_gForms)):
        actualForm = list_gForms[i]
        for sommet in actualForm.get_sommets(size):
            equations = find_equation_with(actualForm, sommet, size)
            eqMerged  = 0
            eqAligned = 0
            belongs = 0

            for j in range(len(list_gForms)):
                if i != j:
                    formToTest = list_gForms[j]
                    equationsToTest = find_equation_with(formToTest, sommet, size)

                    for eq in equations:
                        for eqTest in equationsToTest:
                            if areMerged(eq, eqTest, sommet):
                                eqMerged += 1

                            elif areAligned(eq, eqTest):
                                eqAligned +=1

            if eqMerged == 2:
                if eqAligned >= 1:
                    if sommet not in criticalPoints:
                        criticalPoints.append(sommet)
                else:
                    pass
            elif eqMerged == 1:
                if eqAligned == 1:
                    pass
                else:
                    if sommet not in points:
                        points.append(sommet)
                    for eq in equations:
                        if eq not in eqKeep:
                            eqKeep.append(eq)
            else:
                if sommet not in points:
                    points.append(sommet)
                for eq in equations:
                        if eq not in eqKeep:
                            eqKeep.append(eq)

    points = sorted(points, key = lambda sommet: sommet[1])
    points = sorted(points, key = lambda sommet: sommet[0]) 

    criticalPoints = [point for point in criticalPoints if point not in points]

    # for point in points:
        # print(point)

    # print(len(points))

    # print("##########")

    for eq in eqKeep:
        p1, p2 = eq[-2], eq[-1]
        if p1 not in points or p2 not in points:
            eqTmp.append(eq)

    for eq in eqTmp:
        # print(eq)
        eqKeep.remove(eq)
        p1, p2 = eq[-2], eq[-1]
        for eqToTest in eqTmp:
            if eq != eqToTest:
                p3, p4 = eqToTest[-2], eqToTest[-1]
                if p1 not in points:
                    if p1 not in criticalPoints and p2 not in criticalPoints:
                        if p3 == p1 and areAligned(eq, eqToTest) and p2 != p4:
                            eqKeep.append(make_eq(p2, p4))
                        elif p4 == p1 and areAligned(eq, eqToTest) and p2 != p3:
                            eqKeep.append(make_eq(p2, p3))
                    if areHalfMerged(eq, eqToTest, p1):
                        if belongsTo(p3, eq):
                            if p3 in points and p2 != p3:
                                eqKeep.append(make_eq(p2, p3))
                        elif belongsTo(p4, eq):
                            if p4 in points and p2 != p4:
                                eqKeep.append(make_eq(p2, p4))
                elif p2 not in points:
                    if p1 not in criticalPoints and p2 not in criticalPoints:
                        if p3 == p2 and areAligned(eq, eqToTest) and p1 != p4:
                            eqKeep.append(make_eq(p1, p4))
                        elif p4 == p2 and areAligned(eq, eqToTest) and p1 != p3:
                            eqKeep.append(make_eq(p1, p3))
                    if areHalfMerged(eq, eqToTest, p2):
                        if belongsTo(p3, eq):
                            if p3 in points and p3 != p1:
                                eqKeep.append(make_eq(p1, p3))
                        elif belongsTo(p4, eq):
                            if p4 in points and p1 != p4:
                                eqKeep.append(make_eq(p1, p4))

    # print("##########")

    eqToRemove = []

    for eq in eqKeep:
        p1, p2 = eq[-2], eq[-1]
        for eq2 in eqKeep:
            p3, p4 = eq2[-2], eq2[-1]
            if eq != eq2:
                if areAligned(eq, eq2) and (p1 == p4 or p2 == p3):
                    if eq not in eqToRemove and eq2 not in eqToRemove:
                        eqToRemove.append(eq)
                        break

    eqKeep = [eq for eq in eqKeep if eq not in eqToRemove]

    # for eq in eqKeep:
        # print(eq)

    # print("#########")

    # for point in criticalPoints:
        # print(point)

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

def areAligned(eq1, eq2):
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
    
    return sameDirection and areAligned(eq1, eq2)

def areHalfMerged(eq1, eq2, point):
    halfMerged = False

    if areAligned(eq1, eq2):
        if belongsTo(point, eq1) and belongsTo(point, eq2):
            halfMerged = True
    
    return halfMerged

def belongsTo(point, eq):
    p1, p2 = eq[-2], eq[-1]
    belongsX = p1[0] <= point[0] <= p2[0] or p1[0] >= point[0] >= p2[0]
    belongsY = p1[1] <= point[1] <= p2[1] or p1[1] >= point[1] >= p2[1]

    return belongsY and belongsX