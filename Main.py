import pygame as pyg
from form import Form
from GraphicForm import GraphicForm

def draw(screen, gForm):
    screen.blit(gForm.formeSurface, gForm.formeRect)

pyg.init()
screen = pyg.display.set_mode((800, 600))
pyg.display.set_caption('IA41 - Tangram')

screen.fill((255,255,255))
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
    list_GraphicForm.append(GraphicForm(form, 0, 0))



move = False
ptInitial = [0,0]
ptFinal = [0,0]
actualForm = None

while running:


    pyg.display.flip()

    for gForm in list_GraphicForm:
        draw(screen, gForm)

    for evt in pyg.event.get():
        if evt.type == pyg.QUIT:
            running = False

        elif evt.type == pyg.MOUSEBUTTONDOWN:
            if evt.type == pyg.MOUSEBUTTONDOWN:
                for graphicForm in list_GraphicForm:
                    if graphicForm.isOn(pyg.mouse.get_pos(), graphicForm.formeSurface.get_height()):
                        ptInitial = pyg.mouse.get_pos()
                        actualForm = graphicForm
                        move = True

        elif evt.type == pyg.MOUSEBUTTONUP and move == True:
            ptFinal = pyg.mouse.get_pos()
            actualForm.move(ptInitial, ptFinal)
            screen.fill((255,255,255))
            move = False

        elif evt.type == pyg.KEYDOWN:
            if evt.key == pyg.K_ESCAPE:
                running = False

            if evt.key == pyg.K_SPACE:
                formeRect.x += 1
                screen.fill(white)
                screen.blit(dessinSurface, dessinRect)
                screen.blit(rangementSurface, rangementRect)
                screen.blit(formeSurface, formeRect)



pyg.quit()
exit()
