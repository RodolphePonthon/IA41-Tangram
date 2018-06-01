from form import Form
import pygame as pyg

class GraphicForm:
    def __init__(self, form, posX, posY):
        self.forme = form
        #initialisation Surface
        self.formeSurface = pyg.Surface((300, 300))
        self.formeSurface.fill((0,0,0))
        self.formeSurface.set_colorkey((0,0,0))
        #initialisation Rectangle
        self.formeRect = self.formeSurface.get_rect()
        p = self.forme.ptMoyen()
        for sommet in self.forme.sommets:
            sommet[0] += round(self.formeSurface.get_width()/2/(self.formeSurface.get_width()/self.forme.scale) - p[0], 3)
            sommet[1] += round(self.formeSurface.get_height()/2/(self.formeSurface.get_height()/self.forme.scale)  - p[1], 3)
        self.formeRect.y = posY + (p[1] - self.forme.ptMoyen()[1]) * (self.formeSurface.get_width()/self.forme.scale)
        self.formeRect.x = posX + (p[0] - self.forme.ptMoyen()[0]) * (self.formeSurface.get_width()/self.forme.scale)

        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(self.formeSurface.get_height()))
        pyg.draw.polygon(self.formeSurface, (255,255,255), self.forme.get_sommets(self.formeSurface.get_height()),3)

    def move(self, ptInitial, ptFinal):

        offsetX = ptFinal[0] - ptInitial[0]
        offsetY = ptFinal[1] - ptInitial[1]
        self.formeRect.x += offsetX
        self.formeRect.y += offsetY

    def update(self):
        self.formeSurface.fill((0,0,0))
        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(self.formeSurface.get_height()))
        pyg.draw.polygon(self.formeSurface, (255,255,255), self.forme.get_sommets(self.formeSurface.get_height()),3)


    def isOn(self, p, size = 100):
        return self.forme.isOn([(p[0]-self.formeRect.x),(p[1]-self.formeRect.y)], size)

    def isCornerSelected(self, p, size = 100):
        return self.forme.isCornerSelected([(p[0]-self.formeRect.x),(p[1]-self.formeRect.y)], size)