import pygame as pyg
from form import Form
from GraphicForm import GraphicForm
from math import pi

def draw(screen, gForm):
    gForm.update()
    screen.blit(gForm.formeSurface, gForm.formeRect)

pyg.init()
screen = pyg.display.set_mode((800, 600))
pyg.display.set_caption('IA41 - Tangram')

screen.fill((200,200,200))
running = True

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

move = False
ptInitial = [0,0]
ptFinal = [0,0]
ptTmp = [0,0]
lastPtTmp = [0,0]
actualForm = None
pyg.key.set_repeat(1)
list_GraphicForm[0].forme.rotation(pi/4)
print(list_GraphicForm[0].forme.get_sommets())

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
                        ptInitial = pyg.mouse.get_pos()
                        actualForm = graphicForm
                        lastPtTmp = ptInitial
                        move = True

        elif pyg.mouse.get_pressed()[0] and move:
            ptTmp = pyg.mouse.get_pos()
            actualForm.move(lastPtTmp, ptTmp)
            screen.fill((200,200,200))
            lastPtTmp = ptTmp

        elif evt.type == pyg.MOUSEBUTTONUP and move:
            ptFinal = pyg.mouse.get_pos()
            actualForm.move(lastPtTmp, ptFinal)
            screen.fill((200,200,200))
            move = False

        elif evt.type == pyg.KEYDOWN:
            if evt.key == pyg.K_ESCAPE:
                running = False

pyg.quit()
exit()
