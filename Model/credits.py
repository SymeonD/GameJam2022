import pygame
from pygame import *

pygame.init()
pygame.display.set_caption("Where's Wolf")
screen = pygame.display.set_mode((1024, 768))
screen_r = screen.get_rect()
font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()

def credits():

    credit_list = ["THE END"," ","EQUIPE ZYVASY","","Zineddine CHALEKH","Symeon DE ALMEIDA","Valentin WIBAILLIE","","MUSIQUE"," ", "Free Music Archive","Night Moments by Loco Roco","", "BRUITAGES","", "La Sonotheque","","","","Merci d'avoir joué à Where's Wolf ? !"]

    texts = []
    # we render the text once, since it's easier to work with surfaces
    # also, font rendering is a performance killer
    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (255, 255, 255))
        # we also create a Rect for each Surface. 
        # whenever you use rects with surfaces, it may be a good idea to use sprites instead
        # we give each rect the correct starting position 
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        screen.fill((10, 10, 10))

        for r, s in texts:
            # now we just move each rect by one pixel each frame
            r.move_ip(0, -1)
            # and drawing is as simple as this
            screen.blit(s, r)

        # if all rects have left the screen, we exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            return

        # only call this once so the screen does not flicker
        pygame.display.flip()

        # cap framerate at 60 FPS
        clock.tick(60)