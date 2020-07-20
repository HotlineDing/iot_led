import numpy as np




class Leds:
    """
    Class representing the led array that will drive the leds.
    """

    def __init__(self, display_type='ARRAY', ear=None):
        self.display_type = display_type
        self.ear = ear
        self.leds = []

        if self.display_type=='ARRAY':
            from matplotlib import cm
            self.height = 15 
            self.bins = 10
            self.cm = cm.hsv 
            self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.bins).astype(int)]

        if self.display_type=='CLOUD':
            self.segments = []

    


    def generate_pixels_array(self):
        pixels = [round((item[3]/500)*(self.height))-1 for item in self.ear.fast_bars]
        pixels = pixels[::-1]
        pixels = pixels[::1]
        #pixels = [max(pixels[i:i+3]) for i in range(0, len(pixels), 3)]
        rgb_leds = []
        for x in range(self.bins):
            for y in range(self.height):
                if x%2==1:
                    y = self.height - 1 - y
                if(y<pixels[x]):
                    rgb_leds.append(self.colors[x][0])
                    rgb_leds.append(self.colors[x][1])
                    rgb_leds.append(self.colors[x][2])
                else:
                    rgb_leds += [0,0,0]


        rgb_leds = bytes(rgb_leds)
        return rgb_leds


    def generate_pixels(self):
        if self.display_type=='ARRAY': return self.generate_pixels_array()
        if self.display_type=='CLOUD': return self.generate_pixels_cloud()
