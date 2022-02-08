import pygame
import sys

class Inventory:
    def __init__(self):
        self.rows = 3
        self.col = 9
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 40
        self.x = 50
        self.y = 50
        self.border = 3
    
    #draw everything
    def draw(self, screen):
        font = pygame.font.Font(pygame.font.match_font("calibri"),26)
        #draw background
        pygame.draw.rect(screen,(100,100,100),
                         (self.x,self.y,(self.box_size + self.border)*self.col + self.border,(self.box_size + self.border)*self.rows + self.border))
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border)*x + self.border,self.x + (self.box_size + self.border)*y + self.border,self.box_size,self.box_size )
                pygame.draw.rect(screen,(180,180,180),rect)
                if self.items[x][y]:
                    screen.blit(self.items[x][y][0].resize(self.box_size),rect)
                    obj = font.render(str(self.items[x][y][1]),True,(0,0,0))
                    screen.blit(obj,(rect[0] + self.box_size//2, rect[1] + self.box_size//2))
                    
    #get the square that the mouse is over
    def Get_pos(self):
        mouse = pygame.mouse.get_pos()
        
        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x//(self.box_size + self.border)
        y = y//(self.box_size + self.border)
        return (x,y)
    
    #add an item/s
    def Add(self,Item,xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].id == Item[0].id:
                self.items[x][y][1] += Item[1]
            else:
                temp = self.items[x][y]
                self.items[x][y] = Item
                return temp
        else:
            self.items[x][y] = Item
    
    #check whether the mouse in in the grid
    def In_grid(self,x,y):
        if 0 > x > self.col-1:
            return False
        if 0 > y > self.rows-1:
            return False
        return True

    def run(screen, inventoryHandle):

        runInventory = True
        while runInventory:
            screen.fill((0,0,0))
            inventoryHandle.draw(screen)
            mousex, mousey = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(2)

            pygame.display.update()
