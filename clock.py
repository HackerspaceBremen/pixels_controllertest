import pygame, led, sys, os, random, csv
import smbus
from pygame.locals import *

""" A very simple arcade shooter demo :)
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

adress = 0x48
LM75 = smbus.SMBus(1)

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialport = sys.argv[ 1 ]
    print "INITIALIZING WITH USB-PORT: "+serialport
    ledDisplay = led.dsclient.DisplayServerClientDisplay(serialport, 8123)
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.dsclient.DisplayServerClientDisplay("localhost", 8123)

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 0 #1=alive; 0=dead


def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    global gamestate

    scored = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pass
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_LEFT:
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_SPACE:
                    if gamestate == 0:
                        pass
                        scored = False

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    pass

        screen.fill(BLACK)
        font = pygame.font.Font(None, 16)
        text1 = font.render("Game over", 0, RED)
        text1pos = text1.get_rect()
        text1pos.midtop = (screen.get_rect().centerx, -1)
        screen.blit(text1,text1pos)
        text2 = font.render("Score: "+str(LM75.read_byte(adress)), 0, GREEN)
        text2pos = text2.get_rect()
        text2pos.midbottom = (screen.get_rect().centerx, 21)
        screen.blit(text2,text2pos)

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
