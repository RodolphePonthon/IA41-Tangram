from form import Form

class GraphicForm:
    def __init__(self, form, posX, posY):
        #initialisation Surface
        formeSurface = pyg.Surface((300, 300))
        formeSurface.fill((0,0,0))
        formeSurface.set_colorkey((0,0,0))
        #initialisation Rectangle
        formeRect = formeSurface.get_rect()
        formeRect.y = posY
        formeRect.x = posX

        pyg.draw.polygon(formeSurface, (1,1,1), form.get_sommets(),1)

    def draw(self):
        screen.blit(formeSurface, formeRect)
