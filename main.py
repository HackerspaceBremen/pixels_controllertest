#######################################
# Code coded by Mike Doty
#
# If you want trackball checking, you will
# have to code it yourself.  Sorry!
#
# Oh, and it just grabs the first joystick.
#   Yes, that makes me lazy.
#
# Released February 8, 2008.
#######################################
import pygame, led, sys, os, random, csv 
from pygame.locals import *

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0) 
class App:
    def __init__(self):
 
	
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
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Joystick Analyzer")
 
        # Set up the joystick
        pygame.joystick.init()
 
        self.my_joystick = None
        self.joystick_names = []
 
        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())
 
        print self.joystick_names
 
        # By default, load the first available joystick.
        if (len(self.joystick_names) > 0):
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()
 
        max_joy = max(self.my_joystick.get_numaxes(), 
                      self.my_joystick.get_numbuttons())

        self.simDisplay = simDisplay
        self.ledDisplay = ledDisplay
        self.screen = screen
 
        self.font = pygame.font.Font(None, 14)
 
    # A couple of joystick functions...
    def check_axis(self, p_axis):
        if (self.my_joystick):
            if (p_axis < self.my_joystick.get_numaxes()):
                return self.my_joystick.get_axis(p_axis)
 
        return 0
 
    def check_button(self, p_button):
        if (self.my_joystick):
            if (p_button < self.my_joystick.get_numbuttons()):
                return self.my_joystick.get_button(p_button)
 
        return False
 
    def draw_text(self, text, x, y, color, align_right=False):
        
        surface = self.font.render(text, True,color)
        #surface.set_colorkey( (0, 0, 0) )
 	surfacePos = surface.get_rect()
	surfacePos.topleft = ( x , y )
        self.screen.blit(surface, surfacePos);
 
    def center_text(self, text, x, y, color):
        surface = self.font.render(text, True,color)
        #surface.set_colorkey( (0, 0, 0) )
 
        self.screen.blit(surface, (x - surface.get_width() / 2, 
                                   y - surface.get_height() / 2))
 
    def main(self):
        while (True):
            self.g_keys = pygame.event.get()
 
            self.screen.fill(0)
 
            for event in self.g_keys:
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.quit()
                    return
 
                elif (event.type == QUIT):
                    self.quit()
                    return
 
            #self.draw_text("Joystick Name:  %s" % self.joystick_names[0], 
                           #5, 5, (0, 255, 0))
 
            self.draw_text("Axes (%d)" % self.my_joystick.get_numaxes(), 
                           0, 0, (255, 255, 255))
 
            for i in range(0, self.my_joystick.get_numaxes()):
                #if(self.my_joystick.get_axis(i)):
                #    pygame.draw.circle(self.screen, (0, 0, 200), 
                #                       (10 + (i * 10), 20), 1, 0)
                #else:
                #    pygame.draw.circle(self.screen, (255, 0, 0), 
                #                      (10 + (i * 10), 20), 5, 0)
		value = self.my_joystick.get_axis(i)
 		if(value > 0):
                    self.draw_text("%d" % i, (i * 10), 10, (GREEN))
                elif(value == 0):
                    self.draw_text("%d" % i, (i * 10), 10, (WHITE))
                elif(value < 0):
                    self.draw_text("%d" % i, (i * 10), 10, (RED))
                

            self.draw_text("Buttons (%d)" % self.my_joystick.get_numbuttons(), 
                           37, 0, (255, 255, 255))
 
            for i in range(0, self.my_joystick.get_numbuttons()):
                #if(self.my_joystick.get_button(i)):
                #    pygame.draw.circle(self.screen, (0, 0, 200), 
                #                       (20 + (i * 10), 20), 10, 0)
                #else:
                #    pygame.draw.circle(self.screen, (255, 0, 0), 
                #                      (20 + (i * 10), 20), 10, 0)
                value = self.my_joystick.get_button(i)
                if(value == 1):
                    self.draw_text("%d" % i, 37 + (i * 6), 10, (GREEN))
                elif(value == 0):
                    self.draw_text("%d" % i, 37 + (i * 6), 10, (WHITE))
                
 
            self.simDisplay.update(self.screen)
            self.ledDisplay.update(self.screen)
 
    def quit(self):
        pygame.display.quit()
 
app = App()
app.main()
