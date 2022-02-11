import pygame
from pygame import *

pygame.init()
pygame.display.set_caption("Where's Wolf")
screen = pygame.display.set_mode((1024, 768))
screen_r = screen.get_rect()
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

class Credits:


    def credits():

        credit_list = ["ZYVASY",
                        "",
                        "Zineddine CHALEKH",
                        "Symeon DE ALMEIDA",
                        "Valentin WIBAILLIE",
                        "",
                        "VISUEL",
                        "",
                        "Lanea Zimmerman et William Thompson : Toutes les tuiles des maps ",
                        "Enjl : Arrière plan jour/nuit",
                        "DoubleLeggy : Atlas de texture des PNJ (Sprite Sheet)",
                        "Matt Firth (cheekyinkling) et game-icons.net : Icones des items",
                        "",
                        "MUSIQUE",
                        "",
                        "Derek et Brandon Fiechter :",
                        "Elf Village (Day)",
                        "Haunted Village (Night)",
                        "",
                        "BRUITAGES",
                        "",
                        "Mixkit",
                        "La Sonotheque",
                        "Sound-Fishing",
                        "Jamius",]

        texts = []

        for i, line in enumerate(credit_list):
            s = font.render(line, 1, (255, 255, 255))

            r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
            texts.append((r, s))

        while True:
            for e in pygame.event.get():
                if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            screen.fill((10, 10, 10))

            for r, s in texts:
                r.move_ip(0, -1)
                screen.blit(s, r)

            if not screen_r.collidelistall([r for (r, _) in texts]):
                return

            pygame.display.flip()

            clock.tick(60)