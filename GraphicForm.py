#!--*--coding:utf-8--*--

from form import Form
import pygame as pyg

class GraphicForm:
    def __init__(self, form, posX, posY, size):
        size = float(size)
        self.forme = form
        self.forme.new_scale = size
        #initialisation Surface
        self.formeSurface = pyg.Surface((size, size))
        self.formeSurface.fill((0,0,0))
        self.formeSurface.set_colorkey((0,0,0))
        #initialisation Rectangle
        self.formeRect = self.formeSurface.get_rect()
        p = self.forme.ptMoyen()
        self.initialize()
        self.formeRect.y = posY + (p[1] - self.forme.ptMoyen()[1]) * (size/self.forme.scale)
        self.formeRect.x = posX + (p[0] - self.forme.ptMoyen()[0]) * (size/self.forme.scale)
        self.initialPoint = [self.formeRect.x, self.formeRect.y]

        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(size))
        pyg.draw.polygon(self.formeSurface, (255,255,255), self.forme.get_sommets(size),3)

    def move(self, ptInitial, ptFinal):

        offsetX = ptFinal[0] - ptInitial[0]
        offsetY = ptFinal[1] - ptInitial[1]
        self.formeRect.x += offsetX
        self.formeRect.y += offsetY

    def get_sommets(self, size = 100):
        sommets = []
        rect = self.formeRect
        for sommet in self.forme.get_sommets(size):
            x = sommet[0] + rect.x
            y = sommet[1] + rect.y
            sommets.append([x, y])

        return sommets

    def initialize(self):
        self.forme.initialize()
        size = self.forme.new_scale
        p = self.forme.ptMoyen()
        for sommet in self.forme.sommets:
            sommet[0] += round(size/2/(size/self.forme.scale) - p[0],1)
            sommet[1] += round(size/2/(size/self.forme.scale)  - p[1],1)

    def update(self):
        self.formeSurface.fill((0,0,0))
        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(self.formeSurface.get_height()))
        pyg.draw.polygon(self.formeSurface, (255,255,255), self.forme.get_sommets(self.formeSurface.get_height()),3)

    def draw_only_fill(self):
        self.formeSurface.fill((0,0,0))
        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(self.formeSurface.get_height()))

    def isOn(self, p, size = 100):
        return self.forme.isOn([(p[0]-self.formeRect.x),(p[1]-self.formeRect.y)], size)

    def isCornerSelected(self, p, size = 100):
        return self.forme.isCornerSelected([(p[0]-self.formeRect.x),(p[1]-self.formeRect.y)], size)

    def isCutting(self, gForm, size = 100):
        isCutting = False
        for sommet in self.get_sommets(size):
            if gForm.isOn([sommet[0], sommet[1]], size):
                isCutting = True
                break

        return isCutting