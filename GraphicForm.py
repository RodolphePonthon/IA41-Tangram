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
        self.formeRect.y = posY
        self.formeRect.x = posX

        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(self.formeSurface.get_height()),3)

    def move(self, ptInitial, ptFinal):

        offsetX = ptFinal[0] - ptInitial[0]
        offsetY = ptFinal[1] - ptInitial[1]
        self.formeRect.x += offsetX
        self.formeRect.y += offsetY

    def isOn(self, p, size = 100):
        return self.forme.isOn([(p[0]-self.formeRect.x),(p[1]-self.formeRect.y)], size)
