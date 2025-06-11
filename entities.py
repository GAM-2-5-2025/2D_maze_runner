import pygame
import settings
import math
import random
import game

class Player():
    def __init__(self, pos, width, height, around, skins):
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos.x, pos.y, width, height)
        self.rect.center = (game.gridSize * (self.pos.x + 0.5), game.gridSize * (self.pos.y + 0.5))
        self.move_pos = pos
        self.move_pos = self.pos
        self.moving = None
        self.around = around
        self.inputs = [-1,-1,-1,-1]
        self.skins = skins
        self.skin = self.skins[2][0]
        self.skinframe = 1


    def copy(self):
        return Player(self.pos, self. width, self.height, self.around, self.skins)

    
    def move(self, duration, events):

        time = pygame.time.get_ticks()

        # Za input delay malo drugacije moram ovo napisat ovako
        for event in events:
            
            if event.type == pygame.KEYDOWN:
                key = event.key

                if key in settings.up: self.inputs[0] = time
                if key in settings.left: self.inputs[1] = time
                if key in settings.down: self.inputs[2] = time
                if key in settings.right: self.inputs[3] = time
        
        if self.moving:
            try:
                self.pos = next(self.moving)
                x, y = (game.gridSize - self.width) / 2, (game.gridSize - self.height) / 2
                self.rect = pygame.Rect(game.gridSize * self.pos.x + x, game.gridSize * self.pos.y + y, self.width, self.height)
                return "Moving"
                
            except StopIteration:
                self.moving = None
        
        inde = settings.input_delay
        
        # Ako ide na prazno polje
        if self.around[0] == 0 and (time - self.inputs[0]) / 1000 <= inde:
            self.move_pos = pygame.Vector2(0, -1) + self.pos
            self.skin = self.skins[0][self.skinframe]
            self.skinframe += 1
            if(self.skinframe == 4): self.skinframe = 0
            
        elif self.around[1] == 0 and (time - self.inputs[1]) / 1000 <= inde:
            self.move_pos = pygame.Vector2(-1, 0) + self.pos
            self.skin = self.skins[1][self.skinframe]
            self.skinframe += 1
            if(self.skinframe == 4): self.skinframe = 0

        elif self.around[2] == 0 and (time - self.inputs[2]) / 1000 <= inde:
            self.move_pos = pygame.Vector2(0, 1) + self.pos
            self.skin = self.skins[2][self.skinframe]
            self.skinframe += 1
            if(self.skinframe == 4): self.skinframe = 0

        elif self.around[3] == 0 and (time - self.inputs[3]) / 1000 <= inde:
            self.move_pos = pygame.Vector2(1, 0) + self.pos
            self.skin = self.skins[3][self.skinframe]
            self.skinframe += 1
            if(self.skinframe == 4): self.skinframe = 0


        if self.move_pos == self.pos:
            return "Idle"

        self.moving = self.smooth_in_out(self.pos, self.move_pos, duration)
        return "Started"

        
            
    #def move_smash(self, duration)

    def smooth_in_out(self, start_pos, end_pos, duration):

        frame_number = int(duration * settings.FPS)

        for i in range(frame_number):
           t = (i+1) / frame_number
           t = - (math.cos(math.pi * t) - 1) / 2
           yield start_pos.lerp(end_pos, t)
           

class Zombie():
    def __init__(self, pos, width, height, around, skins):
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(1000, 1000, width, height)
        self.move_pos = pos
        self.move_pos = self.pos
        self.moving = None
        self.around = around
        self.last_move_time = pygame.time.get_ticks()
        self.move_time = settings.zombie_move_time
        self.pause_time = settings.zombie_pause_time
        self.last_pos = pos
        self.skins = skins
        self.skin = random.choice(self.skins)


    def copy(self):
        return Zombie(self.pos, self. width, self.height, self.around, self.skins)

    
    def move(self):
        
        if self.moving:
            try:
                self.pos = next(self.moving)
                x, y = (game.gridSize - self.width) / 2, (game.gridSize - self.height) / 2
                self.rect = pygame.Rect(game.gridSize * self.pos.x + x, game.gridSize * self.pos.y + y, self.width, self.height)
                return "Moving"
                
            except StopIteration:
                self.moving = None
                self.move_time -= settings.zombie_acceleration * self.move_time
                self.pause_time -= settings.zombie_acceleration * self.pause_time

        if (pygame.time.get_ticks() - self.last_move_time) / 1000 >= self.move_time + self.pause_time:

            self.last_move_time = pygame.time.get_ticks()
            
        
            directions = [pygame.Vector2(0, -1),
                      pygame.Vector2(-1, 0),
                      pygame.Vector2(0, 1),
                      pygame.Vector2(1, 0)
                      ]

            order = random.sample(list(range(0,4)), 4)
            
            for i in order:
                    
                # Ako ide na prazno polje
                if self.around[0] == 0 and i == 0:
                    self.move_pos = pygame.Vector2(0, -1) + self.pos
                    self.skin = self.skins[0]
                    break
                    
                elif self.around[1] == 0 and i == 1:
                    self.move_pos = pygame.Vector2(-1, 0) + self.pos
                    self.skin = self.skins[1]
                    break

                elif self.around[2] == 0 and i == 2:
                    self.move_pos = pygame.Vector2(0, 1) + self.pos
                    self.skin = self.skins[2]
                    break

                elif self.around[3] == 0 and i == 3:
                    self.move_pos = pygame.Vector2(1, 0) + self.pos
                    self.skin = self.skins[3]
                    break


        if self.move_pos == self.pos:
            return "Idle"

        self.last_pos = self.pos
        self.moving = self.smooth_in_out(self.pos, self.move_pos, self.move_time)
        return "Started"

        
            
    #def move_smash(self, duration)

    def smooth_in_out(self, start_pos, end_pos, duration):

        frame_number = int(duration * settings.FPS)

        for i in range(frame_number):
           t = (i+1) / frame_number
           t = - (math.cos(math.pi * t) - 1) / 2
           yield start_pos.lerp(end_pos, t)

class Smarter():
    def __init__(self, pos, width, height, around, skins):
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(1000, 1000, width, height)
        self.move_pos = pos
        self.move_pos = self.pos
        self.moving = None
        self.around = around
        self.last_move_time = pygame.time.get_ticks()
        self.move_time = settings.zombie_move_time
        self.pause_time = settings.zombie_pause_time
        self.last_pos = pos
        self.skins = skins
        self.skin = random.choice(self.skins)


    def copy(self):
        return Smarter(self.pos, self. width, self.height, self.around, self.skins)

    
    def move(self):
        
        if self.moving:
            try:
                self.pos = next(self.moving)
                x, y = (game.gridSize - self.width) / 2, (game.gridSize - self.height) / 2
                self.rect = pygame.Rect(game.gridSize * self.pos.x + x, game.gridSize * self.pos.y + y, self.width, self.height)
                return "Moving"
                
            except StopIteration:
                self.moving = None
                self.move_time -= settings.zombie_acceleration * self.move_time
                self.pause_time -= settings.zombie_acceleration * self.pause_time

        if (pygame.time.get_ticks() - self.last_move_time) / 1000 >= self.move_time + self.pause_time:

            self.last_move_time = pygame.time.get_ticks()
            
        
            directions = [pygame.Vector2(0, -1),
                      pygame.Vector2(-1, 0),
                      pygame.Vector2(0, 1),
                      pygame.Vector2(1, 0)
                      ]

            order = random.sample(list(range(0,4)), 4)

            for i in order:
                if directions[i] + self.pos == self.last_pos:
                    order.append(i)
                    order.remove(i)
            
            for i in order:
                    
                # Ako ide na prazno polje
                if self.around[0] == 0 and i == 0:
                    self.move_pos = pygame.Vector2(0, -1) + self.pos
                    self.skin = self.skins[0]
                    self.last_pos = self.pos
                    break
                    
                elif self.around[1] == 0 and i == 1:
                    self.move_pos = pygame.Vector2(-1, 0) + self.pos
                    self.skin = self.skins[1]
                    self.last_pos = self.pos
                    break

                elif self.around[2] == 0 and i == 2:
                    self.move_pos = pygame.Vector2(0, 1) + self.pos
                    self.skin = self.skins[2]
                    self.last_pos = self.pos
                    break

                elif self.around[3] == 0 and i == 3:
                    self.move_pos = pygame.Vector2(1, 0) + self.pos
                    self.skin = self.skins[3]
                    self.last_pos = self.pos
                    break


        if self.move_pos == self.pos:
            return "Idle"

        self.moving = self.smooth_in_out(self.pos, self.move_pos, self.move_time)
        return "Started"

        
            
    #def move_smash(self, duration)

    def smooth_in_out(self, start_pos, end_pos, duration):

        frame_number = int(duration * settings.FPS)

        for i in range(frame_number):
           t = (i+1) / frame_number
           t = - (math.cos(math.pi * t) - 1) / 2
           yield start_pos.lerp(end_pos, t)


class Brain():
    def __init__(self, pos, width, height, skins):
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(1000, 1000, width, height)
        self.move_pos = pos
        self.move_pos = self.pos
        self.moving = None
        self.last_move_time = pygame.time.get_ticks()
        self.move_time = settings.zombie_move_time
        self.pause_time = settings.zombie_pause_time
        self.last_pos = pos
        self.skins = skins
        self.skin = random.choice(self.skins)


    def copy(self):
        return Brain(self.pos, self. width, self.height, self.skins)

    
    def move(self, smjer):
        
        if self.moving:
            try:
                self.pos = next(self.moving)
                x, y = (game.gridSize - self.width) / 2, (game.gridSize - self.height) / 2
                self.rect = pygame.Rect(game.gridSize * self.pos.x + x, game.gridSize * self.pos.y + y, self.width, self.height)
                return "Moving"
                
            except StopIteration:
                self.moving = None
                self.move_time -= settings.zombie_acceleration * self.move_time
                self.pause_time -= settings.zombie_acceleration * self.pause_time

        if (pygame.time.get_ticks() - self.last_move_time) / 1000 >= self.move_time + self.pause_time and smjer != -1:

            self.last_move_time = pygame.time.get_ticks()
            
        
            directions = [pygame.Vector2(0, -1),
                      pygame.Vector2(-1, 0),
                      pygame.Vector2(0, 1),
                      pygame.Vector2(1, 0)
                      ]

            self.move_pos = self.pos + directions[smjer]
            self.skin = self.skins[smjer]


        if self.move_pos == self.pos:
            return "Idle"

        self.last_pos = self.pos
        self.moving = self.smooth_in_out(self.pos, self.move_pos, self.move_time)
        return "Started"

        
            
    #def move_smash(self, duration)

    def smooth_in_out(self, start_pos, end_pos, duration):

        frame_number = int(duration * settings.FPS)

        for i in range(frame_number):
           t = (i+1) / frame_number
           t = - (math.cos(math.pi * t) - 1) / 2
           yield start_pos.lerp(end_pos, t)
