import pygame, os

class screengenerator:
    def __init__(self):
        print('init')

    def make_window(self, width=1000, height=700, color=(0, 0, 0), image="null"):
        size = width, height
        screen = pygame.display.set_mode(size)
        screen.fill(color)

        if image != "null":
            b = image + ".bmp"
            img = pygame.image.load(os.path.join("images", b)).convert_alpha()
            screen.blit(img, (0, 0))

        return screen

    def make_miniwindow(self, width=600, height=300, color=(0, 0, 0)):
        size = width, height
        miniwindow = pygame.Surface(size)
        miniwindow.fill(color)
        return miniwindow

    def make_logwindow(self, width=325, height=625, color=(0, 0, 0)):
        size = width, height
        logwindow = pygame.Surface(size)
        logwindow.fill(color)
        return logwindow

    def make_textsurface(self, fontsize=20, message="no message passed into object", bg = (0, 0, 0), fg = (255, 255, 255), stdfont=False ):
        if stdfont:
            font = pygame.font.Font(None, fontsize)
        else:
            f = os.path.join("fonts", "oetmt.ttf")
            font = pygame.font.Font(f, fontsize)
        textline = font.render(message, 0, fg, bg)
        return textline

