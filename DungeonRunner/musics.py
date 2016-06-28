from pygame.mixer import *
import os, pygame
class musics:
    def __init__(self):
        pygame.mixer.init()

        self.backgroundmusic = os.path.join("music", "background.ogg")
        self.battlemusic     = os.path.join("music", "battle.ogg")
        self.victorymusic    = os.path.join("music", "victory.ogg")
        self.ssound          = os.path.join("music", "sound.ogg")

    def b_start(self):
        pygame.mixer.music.load(self.battlemusic)
        pygame.mixer.music.play()

    def b_pause(self):
        pygame.mixer.music.pause()

    def b_stop(self):
        pygame.mixer.music.stop()

    def v_play(self):
        # victory tone is not persistent, so let it play out and fade
        pygame.mixer.music.load(self.victorymusic)
        pygame.mixer.music.play()
        pygame.mixer.music.fadeout(5000)

    def s_play(self):
        s = pygame.mixer.Sound(self.ssound)
        s.play()

    def background_play(self):
        pygame.mixer.music.load(self.backgroundmusic)
        pygame.mixer.music.play(-1)

    def background_stop(self):
        pygame.mixer.music.stop()