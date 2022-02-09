import pygame
import sys


class Inventory:
    def __init__(self):
        self.rows = 2
        self.cols = 9
        self.capacity = self.rows * self.cols
        self.items = []
        self.box_size = 34
        self.x = 650
        self.y = 650
        self.border = 3
        self.rect = (self.x, self.y, (self.box_size + self.border) * self.cols + self.border,
                     (self.box_size + self.border) * self.rows + self.border)

    def add(self, newItem):
        add = None
        itemNum = 0
        for item in self.items:
            if item:
                itemNum += 1
                if newItem == item[0]:
                    item[1] += 1
                    add = True
        if not add and self.capacity > itemNum:
            self.items.append([newItem, 1])
        elif self.capacity < itemNum:
            print("inventaire plein")

        for items in self.items:
            print(items[0].name + " : " + str(items[1]))

    def drawInventory(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        numcase = 0
        font = pygame.font.Font(pygame.font.match_font("calibri"), 22)

        for x in range(self.cols):
            for y in range(self.rows):
                caseRect = (self.x + (self.box_size + self.border) * x + self.border,
                            self.x + (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                pygame.draw.rect(screen, (180, 180, 180), caseRect)

                # Si il y a un item dans la case
                if numcase < len(self.items):
                    screen.blit(self.items[numcase][0].image, caseRect)
                    amount = font.render(str(self.items[numcase][1]), True, (0, 0, 0))
                    screen.blit(amount, (caseRect[0] + self.box_size // 2, caseRect[1] + self.box_size // 2))

                numcase += 1

    def update(self, screen, inventory):
        self.drawInventory(screen)

    #check if the mouse is in tge grid
    def in_grid(self, posX, posY):
        if self.x > posX or posX > self.x+(self.cols+1)*self.border+self.cols*self.box_size:
            return False
        if self.y > posY or posY > self.y+(self.rows+1)*self.border+self.rows*self.box_size:
            return False
        return True

    #return item in position
    def getItem(self, posX, posY):
        case = 0
        if (posY-650)//38.5 >= 1:
            case = ((posX-650)//(336/9))*2+2
        else:
            case = ((posX - 650) // (336 / 9)*2)+1
        if len(self.items) >= case:
            return self.items[int(case)-1][0]



    """
    #draw everything
    def draw(self, screen):
        font = pygame.font.Font(pygame.font.match_font("calibri"),22)
        #draw background
        pygame.draw.rect(screen,(100,100,100),
                         (self.x,self.y,(self.box_size + self.border)*self.col + self.border,(self.box_size + self.border)*self.rows + self.border))
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border)*x + self.border,self.x + (self.box_size + self.border)*y + self.border,self.box_size,self.box_size )
                pygame.draw.rect(screen,(180,180,180),rect)
                if self.items[x][y]:
                    screen.blit(self.items[x][y].surface, rect)
                    #screen.blit(self.items[x][y][0].resize(self.box_size),rect)
                    obj = font.render(str(self.items[x][y].image), True, (0, 0, 0))
                    #obj = font.render(str(self.items[x][y][1]), True, (0, 0, 0))
                    screen.blit(obj, (rect[0] + self.box_size//2, rect[1] + self.box_size//2))

    def open(screen, inventoryHandle):
        selected = None
        inventoryHandle.draw(screen)

        font = pygame.font.Font(pygame.font.match_font("calibri"),22)
        mousex, mousey = pygame.mouse.get_pos()

        #dessine l'item sélectionner à côte de la souris
        if selected:
            screen.blit(selected[0].resize(30),(mousex,mousey))
            obj = font.render(str(selected[1]),True,(0,0,0))
            screen.blit(obj,(mousex + 15, mousey + 15))

            #récupere la position de la souris dans l'inventaire (quelle case ?)
            pos = inventoryHandle.Get_pos()
            if inventoryHandle.In_grid(pos[0],pos[1]):
                if selected:
                    selected = inventoryHandle.Add(selected,pos)
                elif inventoryHandle.items[pos[0]][pos[1]]:
                    selected = inventoryHandle.items[pos[0]][pos[1]]
                    inventoryHandle.items[pos[0]][pos[1]] = None
    """
