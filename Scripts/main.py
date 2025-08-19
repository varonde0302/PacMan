import pygame as pg
import map as mp
import pacman as pc
import ghost as go
import time as tm
import random as rd

first_init = True
map = mp.maps[mp.map_i]

pg.init()
screen = pg.display.set_mode((len(map.map_list[0])*mp.scale_multi, len(map.map_list)*mp.scale_multi))
pg.display.set_caption('PacMan')
pg.display.set_icon(pg.image.load(r'..\Assets\Sprites\pacman\pacman_right.png'))

map.create_map_interface()

pacman = pc.pacman
red_ghost = go.red_ghost
random_ip = rd.randint(0,len(mp.maps[mp.map_i].preset_arrived_tile)-1)
red_ghost.back_up_start_way= red_ghost.new_way(red_ghost.width_traversal(red_ghost.coord_graph[0]),mp.maps[mp.map_i].preset_arrived_tile[random_ip])
red_ghost.way = red_ghost.back_up_start_way.copy()
mp.maps[mp.map_i].preset_arrived_tile.pop(random_ip)

orange_ghost = go.orange_ghost
random_ip = rd.randint(0,len(mp.maps[mp.map_i].preset_arrived_tile)-1)
orange_ghost.back_up_start_way = orange_ghost.new_way(orange_ghost.width_traversal(orange_ghost.coord_graph[0]),mp.maps[mp.map_i].preset_arrived_tile[random_ip])
orange_ghost.way = orange_ghost.back_up_start_way.copy()
mp.maps[mp.map_i].preset_arrived_tile.pop(random_ip)

pink_ghost = go.pink_ghost
random_ip = rd.randint(0,len(mp.maps[mp.map_i].preset_arrived_tile)-1)
pink_ghost.back_up_start_way = pink_ghost.new_way(pink_ghost.width_traversal(pink_ghost.coord_graph[0]),mp.maps[mp.map_i].preset_arrived_tile[random_ip])
pink_ghost.way = pink_ghost.back_up_start_way.copy()
mp.maps[mp.map_i].preset_arrived_tile.pop(random_ip)

light_blue_ghost = go.light_blue_ghost
random_ip = rd.randint(0,len(mp.maps[mp.map_i].preset_arrived_tile)-1)
light_blue_ghost.back_up_start_way = red_ghost.new_way(light_blue_ghost.width_traversal(light_blue_ghost.coord_graph[0]),mp.maps[mp.map_i].preset_arrived_tile[random_ip])
light_blue_ghost.way = light_blue_ghost.back_up_start_way.copy()
mp.maps[mp.map_i].preset_arrived_tile.pop(random_ip)

pac_sprite = pg.sprite.RenderPlain(pacman,red_ghost,orange_ghost,pink_ghost,light_blue_ghost)

clock = pg.time.Clock()
pause = False

running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and not pc.pacman.gameover and not pause:
                pacman.next_state = 'up'
            
            if event.key == pg.K_DOWN and not pc.pacman.gameover and not pause:
                pacman.next_state = 'down'
                
            if event.key == pg.K_LEFT and not pc.pacman.gameover and not pause:
                pacman.next_state = 'left'

            if event.key == pg.K_RIGHT and not pc.pacman.gameover and not pause:
                pacman.next_state = 'right'   
            
            if event.key == pg.K_ESCAPE and not pc.pacman.gameover:
                pause = not pause
                if not pause:
                    pc.pacman.live_time += tm.time()-start_pause_time
                else:
                    start_pause_time = tm.time()

    if not pc.pacman.gameover and not pause:          
        pacman.update()
        
        red_ghost.update()
        orange_ghost.update()
        light_blue_ghost.update()
        pink_ghost.update()
    
    mp.tile_map.draw(screen)
    pac_sprite.draw(screen)
    pc.paclife_sprites.draw(screen)

    score_label = pg.font.Font(None,1*mp.scale_multi).render('score',1,(255,255,90))
    score_text = pg.font.Font(None,1*mp.scale_multi).render(str(pacman.score),1,(255,255,90))
    screen.blit(score_label,(1.25*mp.scale_multi,10*mp.scale_multi))
    screen.blit(score_text,(0.9*mp.scale_multi,11*mp.scale_multi))
    
    if pc.pacman.gameover:
        gameover_text = pg.font.Font(None,1*mp.scale_multi).render('GAME OVER',1,(255,0,0))
        screen.blit(gameover_text,(8.5*mp.scale_multi,15.20*mp.scale_multi))

    if pause:
        pause_text = pg.font.Font(None,1*mp.scale_multi).render('PAUSE',1,(255,255,0))
        screen.blit(pause_text,(9.4*mp.scale_multi,15.20*mp.scale_multi))

    
    
    pg.display.flip()
    clock.tick(80)
    first_init = False
pg.quit()
