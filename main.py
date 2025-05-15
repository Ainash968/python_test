import random
from pathlib import Path

import dead as dead
import pygame as pg

pg.init()

WIDTH=720
HEIGHT=480

WHITE=(255,255,255)
RED=(240,0,0)
GREEN=(0,240,0)

BG_COLOR=WHITE
size = (WIDTH, HEIGHT)

def load_animation(path, base_filename, count, image=None):
  animation=[]#хранилище кадров
  for i in range(1,count):
    image=pg.image.load(Path(f"{path}/{base_filename}{i}.png"))
    image=pg.transform.scale2x(image)
    animation.append(image)
  return animation

def get_next_frame(animation,game_frame):
  animation_frame=animation[game_frame % len(animation)-1]
  return animation_frame

def go_center(surface):
    rect=surface.get_rect()
    rect.center=WIDTH // 2,HEIGHT // 2
    return rect

screen = pg.display.set_mode(size)
pg.display.set_caption("window")

fps = 10
clock = pg.time.Clock()

frame = 0
click = False
game_over = False

font=pg.font.Font('assets/3d-thirteen-pixel-fonts.otf',WIDTH//6)
game_over_text=font.render('GAME OVER!',True,RED)
win_text=font.render('YOU WIN!',True,GREEN)

win_text_rect=go_center(win_text)
game_over_text_rect=go_center(game_over_text)

duck_animation = load_animation("assets", "duck", 4)
duck_image = get_next_frame(duck_animation, frame)

ducks=[]
for _ in range(10):
    duck_rect=duck_image.get_rect()
    duck_rect.left=WIDTH+random.randint(0,WIDTH)
    duck_rect.bottom=HEIGHT-random.randint(0,HEIGHT-100)
    ducks.append(duck_rect)

runGame = True
while runGame:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            runGame = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                click = False


    duck_image = get_next_frame(duck_animation, frame)
    # Рендеринг
    screen.fill(BG_COLOR)
    cursor_position=pg.mouse.get_pos()
    for dead,duck in enumerate(ducks):
        duck.x = random.randint(20,80)
        screen.blit(duck_image, duck)
        if duck.collidepoint(cursor_position) and click:
                ducks.pop(dead)
                click = False
        if duck.right < 0:
            game_over = True
    if not ducks:
        screen.blit(win_text,win_text_rect)
    if game_over:
        screen.blit(game_over_text,game_over_text_rect)

    # после отрисовки всего, переворачиваем экран
    pg.display.flip()
    clock.tick(fps)
    frame += 1
pg.quit()
