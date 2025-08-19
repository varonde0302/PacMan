import pygame as pg
from pygame.sprite import Group
import data_struct as ds
import map as mp
import pacman as pc
import random as rd
import time as tm

class Ghost(pg.sprite.Sprite):
    def __init__(self,color) -> None:
        pg.sprite.Sprite.__init__(self)
        self.color = color
        
        if self.color == 'red':
            self.image = pg.image.load(r'..\Assets\Sprites\ghost\temp_red_ghost.png')
        if self.color == 'orange':
            self.image = pg.image.load(r'..\Assets\Sprites\ghost\orange_ghost.png')
        if self.color == 'pink':
            self.image = pg.image.load(r'..\Assets\Sprites\ghost\pink_ghost.png')
        if self.color == 'lightblue':
            self.image = pg.image.load(r'..\Assets\Sprites\ghost\light_blue_ghost.png')
        
        self.image= pg.transform.scale(self.image,(mp.scale_multi,mp.scale_multi))
        self.rect = self.image.get_rect()
        self.rect.move_ip(10*mp.scale_multi,12*mp.scale_multi)


        self.coord_graph = [(10,12)]
        self.way = []
        self.back_up_start_way = []
        self.state = None

        self.can_start = False
        self.sarretepouruneraisonquejecomprendspas = False

        self.can_die = False
        self.escape_tile = mp.maps[mp.map_i].accessible_tile[rd.randint(0,len(mp.maps[mp.map_i].accessible_tile))-1]

        self.finish_first_way = False
        self.time_pause = 0
    
    def update(self):
        global nb_ghost_start
        if self.can_start:
            self.finish_way()
            self.big_update_way()
            self.collied_pacman()
            self.can_be_kill()
            self.update_sprite()
            self.update_coord()
            self.move()
            self.in_wall()
            self.reset()
        else:
            self.start()
        

    def move(self):
        self.change_state()

        if self.state == 'left':
            self.rect.move_ip(-4,0)
        
        if self.state == 'right':
            self.rect.move_ip(4,0)
        
        if self.state == 'up':
            self.rect.move_ip(0,-4)
        
        if self.state == 'down':
            self.rect.move_ip(0,4)

    
    def change_state(self):
        if not self.sarretepouruneraisonquejecomprendspas:
            if len(self.way)>2:
                can_change = self.can_change_state()
                if self.way[0] != None:
                    if not can_change:

                        self.state = None
                        self.sarretepouruneraisonquejecomprendspas = True
                    if can_change and self.coord_graph[0][0] == self.way[1][0]+1 and self.coord_graph[0][1] == self.way[1][1]:
                        self.state = 'left'
                    
                    if can_change and self.coord_graph[0][0] == self.way[1][0]-1 and self.coord_graph[0][1] == self.way[1][1]:
                        self.state = 'right'
                    
                    if can_change and self.coord_graph[0][0] == self.way[1][0] and self.coord_graph[0][1] == self.way[1][1]+1:
                        self.state = 'up'
                    
                    if can_change and self.coord_graph[0][0] == self.way[1][0] and self.coord_graph[0][1] == self.way[1][1]-1:
                        self.state = 'down'

                else:
                    self.state = None         
            else:
                self.state = None
        
        else:
            if self.coord_graph[0][0] == self.way[0][0]-1 and self.coord_graph[0][1] == self.way[0][1]-1:
                self.state = 'right_down'
                    
            if self.coord_graph[0][0] == self.way[0][0]+1 and self.coord_graph[0][1] == self.way[0][1]-1:
                self.state = 'left_down'
                    
            if self.coord_graph[0][0] == self.way[0][0]-1 and self.coord_graph[0][1] == self.way[0][1]+1:
                self.state = 'right_up'

            if self.coord_graph[0][0] == self.way[0][0]+1 and self.coord_graph[0][1] == self.way[0][1]+1:
                self.state = 'left_up'
            
            
            
            if (self.state == 'right_down' or self.state == 'right_up') \
                and mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]+1] != 'X':

                self.way.insert(0,(self.coord_graph[0][0]+1,self.coord_graph[0][1]))
                self.way.insert(0,(self.coord_graph[0][0],self.coord_graph[0][1]))
                self.state = 'right'
                if len(self.coord_graph)>1:
                    self.coord_graph.pop()
            
            elif (self.state == 'left_down' or self.state == 'left_up') \
                and mp.maps[mp.map_i].map_list[self.coord_graph[0][1]][self.coord_graph[0][0]-1] != 'X':

                self.way.insert(0,(self.coord_graph[0][0]-1,self.coord_graph[0][1]))
                self.way.insert(0,(self.coord_graph[0][0],self.coord_graph[0][1]))
                self.state = 'left'
                if len(self.coord_graph)>1:
                    self.coord_graph.pop()

            elif (self.state == 'right_down' or self.state == 'left_down') \
                and mp.maps[mp.map_i].map_list[self.coord_graph[0][1]+1][self.coord_graph[0][0]] != 'X':

                self.way.insert(0,(self.coord_graph[0][0],self.coord_graph[0][1]+1))
                self.way.insert(0,(self.coord_graph[0][0],self.coord_graph[0][1]))
                self.state = 'down'
                if len(self.coord_graph)>1:
                    self.coord_graph.pop()

            elif (self.state == 'right_up' or self.state == 'left_up') \
                and mp.maps[mp.map_i].map_list[self.coord_graph[0][1]-1][self.coord_graph[0][0]] != 'X':

                self.way.insert(0,(self.coord_graph[0][0],self.coord_graph[0][1]-1))
                self.way.insert(0,(self.coord_graph[0][0],self.coord_graph[0][1]))
                self.state = 'up'
                if len(self.coord_graph)>1:
                    self.coord_graph.pop()

            self.sarretepouruneraisonquejecomprendspas = False

        
    def can_change_state(self):
        if self.state == 'up' and self.rect.y <= self.coord_graph[0][1]*mp.scale_multi-mp.scale_multi:
            self.way.pop(0)
            self.coord_graph.pop(0)
            return True
        
        if self.state == 'down' and self.rect.y >= self.coord_graph[0][1]*mp.scale_multi+mp.scale_multi:
           self.way.pop(0)
           self.coord_graph.pop(0)
           return True 
        
        if self.state == 'right' and self.rect.x >= self.coord_graph[0][0]*mp.scale_multi+mp.scale_multi:
            self.way.pop(0)
            self.coord_graph.pop(0)
            return True
        
        if self.state == 'left' and self.rect.x <= self.coord_graph[0][0]*mp.scale_multi-mp.scale_multi:
            self.way.pop(0)
            self.coord_graph.pop(0)
            return True
        
        if self.state == None:
            return True
        
        else:            
            return False
        
    
    def update_coord(self):
        if self.state == 'up' and len(self.coord_graph)<2:
            self.coord_graph.append((self.coord_graph[0][0],self.coord_graph[0][1]-1))
        
        if self.state == 'down' and len(self.coord_graph)<2:
            self.coord_graph.append((self.coord_graph[0][0],self.coord_graph[0][1]+1))
        
        if self.state == 'left' and len(self.coord_graph)<2:
            self.coord_graph.append((self.coord_graph[0][0]-1,self.coord_graph[0][1]))
        
        if self.state == 'right' and len(self.coord_graph)<2:
            self.coord_graph.append((self.coord_graph[0][0]+1,self.coord_graph[0][1]))
    
    
    def width_traversal(self,s):
        traversal = {s:None}
        f = ds.File()
        f.add(s)
        while not f.is_empty():
            s = f.remove()
            for v in mp.maps[0].map_graph.neightboor(s):
                if v not in traversal:
                    f.add(v)
                    traversal[v] = s
        return traversal
     
    
    def collied_pacman(self):
        global nb_ghost_dead
        if pc.pacman.coord_graph[0] in self.coord_graph:
            if not self.can_die:    
                pc.pacman.dead = True
                pc.pacman.rect.move_ip(10*mp.scale_multi-pc.pacman.rect.x , 20*mp.scale_multi-pc.pacman.rect.y)
                pc.pacman.coord_graph=[(10,20)]
                pc.pacman.state = None
                pc.pacman.next_state = None
                pc.pacman.first_move = True
                
                pc.pacman.lifes -= 1
                pc.paclife_sprite.pop()
                pc.paclife_sprites.empty()
                pc.paclife_sprites.add(pc.paclife_sprite)
                
                if pc.pacman.lifes == 0:
                    pc.pacman.gameover = True

                

            else:
                self.rect.move_ip(10*mp.scale_multi-self.rect.x , 12*mp.scale_multi-self.rect.y)
                self.coord_graph = [(10,12)]
                self.state = None

                nb_ghost_dead += 1
                pc.pacman.score += nb_ghost_dead * 250
                
            
                if self.color == 'red':
                    pc.pacman.can_kill_red = False
                    self.image = pg.image.load(r'..\Assets\Sprites\ghost\temp_red_ghost.png')           
                if self.color == 'orange':
                    pc.pacman.can_kill_orange = False
                    self.image = pg.image.load(r'..\Assets\Sprites\ghost\orange_ghost.png')            
                if self.color == 'pink':
                    pc.pacman.can_kill_pink = False
                    self.image = pg.image.load(r'..\Assets\Sprites\ghost\pink_ghost.png')         
                if self.color == 'lightblue':
                    pc.pacman.can_kill_blue = False
                    self.image = pg.image.load(r'..\Assets\Sprites\ghost\light_blue_ghost.png')
                self.image= pg.transform.scale(self.image,(mp.scale_multi,mp.scale_multi))
                
                
                if nb_ghost_dead == 4:
                    nb_ghost_dead = 0

    def new_back_way(self,traversal,end):
        if end not in traversal:
            return self.way
        else:
            way = [None,end]
            s = traversal[end]
            while traversal[s] != None:
                way.append(s)
                s = traversal[s]

            way.append(self.coord_graph[0])
            way.reverse()
            return way
    
            
    def new_way(self,traversal,end):
        if end == self.coord_graph[0] and not pc.pacman.dead :
            return [None]
        
        elif end not in traversal:
            return self.way
        
        else:
            way = [None,pc.pacman.coord_graph[0],end]
            s = traversal[end]
            while traversal[s] != None:
                way.append(s)
                s = traversal[s]

            way.append(self.coord_graph[0])
            way.reverse()
            return way
    
    
    def find_end(self):
        if pc.pacman.coord_graph[0] not in mp.maps[mp.map_i].tp_tile_list:    
            coord = pc.pacman.coord_graph[0]
            block_around_pc =  [[(coord[0],coord[1]-1)],
                [(coord[0]-1,coord[1]),coord,(coord[0]+1,coord[1])],
                                [(coord[0],coord[1]+1)]]
            
            possible_ends = [val for sl in block_around_pc \
                            for val in sl  \
                                if mp.maps[mp.map_i].map_list[val[1]][val[0]] != 'X' \
                                        and mp.maps[mp.map_i].map_list[val[1]][val[0]] != '-' and val != coord]
            return possible_ends[rd.randint(0,len(possible_ends)-1)]
        else:
            return pc.pacman.coord_graph[0]


    def update_way(self,new_way):
        if len(self.coord_graph) == 1:
            self.way = new_way

    
    def update_sprite(self):
        if self.can_die:
            self.image = pg.image.load(r'..\Assets\Sprites\ghost\dark_blue_ghost.png')
        else:
            if self.color == 'red':
                self.image = pg.image.load(r'..\Assets\Sprites\ghost\temp_red_ghost.png')         
            if self.color == 'orange':
                self.image = pg.image.load(r'..\Assets\Sprites\ghost\orange_ghost.png')         
            if self.color == 'pink':
                self.image = pg.image.load(r'..\Assets\Sprites\ghost\pink_ghost.png')            
            if self.color == 'lightblue':
                self.image = pg.image.load(r'..\Assets\Sprites\ghost\light_blue_ghost.png')
        self.image= pg.transform.scale(self.image,(mp.scale_multi,mp.scale_multi))

    
    def can_be_kill(self):
        if self.color == 'red':
            self.can_die = pc.pacman.can_kill_red 
        if self.color == 'orange':
            self.can_die = pc.pacman.can_kill_orange 
        if self.color == 'pink':
            self.can_die = pc.pacman.can_kill_pink
        if self.color == 'lightblue':
            self.can_die = pc.pacman.can_kill_blue 

    
    def reset(self):
        global nb_ghost_start
        global nb_ghost_finish_first_way
        global all_ghost_finished_way
        global time_pause

        if pc.pacman.dead and not pc.pacman.gameover:
            red_ghost.rect.move_ip(10*mp.scale_multi-red_ghost.rect.x , 12*mp.scale_multi-red_ghost.rect.y)
            red_ghost.coord_graph = [(10,12)]
            red_ghost.state = None
            red_ghost.can_start = False
            red_ghost.finish_first_way = False
            red_ghost.way = red_ghost.back_up_start_way.copy()

            pink_ghost.rect.move_ip(10*mp.scale_multi-pink_ghost.rect.x , 12*mp.scale_multi-pink_ghost.rect.y)
            pink_ghost.coord_graph = [(10,12)]
            pink_ghost.state = None
            pink_ghost.can_start = False
            pink_ghost.finish_first_way = False
            pink_ghost.way = pink_ghost.back_up_start_way.copy()
            pink_ghost.time_pause = 0

            orange_ghost.rect.move_ip(10*mp.scale_multi-orange_ghost.rect.x , 12*mp.scale_multi-orange_ghost.rect.y)
            orange_ghost.coord_graph = [(10,12)]
            orange_ghost.state = None
            orange_ghost.can_start = False
            orange_ghost.finish_first_way = False
            orange_ghost.way = orange_ghost.back_up_start_way.copy()

            light_blue_ghost.rect.move_ip(10*mp.scale_multi-light_blue_ghost.rect.x , 12*mp.scale_multi-light_blue_ghost.rect.y)
            light_blue_ghost.coord_graph = [(10,12)]
            light_blue_ghost.state = None
            light_blue_ghost.can_start = False
            light_blue_ghost.finish_first_way = False
            light_blue_ghost.way = light_blue_ghost.back_up_start_way.copy()

            nb_ghost_start = 0
            all_ghost_finished_way = False
            nb_ghost_finish_first_way = False
            time_pause = 0

            pc.pacman.dead = False
            pc.pacman.can_kill_blue = False
            pc.pacman.can_kill_orange = False
            pc.pacman.can_kill_pink = False
            pc.pacman.can_kill_red = False
            pc.pacman.live_time = tm.time()


        elif pc.pacman.dead and pc.pacman.gameover:
            self.rect.move_ip(10*mp.scale_multi-self.rect.x , 12*mp.scale_multi-self.rect.y)
            self.coord_graph = [(10,12)]
            self.state = None
            self.update_way([None])
        

    def big_update_way(self):
        global all_ghost_finished_way
        if not pc.pacman.dead and all_ghost_finished_way:
            if not self.can_die:
                self.update_way(self.new_way(self.width_traversal(self.coord_graph[0]),self.find_end())) 
            else:
                if (self.escape_tile in self.coord_graph) or len(self.way)<=2:
                    self.escape_tile = mp.maps[mp.map_i].accessible_tile[rd.randint(0,len(mp.maps[mp.map_i].accessible_tile))-1]
                self.way = self.new_back_way(self.width_traversal(self.coord_graph[0]),self.escape_tile)

    def start(self):
        global nb_ghost_start
        global time_pause
        if not self.can_start:
            if self.color == 'red' and tm.time() >= pc.pacman.live_time + 1:
                self.can_start = True
                nb_ghost_start += 1
            
            if self.color == 'pink' and tm.time() >= pc.pacman.live_time + 4.5:
                self.can_start = True
                nb_ghost_start += 1

            if self.color == 'orange' and tm.time() >= pc.pacman.live_time + 8:
                self.can_start = True
                nb_ghost_start += 1

            if self.color == 'lightblue' and tm.time() >= pc.pacman.live_time + 11.5:
                self.can_start = True
                nb_ghost_start += 1



    def finish_way(self):
        global nb_ghost_start
        global all_ghost_finished_way
        global nb_ghost_finish_first_way

        if not all_ghost_finished_way:
            if not self.finish_first_way and self.way[2] is None:
                nb_ghost_finish_first_way += 1
                self.finish_first_way = True
            
            elif self.finish_first_way and nb_ghost_finish_first_way != 4:
                if (self.escape_tile in self.coord_graph) or len(self.way)<=2:
                    self.escape_tile = mp.maps[mp.map_i].accessible_tile[rd.randint(0,len(mp.maps[mp.map_i].accessible_tile))-1]
                self.way = self.new_back_way(self.width_traversal(self.coord_graph[0]),self.escape_tile)

        if nb_ghost_finish_first_way == 4:
            all_ghost_finished_way = True

    def in_wall(self):
        if len(self.coord_graph) == 1 and (self.coord_graph[0] == (self.coord_graph[0][0],self.coord_graph[0][1] + 1) or \
                                           self.coord_graph[0] == (self.coord_graph[0][0],self.coord_graph[0][1] - 1)or \
                                            self.coord_graph[0] == (self.coord_graph[0][0]+1,self.coord_graph[0][1]) or \
                                            self.coord_graph[0] == (self.coord_graph[0][0]-1,self.coord_graph[0][1]))  :
            if (self.state == 'right' or self.state == 'left'):
                if not (self.rect.y > self.coord_graph[0][1]*mp.scale_multi and self.rect.y < self.coord_graph[0][1]*mp.scale_multi + mp.scale_multi):
                    self.rect.y = self.coord_graph[0][1]*mp.scale_multi
                    print(1,self.state,self.color)
            
            elif (self.state == 'up' or self.state == 'down'):
                if not (self.rect.x > self.coord_graph[0][0]*mp.scale_multi and self.rect.x < self.coord_graph[0][0]*mp.scale_multi + mp.scale_multi):
                    self.rect.x = self.coord_graph[0][0]*mp.scale_multi
                    print(0,self.state,self.color)


red_ghost = Ghost('red')
orange_ghost = Ghost('orange')
light_blue_ghost = Ghost('lightblue')
pink_ghost = Ghost('pink')

nb_ghost_dead = 0
nb_ghost_start = 0
nb_ghost_finish_first_way = 0
all_ghost_finished_way = False
time_pause = 0