import numpy as np
import socket


class Leds:
    """
    Class representing the led array that will drive the leds.
    """


    def __init__(self, visualizer=None, bins=10, height=15):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.visualizer = visualizer
        self.height = height
        self.bins = bins

        self.colors = visualizer.slow_bar_colors
        self.colors = self.colors[::-1]


    def generate_pixels(self):
        self.pixels = [round((item[3]/500)*(self.height))-1 for item in self.visualizer.fast_bars]
        #self.pixels = self.pixels[::-3]
        self.pixels = self.pixels[::-1]
        #self.pixels = [max(self.pixels[i:i+3]) for i in range(0, len(self.pixels), 3)]
        self.pixels = self.pixels[::1]
        rgb_leds = []
        for x in range(self.bins):
            for y in range(self.height):
                if x%2==1:
                    rgb_leds.append((x+1)*self.height-y-1)
                else:
                    rgb_leds.append(x*self.height+y)
                if(y<self.pixels[x]):
                    rgb_leds.append(self.colors[x][0])
                    rgb_leds.append(self.colors[x][1])
                    rgb_leds.append(self.colors[x][2])
                else:
                    rgb_leds.append(0)
                    rgb_leds.append(0)
                    rgb_leds.append(0)

        #print([round(item[1]) for item in self.visualizer.slow_bars])
        #print(self.pixels[::-1])
        #rgb_leds = rgb_leds[::-1]
        rgb_leds = bytes(rgb_leds)
        self.sock.sendto(rgb_leds, ('192.168.0.150',7777))
