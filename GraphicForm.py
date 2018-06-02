#!--*--coding:utf-8--*--

from form import Form
from form import equation
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
        self.formeRect.y = round(posY + (p[1] - self.forme.ptMoyen()[1]) * (size/self.forme.scale))
        self.formeRect.x = round(posX + (p[0] - self.forme.ptMoyen()[0]) * (size/self.forme.scale))
        self.initialPoint = [self.formeRect.x, self.formeRect.y]

        pyg.draw.polygon(self.formeSurface, (1,1,1), self.forme.get_sommets(size))
        pyg.draw.polygon(self.formeSurface, (255,255,255), self.forme.get_sommets(size),3)

    def move(self, ptInitial, ptFinal, width, height):

        offsetX = round(ptFinal[0] - ptInitial[0])
        offsetY = round(ptFinal[1] - ptInitial[1])

        offsetX, offsetY = self.offsetBorderCollision(offsetX, offsetY, width, height)
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

    def build_equations(self, size = 100):
        equations = []
        sommets = self.get_sommets(size)

        for i in range(len(sommets)-1):
            first_point = sommets[i]
            second_point = sommets[i+1]
            equations.append(equation(first_point, second_point))

        equations.append(equation(sommets[i+1], sommets[0]))

        return equations

    def ptMoyen(self, size = 100):
        x, y = 0, 0
        for sommet in self.get_sommets(size):
            x += sommet[0]
            y += sommet[1]

        l = len(self.forme.sommets)
        y /= l
        x /= l
        return[round(x), round(y)]

    def offsetBorderCollision(self, offsetX, offsetY, width, height):
        for sommet in self.get_sommets(self.forme.new_scale):
            newX = sommet[0] + offsetX
            newY = sommet[1] + offsetY
            if newX > width-1:
                offsetX = width - 1 - sommet[0]
            if newX < 1:
                offsetX = 1 - sommet[0]
            if newY > height-1:
                offsetY = height - 1 - sommet[1]
            if newY < 1:
                offsetY = 1 - sommet[1]
        return offsetX, offsetY

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

    def magnet(self, form, width, height):

        #Definition de la "distance" de magnet
        d = 20
        move = False

        for sommet1 in self.get_sommets(self.forme.new_scale):
            if move:
                break
            for sommet2 in form.get_sommets(form.forme.new_scale):
                    offsetX = sommet1[0] - sommet2[0]
                    offsetY = sommet1[1] - sommet2[1]

                    if abs(offsetX) <= d and abs(offsetY) <= 30:
                        self.move(sommet1, sommet2, width, height)
                        move = True
                        break