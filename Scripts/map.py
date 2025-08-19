import pygame as pg
from pygame.sprite import Group
import random as rd
import data_struct as ds

class Map:
    def __init__(self,map:str) -> None:
        self.map_list = self.create_map_list(map)
        self.map_tile_list = []
        self.map_graph = self.create_map_graph(self.map_list)
        self.accessible_tile = [tile for tile in self.map_graph.adj if len(self.map_graph.adj[tile]) != 0 and self.map_list[tile[1]][tile[0]] != '/']
        self.preset_arrived_tile = []
        self.tp_tile_list = []

    def create_map_list(self,map:str) -> list:
        file = open(map)
        
        map_list = []
        for val in file.read().split('\n'):
            map_list.append(list(val))
        file.close()
        
        return map_list

    def create_map_interface(self):
        tile_list = [r'..\bonus\big_pacdot.png',r'..\bonus\litle_pacdot.png',r'..\map_tile\background.png',r'..\map_tile\barrier.png',r'..\map_tile\teleporter.png']
        symbol_list = [ '0','.','/','X','%']
        
        for i in range(len(self.map_list)):
            for j in range(len(self.map_list[i])):
                if self.map_list[i][j] == 'X':
                    map_tile = MapTile(r'..\Assets\Sprites\map_tile\barrier.png')
                
                elif self.map_list[i][j] == '/' or self.map_list[i][j] == '!':
                    map_tile = MapTile(r'..\Assets\Sprites\map_tile\background.png')
                
                elif self.map_list[i][j] == '%':
                    map_tile = MapTile(r'..\Assets\Sprites\map_tile\teleporter.png')
                    self.tp_tile_list.append((j,i))
                
                elif self.map_list[i][j] == '?':
                    rd_tile = rd.randint(0,len(tile_list)-1)
                    map_tile = MapTile(r'..\Assets\Sprites'+tile_list[rd_tile])
                    self.map_list[i][j] = symbol_list[rd_tile]
                
                elif self.map_list[i][j] == '-':
                    map_tile = MapTile(r'..\Assets\Sprites\map_tile\ghost_door_lobby.png')
                
                elif self.map_list[i][j] == '0':
                    map_tile = MapTile(r'..\Assets\Sprites\bonus\big_pacdot.png')
                    self.preset_arrived_tile.append((j,i))
                
                elif self.map_list[i][j] == '.':
                    map_tile = MapTile(r'..\Assets\Sprites\bonus\litle_pacdot.png')
                
                map_tile.rect.move_ip(j*scale_multi,i*scale_multi)
                self.map_tile_list.append(map_tile)      
    
    def create_map_graph(self,map:list)->ds.Graphe:
        map_graph = ds.Graphe()
        for i in range(len(map)):
            for j in range(len(map[i])):
                map_graph.addsummit((j,i))
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] != 'X':
                    if i<len(map)-1 and map[i+1][j]!='X':
                        map_graph.addedge((j,i),(j,i+1))
                    if i>0 and map[i-1][j]!='X':
                        map_graph.addedge((j,i),(j,i-1))
                    if j<len(map[i])-1 and map[i][j+1]!='X':
                        map_graph.addedge((j,i),(j+1,i))
                    if j>0 and map[i][j-1]!='X':
                        map_graph.addedge((j,i),(j-1,i))
                    else:
                        map_graph.addsummit((j,i))
                else:
                    map_graph.addsummit((j,i))
        return map_graph


class MapTile(pg.sprite.Sprite):
    def __init__(self,sprite):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(sprite)
        self.image= pg.transform.scale(self.image,(scale_multi,scale_multi))
        self.rect = self.image.get_rect()

pg.init()
scale = pg.display.get_desktop_sizes()
scale_multi = int((scale[0][1]-90)/27)
maps  = [Map(r'..\Assets\Maps\map1.txt')]  
map_i = 0
tile_map = pg.sprite.RenderPlain(maps[map_i].map_tile_list)

if __name__=='__main__':
    map = Map(r'..\Assets\Maps\map1.txt')
    for l in map.map_list:
        print(l)
    map.map_graph.display()
    print(len(map.preset_arrived_tile))