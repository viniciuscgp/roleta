import pygame, sys
from pygame.locals import *
import random
from  roullete import Roulette
from roullete import RouletteState
from button import Button
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
 
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
surface.fill(WHITE)
pygame.display.set_caption("Na Rede - Roleta")

roulette = None

def create_another_roulette():
    global roulette
    roulette = Roulette(x=SCREEN_WIDTH / 2, 
                        y=SCREEN_HEIGHT / 2, 
                        radius=250, 
                        initial_power= random.uniform(2, 5), 
                        handle_image_path="assets/handle.png",
                        background_image_path="assets/roleta2.png")



# Create the button
def start_roulette():
    if roulette.state == RouletteState.STOPPED:
        roulette.reset(new_power=random.uniform(2, 5))

font = pygame.font.SysFont(None, 28)
start_button = Button(x=SCREEN_WIDTH // 2 - 100, 
                      y=SCREEN_HEIGHT - 100, 
                      width=200, 
                      height=50, 
                      text="Rodar a Roleta", 
                      font=font, 
                      bg_color=RED, 
                      text_color=WHITE, 
                      action=create_another_roulette)


create_another_roulette()
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            create_another_roulette();
        start_button.handle_event(event)     

    roulette.update()
     
    surface.fill(WHITE)
    roulette.draw(surface)
    start_button.draw(surface) 
         
    pygame.display.update()
    FramePerSec.tick(FPS)

    