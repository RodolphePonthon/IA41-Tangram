import pygame as pyg
from form import Form
from GraphicForm import GraphicForm
from math import pi

def draw(screen, gForm):
    gForm.update()
    screen.blit(gForm.formeSurface, gForm.formeRect)

def init_forms():
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
        list_GraphicForm.append(GraphicForm(form, 10, 150))

    return list_GraphicForm

def gestion_event(evt):
    pass

def main():
    #Initialize screen
    pyg.init()
    screen = pyg.display.set_mode((800, 600))
    pyg.display.set_caption('IA41 - Tangram')
    screen.fill((200,200,200))

    #Initialize variables
    list_GraphicForm = init_forms()
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
    pyg.key.set_repeat(True)

    while running:

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
                            if graphicForm.isCornerSelected(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                                ptInitial = pyg.mouse.get_pos()
                                actualForm = graphicForm
                                lastPtTmp = ptInitial
                                turn = True
                            else:
                                ptInitial = pyg.mouse.get_pos()
                                actualForm = graphicForm
                                lastPtTmp = ptInitial
                                move = True

            elif pyg.mouse.get_pressed()[0] and move:
                ptTmp = pyg.mouse.get_pos()
                actualForm.move(lastPtTmp, ptTmp)
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
                actualForm.move(lastPtTmp, ptFinal)
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

    pyg.quit()
    exit()

if __name__ == '__main__':
    main()