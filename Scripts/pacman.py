import pygame as pg
from pygame.sprite import Group
import map as mp
import time as tm
import random as rd

class Pacman(pg.sprite.Sprite):
    
    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)
        self.sprite = r'..\Assets\Sprites\pacman\pacman_left.png'
        self.image = pg.image.load(r'..\Assets\Sprites\pacman\pacman_left.png')
        self.image= pg.transform.scale(self.image,(mp.scale_multi,mp.scale_multi))
        self.rect = self.image.get_rect()
        self.rect.move_ip(10*mp.scale_multi,20*mp.scale_multi)

        self.state = None
        self.next_state = 'left'
        self.coord_graph = [(10,20)]
        self.first_move = True
        self.side_sprite = 'left.png'

        self.exec_time = 1

        self.score = 0
        self.dead = False
        self.gameover = False
        self.lifes = 4
        self.live_time = tm.time()

        self.can_kill_red = False
        self.can_kill_blue = False
        self.can_kill_orange = False
        self.can_kill_pink = False
        self.can_kill_time = 0

    def update(self):

        self.teleport()
        self.move()
        self.update_coord_graph()
        self.collide_pac_dot()
        self.cant_kill()


    def move(self):
        if self.collision():
            self.state = None
        else:
            if self.state == None and self.next_state != None and self.first_move == False:               
                self.state = self.next_state 
                self.coord_graph.pop()#quand pacman subit une collision mon programme considére qu'il est en traversé 
                                      #donc si il change de direction ça va causer des pbs avec les collisions et les coordonnées de pacman 
                                      #donc on supprime la case d'arrivé de la traversé et non celle de départ.
            if self.state == 'left':
                self.side_sprite = self.state + '.png'
                self.rect.move_ip(-mp.scale_multi*(1+self.exec_time)/28,0)            
            
            if self.state == 'right':
                self.side_sprite = self.state + '.png'
                self.rect.move_ip(mp.scale_multi*(1+self.exec_time)/28,0)
            
            if self.state == 'up':
                self.side_sprite = self.state + '.png'
                self.rect.move_ip(0,-mp.scale_multi*(1+self.exec_time)/28)
            
            if self.state == 'down':
                self.side_sprite = self.state + '.png'
                self.rect.move_ip(0,mp.scale_multi*(1+self.exec_time)/28)

            self.image = pg.image.load(str(r'..\Assets\Sprites\pacman\pacman_'+self.side_sprite))
            self.image= pg.transform.scale(self.image,(mp.scale_multi,mp.scale_multi))



    def collision(self):

        if len(self.coord_graph) == 2 and (self.next_state ==  'up' or self.next_state == 'down') and\
              (self.state == 'left' or self.state == 'right') :
            self.next_state = None
            return True
        
        elif len(self.coord_graph) == 2 and (self.next_state ==  'left' or self.next_state == 'right') and\
              (self.state == 'up' or self.state == 'down') :
            self.next_state = None
            return True
        elif self.next_state == 'left' and (mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]-1]  == 'X' \
                    or mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]-1]  == '-'):
            return True
                    
        elif self.next_state == 'right' and (mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]+1]  == 'X' \
                    or mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]+1]  == '-'):
            return True
                    
        elif self.next_state == 'up' and (mp.maps[mp.map_i].map_list[self.coord_graph[0][1]-1][self.coord_graph[0][0]]  == 'X' \
                    or mp.maps[mp.map_i].map_list[self.coord_graph[0][1]-1][self.coord_graph[0][0]]  == '-'):
            return True
                
        elif self.next_state == 'down' and (mp.maps[mp.map_i].map_list[self.coord_graph[0][1]+1][self.coord_graph[0][0]]  == 'X' \
                    or mp.maps[mp.map_i].map_list[self.coord_graph[0][1]+1][self.coord_graph[0][0]] == '-'):
            return True
        
        else: 
            return False

    def collide_pac_dot(self):
        if mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]]  == '.' \
                    or mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]]  == '0':
            
            if mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]]  == '0':
                self.can_kill_red = True
                self.can_kill_blue = True
                self.can_kill_orange = True
                self.can_kill_pink = True

                self.can_kill_time = tm.time()
                
            
            mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]] = '/'
            
            mp.tile_map.add(mp.maps[mp.map_i].map_tile_list)
            
            coord = self.coord_graph[0][1] + self.coord_graph[0][1] * self.coord_graph[0][0]
            
            mp.maps[mp.map_i].map_tile_list.insert(coord,mp.MapTile(r'..\Assets\Sprites\map_tile\background.png'))
            mp.maps[mp.map_i].map_tile_list.pop(coord+1)
            mp.maps[mp.map_i].map_tile_list[coord].rect.move_ip(self.coord_graph[0][0]*mp.scale_multi,self.coord_graph[0][1]*mp.scale_multi)
            
            mp.tile_map.add(mp.maps[mp.map_i].map_tile_list)

            self.score += 10
    
    def update_coord_graph(self):
        if len(self.coord_graph) > 1:
            if (self.rect.x <= self.coord_graph[0][0] *mp.scale_multi - mp.scale_multi and self.state == 'left') \
                or (self.rect.y <= self.coord_graph[0][1] *mp.scale_multi - mp.scale_multi and self.state =='up'):#Quand pacman traverse deux cases et qu'il arrive à la suivante cette contidition suprime la case de départ des cases qui sont entrain d'être traversé 
                self.coord_graph.remove(self.coord_graph[0])
        else:
            if self.next_state == 'left' :
                self.coord_graph.append((self.coord_graph[0][0]-1,self.coord_graph[0][1]))#ajoute la case d'arrivé pendant la traversé de deux cases
                self.state = self.next_state
                self.first_move = False
            
            if self.next_state == 'up' :
                self.coord_graph.append((self.coord_graph[0][0],self.coord_graph[0][1]-1))
                self.state = self.next_state
                self.first_move = False
            
        if len(self.coord_graph) > 1:
            if (self.rect.x >= self.coord_graph[0][0] *mp.scale_multi + mp.scale_multi and self.state == 'right') \
                    or (self.rect.y >= self.coord_graph[0][1] *mp.scale_multi + mp.scale_multi and self.state =='down'):
                self.coord_graph.remove(self.coord_graph[0])

        else:
            if self.next_state == 'right':
                self.coord_graph.append((self.coord_graph[0][0]+1,self.coord_graph[0][1]))
                self.state = self.next_state
                self.first_move = False
                
            if self.next_state == 'down':
                self.coord_graph.append((self.coord_graph[0][0],self.coord_graph[0][1]+1))
                self.state = self.next_state
                self.first_move = False
    
    def cant_kill(self):
        if tm.time() >= self.can_kill_time + 10:
            self.can_kill_blue = False
            self.can_kill_red = False
            self.can_kill_orange = False
            self.can_kill_pink = False

    def can_tp(self):
        return len(self.coord_graph) == 1 and (self.coord_graph[0] in mp.maps[mp.map_i].tp_tile_list)
    
    
    def teleport(self):
        if self.can_tp():
            actual_place = self.coord_graph[0]
            mp.maps[mp.map_i].tp_tile_list.remove(actual_place)
            tp_tile = mp.maps[mp.map_i].tp_tile_list[rd.randint(0,len(mp.maps[mp.map_i].tp_tile_list)-1)]
            self.rect.move_ip(tp_tile[0] * mp.scale_multi - self.rect.x, tp_tile[1] * mp.scale_multi - self.rect.y)
            self.coord_graph = [tp_tile]
            mp.maps[mp.map_i].tp_tile_list.append(actual_place)




class PacLife(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(r'..\Assets\Sprites\pacman\pacman_right.png')
        self.rect = self.image.get_rect()
        self.image= pg.transform.scale(self.image,(mp.scale_multi//1.5,mp.scale_multi//1.5))
        self.rect.move_ip(x,y)


pacman = Pacman()
paclife_sprite = [PacLife(0.5*mp.scale_multi,15.5*mp.scale_multi),PacLife(1.2*mp.scale_multi,15.5*mp.scale_multi),PacLife(1.9*mp.scale_multi,15.5*mp.scale_multi),PacLife(2.6*mp.scale_multi,15.5*mp.scale_multi)]
pg.init()
paclife_sprites = pg.sprite.RenderPlain(paclife_sprite)