#!--*--coding:utf-8--*--

from copy import deepcopy
import pygame as pyg
from form import Form
from GraphicForm import GraphicForm
from Silhouette import silhouette
from ArtInt import Ia
from math import pi
from os import environ
from zone import Zone
from Button import Button
from convert_to_draw import convert_to_draw
from sys import exit

environ['SDL_VIDEO_CENTERED'] = '1'

#Draw form with border
def draw(screen, gForm, withBorder = True):
    gForm.update(withBorder)
    screen.blit(gForm.formeSurface, gForm.formeRect)

#Create a list of forms in the initialize position
def init_forms(width, height):
    triangle = Form([[50,50],[0,100],[0,0]])
    triangle2 = Form([[100,0],[50,50],[0,0]])
    triangle3 = Form([[50,100],[100,50],[100,100]])
    triangle4 = Form([[75,25],[100,0],[100,50]])
    triangle5 = Form([[25,75],[50,50],[75,75]])
    carre = Form([[50,50],[75,25],[100,50],[75,75]])
    para = Form([[0,100],[25,75],[75,75],[50,100]])

    #List sorted by "area", the biggest forms first 
    list_forms = [triangle, triangle2, triangle3, para, carre,triangle4, triangle5]
    list_GraphicForm = []
    for form in list_forms:
        list_GraphicForm.append(GraphicForm(form, width/4 - height/4, int(height/4), int(height/2)))

    return list_GraphicForm

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
    icon = pyg.image.load('Textures/icone.png')
    pyg.display.set_icon(icon)
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
    list_ptsFormeSurface = []
    actualForm = None
    silhouetteForme = None
    zoneDessin = Zone((width/2, 0), (width/2, height), "Textures/ZoneDessin.png")
    zoneDepart = Zone((width/4 - height/4, height/4), (height/2, height/2), "Textures/ZoneDepart.png")
    titreBg = Zone((0, 0), (width/2, height), "Textures/menuBg.png", False)
    zoneTransition = Zone((0, 0), (width/2, height), "Textures/ZoneDessin.png")
    msgSelect = Zone((0, 3*height/4), (width/2, 20*height/600), "Textures/messageSelection.png")
    buttonLock = Button((width/4-width/8, height-height/6), (width/4, height/8), "Textures/buttonLock.png")
    buttonCheck = Button((width/2-height*50/600, height-height*50/600), (height*50/600, height*50/600), "Textures/buttonCheck.png")

    #"Magnet", is applied to all forms in order to have a good start position
    for gForm in list_GraphicForm:
            for gForm2 in list_GraphicForm:
                gForm.magnet(gForm2, width, height)

    while running:
        #first phase, the user move and rotate forms to create a new one (silhouette)
        if phase == 1:
            #Place zones
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
                    #testing if we are on a button and move to the phase  2
                    zoneDepartVide = 1
                    if buttonLock.isOn(pyg.mouse.get_pos()):
                        for Gforme in list_GraphicForm:
                            if zoneDepart.isOn(Gforme):
                                zoneDepartVide = 0
                        if zoneDepartVide:
                            zoneDessin = Zone((width/2, 0), (width/2, height), "Textures/ZoneDessin.png")
                            phase = 2

                #Move the selected form
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

                #Rotate the selected form
                elif pyg.mouse.get_pressed()[0] and turn:
                    ptTmp = pyg.mouse.get_pos()
                    angle = (lastPtTmp[1] - ptTmp[1])
                    if abs(angle) > pasInterval:
                        sens = angle/abs(angle)
                        for i in range(pasInterval):
                            actualForm.forme.rotation(pi*sens/interval)
                        screen.fill((200,200,200))
                        lastPtTmp = ptTmp

                #Move the selected form
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

                #Rotate the selected form
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

        #Second phase, creation of the silhouette
        elif phase == 2:
            #Place zones
            screen.blit(zoneTransition.surface, zoneTransition.rect)
            screen.blit(zoneDessin.surface, zoneDessin.rect)

            #Draw Forms
            for gForm in list_GraphicForm:
                if zoneDessin.isOn(gForm):
                    draw(screen, gForm, withBorder)
                else:
                    draw(screen, gForm)
              
            #Print the silhouette in real time
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
                                
                    # Testing if the silhouette is finished and move to phase 3
                    if buttonCheck.isOn(pyg.mouse.get_pos()):
                        if list_ptsForme != []:
                            list_ptsFormeTmp = [list_ptsForme[0]]
                            for i in range(1, len(list_ptsForme)):
                                if (list_ptsForme[i][0] != list_ptsForme[i-1][0]) or (list_ptsForme[i][1] != list_ptsForme[i-1][1]):
                                    list_ptsFormeTmp.append(list_ptsForme[i])
                            list_ptsForme = list_ptsFormeTmp
                            if len(list_ptsForme) > 2 and list_ptsForme[0] == list_ptsForme[-1]:
                                list_ptsFormeSurface = [deepcopy(pt) for pt in list_ptsForme]
                                for pt in list_ptsForme:
                                    pt[0] += width/2
                                silhouetteForme = silhouette(list_ptsForme)
                                silhouetteForme.clean_couples()
                                zoneTransition = Zone((0, 0), (width/2, height), "Textures/ZoneDessin.png")
                                phase = 3
    
        #Laste phase, call of the AI 
        elif phase ==3:

            for evt in pyg.event.get():
                if evt.type == pyg.QUIT:
                    running = False
                    
                    
            #Draw forms
            pyg.draw.lines(zoneDessin.surface, (255,0,0), False, list_ptsFormeSurface, 5)
            
            forms_ia = init_forms(width, height)

            #Print the forms give to the AI
            for gforme in forms_ia:
                pyg.draw.polygon(zoneTransition.surface, (0,0,0), gforme.get_sommets(gforme.forme.new_scale))
                pyg.draw.polygon(zoneTransition.surface, (200,200,200), gforme.get_sommets(gforme.forme.new_scale), 4)
                    
            #Place zones
            screen.blit(zoneTransition.surface, zoneTransition.rect)
            screen.blit(zoneDessin.surface, zoneDessin.rect)
            
            pyg.display.flip()

            # create and call the AI with the silhouette and a list a form (starting square)            
            ia = Ia(silhouetteForme, forms_ia, width, height)
            
            pyg.display.flip()
            
            list_GraphicForm = ia.list_form
            list_ptsForme = []
            
            zoneTransition = Zone((0, 0), (width/2, height), "Textures/ZoneDessin.png")
            phase = 1
    pyg.quit()
    exit()

if __name__ == '__main__':
    main()
