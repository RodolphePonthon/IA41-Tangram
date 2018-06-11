#!--*--coding:utf-8--*--

class silhouette:
    def __init__(self, list_pts_form):
        self.couples = creation_couples(list_pts_form)
        
def creation_couples(list_pts):
    list_cpl = []
    for i in range(len(list_pts)-1):
        list_cpl.append([list_pts[i], list_pts[i+1]])
    return list_cpl