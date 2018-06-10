#!--*--coding:utf-8--*--

from copy import copy
import pygame as pyg
from form import Form
from Button import Button
from GraphicForm import GraphicForm
from math import pi
from os import environ
from zone import Zone
from convert_to_draw import convert_to_draw

environ['SDL_VIDEO_CENTERED'] = '1'

def draw(screen, gForm, withBorder = True):
    gForm.update(withBorder)
    screen.blit(gForm.formeSurface, gForm.formeRect)

def init_forms(width, height):
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
        list_GraphicForm.append(GraphicForm(form, width/4 - height/4, int(height/4), int(height/2)))

    return list_GraphicForm

def gestion_event(evt):
    pass

def main():
    #Initialize screen
    pyg.init()
    width = 1000
    height = 600
    fps = 30
    withBorder = True
    screen = pyg.display.set_mode((width, height))
    screen_rect = screen.get_rect()
    screen_rect.x = screen_rect.y = 0
    pyg.display.set_caption('IA41 - Tangram')
    screen.fill((200,200,200))
    clock = pyg.time.Clock()
    clock.tick(fps)

    #Initialize variables
    list_GraphicForm = init_forms(width, height)
    running = True
    phase = 1
    move = False
    turn = False
    interval = 180
    pasInterval = 45
    ptInitial = [0,0]
    ptFinal = [0,0]
    ptTmp = [0,0]
    lastPtTmp = [0,0]
    list_ptsForme = []
    actualForm = None
    zoneDessin = Zone((width/2, 0), (width/2, height), "Textures/ZoneDessin.png")
    zoneDepart = Zone((width/4 - height/4, height/4), (height/2, height/2), "Textures/ZoneDepart.png")
    titreBg = Zone((0, 0), (width/2, height), "Textures/menuBg.png", False)
    zoneTransition = Zone((0, 0), (width/2, height), "Textures/ZoneDessin.png")
    msgSelect = Zone((0, 3*height/4), (width/2, 20*height/600), "Textures/messageSelection.png")
    buttonLock = Button((width/4-width/8, height-height/6), (width/4, height/8), "Textures/buttonLock.png")
    buttonCheck = Button((width/2-height*50/600, height-height*50/600), (height*50/600, height*50/600), "Textures/buttonCheck.png")

    for gForm in list_GraphicForm:
            for gForm2 in list_GraphicForm:
                gForm.magnet(gForm2, width, height)

    finale = []
    formToFind = [[121, 541], [121, 241], [46, 166], [121, 91], [46, 16], [346, 16], [346, 166], [271, 241], [271, 391]]

    while running:
        if phase == 1:
            #Place zones
            for form in finale:
                pyg.draw.polygon(zoneDessin.surface, (0,0,0), form)
            screen.blit(titreBg.surface, titreBg.rect)
            screen.blit(zoneDessin.surface, zoneDessin.rect)
            screen.blit(zoneDepart.surface, zoneDepart.rect)

            #Draw Forms
            for gForm in list_GraphicForm:
                if zoneDessin.isOn(gForm):
                    draw(screen, gForm, withBorder)
                else:
                    draw(screen, gForm)
            
            #Place Button
            screen.blit(buttonLock.surface, buttonLock.rect)
            
            pyg.display.flip()

            if zoneDessin.rect.collidepoint(pyg.mouse.get_pos()):
                withBorder = True
            else:
                withBorder = False

            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    running = False

                elif evt.type == pyg.MOUSEBUTTONDOWN:
                    for graphicForm in list_GraphicForm:
                        if graphicForm.isOn(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                            ptInitial = pyg.mouse.get_pos()
                            actualForm = graphicForm
                            lastPtTmp = ptInitial
                            #Put the actual form at the end of the list to be printed last
                            list_GraphicForm[- 1], list_GraphicForm[list_GraphicForm.index(actualForm)] = list_GraphicForm[list_GraphicForm.index(actualForm)], list_GraphicForm[- 1]
                            if graphicForm.isCornerSelected(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                                turn = True
                            else:
                                move = True
                    #testing if we are on a button
                    zoneDepartVide = 1
                    if buttonLock.isOn(pyg.mouse.get_pos()):
                        for Gforme in list_GraphicForm:
                            if zoneDepart.isOn(Gforme):
                                zoneDepartVide = 0
                                print("Zone de depart n est pas vide !")
                        if zoneDepartVide:
                            phase = 2

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
                        formToFind = convert_to_draw(list_GraphicForm)
                        finale = []
                        for form in list_GraphicForm:
                            s = []
                            for sommet in form.get_sommets(form.formeSurface.get_height()):
                                s.append([sommet[0] - zoneDessin.rect.x, sommet[1]])
                            finale.append(s)
                            form.initialize()
        elif phase == 2:
            #Place zones
            for form in finale:
                pyg.draw.polygon(zoneDessin.surface, (0,0,0), form)
            screen.blit(zoneTransition.surface, zoneTransition.rect)
            screen.blit(zoneDessin.surface, zoneDessin.rect)

            #Draw Forms
            for gForm in list_GraphicForm:
                if zoneDessin.isOn(gForm):
                    draw(screen, gForm, withBorder)
                else:
                    draw(screen, gForm)
              
            if len(list_ptsForme) > 1:
                pyg.draw.lines(zoneTransition.surface, (200,200,200), False, list_ptsForme, 5)
                
            screen.blit(msgSelect.surface, msgSelect.rect)
            screen.blit(buttonCheck.surface, buttonCheck.rect)
            
            pyg.display.flip()

            if zoneDessin.rect.collidepoint(pyg.mouse.get_pos()):
                withBorder = True
            else:
                withBorder = False

            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    running = False
                    
                elif evt.type == pyg.MOUSEBUTTONDOWN:
                    for graphicForm in list_GraphicForm:
                        if graphicForm.isOn(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                            newSommet = graphicForm.getCornerSelected(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height())
                            if  newSommet != []:
                                newSommet[0] -= width/2
                                list_ptsForme.append(newSommet)
                                
                    if buttonCheck.isOn(pyg.mouse.get_pos()):
                        if list_ptsForme != []:
                            list_ptsFormeTmp = [list_ptsForme[0]]
                            for i in range(1, len(list_ptsForme)):
                                if (list_ptsForme[i][0] != list_ptsForme[i-1][0]) or (list_ptsForme[i][1] != list_ptsForme[i-1][1]):
                                    list_ptsFormeTmp.append(list_ptsForme[i])
                            list_ptsForme = list_ptsFormeTmp
                            if len(list_ptsForme) > 2 and list_ptsForme[0] == list_ptsForme[-1]:
                                list_ptsFinalForme =copy(list_ptsForme)
                                del list_ptsFinalForme[-1]
                                final_Gform = GraphicForm(Form(list_ptsFinalForme), width/4 - height/4, int(height/4), int(height/2))
                                screen.fill((200,200,200))
                                phase = 3
                            else:
                                print("Forme non conforme : vérifiez que le début est bien relié à la fin ou que la forme comporte au moins 3 sommets.")
                        else:
                            print("Liste de points vide !")
                            
        elif phase ==3:
            #Place zones
            screen.blit(zoneTransition.surface, zoneTransition.rect)
            screen.blit(zoneDessin.surface, zoneDessin.rect)
            
            #Draw forms
            pyg.draw.lines(zoneTransition.surface, (200,200,200), False, list_ptsForme, 5)
            #draw(screen, final_Gform)
            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    running = False
                    
                elif evt.type == pyg.MOUSEBUTTONDOWN:
                    pass
            pyg.display.flip()
            
            
            
            
    pyg.quit()
    exit()

if __name__ == '__main__':
    main()
