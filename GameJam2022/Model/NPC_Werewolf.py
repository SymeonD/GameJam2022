from NPC import NPC as parent

class NPC_Werewolf(parent):

    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        self.moonCycle = 1;
        self.type = 'speed';