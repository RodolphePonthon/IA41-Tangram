#!--*--coding:utf-8--*--

import pygame as pyg
from form import Form
from GraphicForm import GraphicForm
from math import pi
from os import environ
from zone import Zone
from convert_to_draw import convert_to_draw

environ['SDL_VIDEO_CENTERED'] = '1'

def draw(screen, gForm):
    gForm.update()
    screen.blit(gForm.formeSurface, gForm.formeRect)

def init_forms(size):
    triangle = Form([[0,0],[0,100],[50,50]])
    triangle2 = Form([[0,0],[50,50],[100,0]])
    triangle3 = Form([[75,25],[100,0],[100,50]])
    triangle4 = Form([[50,100],[100,50],[100,100]])
    triangle5 = Form([[25,75],[50,50],[75,75]])
    carre = Form([[50,50],[75,25],[100,50],[75,75]])
    para = Form([[0,100],[25,75],[75,75],[50,100]])

    list_forms = [triangle, triangle2, triangle3, triangle4, triangle5, carre, para]

    list_GraphicForm = []
    for form in list_forms:
        list_GraphicForm.append(GraphicForm(form, 10, int(size/4), int(size/2)))

    return list_GraphicForm

def gestion_event(evt):
    pass

def main():
    #Initialize screen
    pyg.init()
    width = 800
    height = 600
    fps = 30
    screen = pyg.display.set_mode((width, height))
    screen_rect = screen.get_rect()
    screen_rect.x = screen_rect.y = 0
    pyg.display.set_caption('IA41 - Tangram')
    screen.fill((200,200,200))
    clock = pyg.time.Clock()
    clock.tick(fps)

    #Initialize variables
    list_GraphicForm = init_forms(height)
    running = True
    move = False
    turn = False
    interval = 180
    pasInterval = 45
    ptInitial = [0,0]
    ptFinal = [0,0]
    ptTmp = [0,0]
    lastPtTmp = [0,0]
    actualForm = None
    zoneDessin = Zone((0, 0, 100), (width/2, 0), (width/2, height))
    zoneDepart = Zone((0, 133, 0), (10, height/4), (height/2, height/2))

    for gForm in list_GraphicForm:
            for gForm2 in list_GraphicForm:
                gForm.magnet(gForm2, width, height)

    finale = [[121, 541], [121, 241], [46, 166], [121, 91], [46, 16], [346, 16], [346, 166], [271, 241], [271, 391]] 

    while running:
        #Place zones
        #pyg.draw.polygon(zoneDessin.surface, (0,0,0), finale)
        screen.blit(zoneDessin.surface, zoneDessin.rect)
        screen.blit(zoneDepart.surface, zoneDepart.rect)

        #Draw Forms
        for gForm in list_GraphicForm:
            draw(screen, gForm)

        pyg.display.flip()

        for evt in pyg.event.get():
            if evt.type == pyg.QUIT:
                running = False

            elif evt.type == pyg.MOUSEBUTTONDOWN:
                if evt.type == pyg.MOUSEBUTTONDOWN:
                    for graphicForm in list_GraphicForm:
                        if graphicForm.isOn(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                            ptInitial = pyg.mouse.get_pos()
                            actualForm = graphicForm
                            lastPtTmp = ptInitial
                            #Put the actual form at the end of the list to be printed last
                            list_GraphicForm[len(list_GraphicForm) - 1], list_GraphicForm[list_GraphicForm.index(actualForm)] = list_GraphicForm[list_GraphicForm.index(actualForm)], list_GraphicForm[len(list_GraphicForm) - 1]
                            if graphicForm.isCornerSelected(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                                turn = True
                            else:
                                move = True

            elif pyg.mouse.get_pressed()[0] and move:
                ptTmp = pyg.mouse.get_pos()
                actualForm.move(lastPtTmp, ptTmp, width, height)
                for i in range(len(list_GraphicForm)-1):
                    formTmp = list_GraphicForm[i]
                    if zoneDessin.isOn(actualForm) or zoneDessin.isOn(formTmp):     
                        if actualForm.isCutting(formTmp, graphicForm.formeSurface.get_height()) or formTmp.isCutting(graphicForm, graphicForm.formeSurface.get_height()):
                            actualForm.move(ptTmp, lastPtTmp, width, height)
                            break
                    if zoneDessin.isOn(actualForm) and zoneDessin.isOn(actualForm):
                        if not (actualForm.isCutting(formTmp, graphicForm.formeSurface.get_height()) and formTmp.isCutting(graphicForm, graphicForm.formeSurface.get_height())):
                            actualForm.magnet(formTmp, width, height)
                screen.fill((200,200,200))
                lastPtTmp = ptTmp

            elif pyg.mouse.get_pressed()[0] and turn:
                ptTmp = pyg.mouse.get_pos()
                angle = (lastPtTmp[1] - ptTmp[1])
                if abs(angle) > pasInterval:
                    sens = angle/abs(angle)
                    for i in range(pasInterval):
                        actualForm.forme.rotation(pi*sens/interval)
                    screen.fill((200,200,200))
                    lastPtTmp = ptTmp

            elif evt.type == pyg.MOUSEBUTTONUP and move:
                ptFinal = pyg.mouse.get_pos()
                actualForm.move(lastPtTmp, ptFinal, width, height)
                for i in range(len(list_GraphicForm)-1):
                    formTmp = list_GraphicForm[i]
                    if zoneDessin.isOn(actualForm) or zoneDessin.isOn(formTmp):     
                        if actualForm.isCutting(formTmp, graphicForm.formeSurface.get_height()) or formTmp.isCutting(graphicForm, graphicForm.formeSurface.get_height()):
                            actualForm.move(ptFinal, lastPtTmp, width, height)
                            break
                    if zoneDessin.isOn(actualForm) and zoneDessin.isOn(actualForm):
                        if not (actualForm.isCutting(formTmp, graphicForm.formeSurface.get_height()) and formTmp.isCutting(graphicForm, graphicForm.formeSurface.get_height())):
                            actualForm.magnet(formTmp, width, height)
                if not zoneDessin.isOn(actualForm):
                    actualForm.move([actualForm.formeRect.x, actualForm.formeRect.y] , actualForm.initialPoint, width, height)
                    actualForm.initialize()
                screen.fill((200,200,200))
                actualForm = None
                move = False

            elif evt.type == pyg.MOUSEBUTTONUP and turn:
                ptTmp = pyg.mouse.get_pos()
                angle = (lastPtTmp[1] - ptTmp[1])
                if abs(angle) > pasInterval:
                    sens = angle/abs(angle)
                    for i in range(pasInterval):
                        actualForm.forme.rotation(pi*sens/interval)
                    screen.fill((200,200,200))
                actualForm = None
                turn = False

            elif evt.type == pyg.KEYDOWN:
                if evt.key == pyg.K_ESCAPE:
                    running = False
                if evt.key == pyg.K_SPACE:
                    finale = convert_to_draw(list_GraphicForm)

    pyg.quit()
    exit()

if __name__ == '__main__':
    main()

# On compte tous les sommets sauf si on trouve pour deux formes différentes
# deux mêmes équations, on ne prend pas le point