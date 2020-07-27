import socket
import numpy as np



class Led: 
    '''
    Main led driver class. Meant to be a parent class for led devices.
    Maintains a list of led devices used to synchronize and perform complex and cool displays
    '''


    def __init__(self, ear):
        self.ear = ear
        self.devices = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def add_device(self, device):
        self.devices.append(device)

    def update(self):
        for device in self.devices:
            leds = device.generate_pixels()
            self.sock.sendto(leds, (device.ip, device.port))


class Device:
    def __init__(self, ear, device_type, ip, port):
        self.ear = ear
        self.device_type = device_type
        self.ip = ip
        self.port = port
    
    def generate_pixels(self):
        return None


class Array(Device):
    def __init__(self, ear, device_type, ip, port, bins, height):
        super().__init__(ear, device_type, ip, port)
        from matplotlib import cm
        self.bins = bins
        self.height = height
        self.cm = cm.hsv
        #PuBu
        self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.bins*self.height).astype(int)]
        self.colors = self.colors[::-1]
        self.colors = self.colors[10:] + self.colors[:10]

    def generate_pixels(self):
        pixels = [round((item[3]/500)*(self.height))-1 for item in self.ear.fast_bars]
        pixels = pixels[::-1]
        pixels = pixels[::2]
        #pixels = [max(pixels[i:i+3]) for i in range(0, len(pixels), 3)]
        rgb_leds = []
        for x in range(self.bins):
            for y in range(self.height):
                n = x*self.height + y
                if x%2==1:
                    y = self.height - 1 - y
                if(y<pixels[x]):
                    rgb_leds.append(self.colors[n][0])
                    rgb_leds.append(self.colors[n][1])
                    rgb_leds.append(self.colors[n][2])
                else:
                    rgb_leds += [0,0,0]

        #rgb_leds = rgb_leds[::-1]
        #rgb_leds = 


        rgb_leds = bytes(rgb_leds)
        return rgb_leds


class Cloud(Device):
    def __init__(self, ear, device_type, ip, port, shape):
        from matplotlib import cm
        super().__init__(ear, device_type, ip, port)
        self.frequency_bins = len(ear.fast_bars)
        self.segments = shape
        self.total_leds = sum([x[0] for x in self.segments])
        self.cm = cm.hsv
        self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,500).astype(int)]
        self.bins_per_segment = self.frequency_bins // len(self.segments)
        self.mode = 'Demo2'
        self.flag = 1
        print(self.total_leds)
        self.rgb_leds = []
        for i in range(40):
            self.rgb_leds.append(self.colors[i][0])
            self.rgb_leds.append(self.colors[i][1])
            self.rgb_leds.append(self.colors[i][2])
        for i in range(self.total_leds-40):
            self.rgb_leds += [0,0,0]
        self.counter = 0
        self.counter2 = 0


    def generate_pixels(self):
        if self.mode == 'Demo':
            if self.counter == 10:
                self.rgb_leds = self.rgb_leds[3:] + self.rgb_leds[:3]
                self.counter -= 10
            self.counter += 1 
        if self.mode == 'Demo2':
            if self.counter == 20:
                self.counter -= 20
                self.rgb_leds = []
                self.counter2 += 1
                for i in range(self.total_leds):
                    if self.counter2 == len(self.colors):
                        self.counter2 -= len(self.colors)
                    self.rgb_leds.append(self.colors[self.counter2][0])
                    self.rgb_leds.append(self.colors[self.counter2][1])
                    self.rgb_leds.append(self.colors[self.counter2][2])
            self.counter += 1
            #for i in range(300-self.total_leds):
            #    rgb_leds += [0,0,0]
        #else:        
        #    for i in range(len(segments)):
        #        frequency_bins = self.ear.fast_bars[self.bins_per_segment * (self.segments[i][1]-1) : (self.bins_per_segment+1) * (self.segments[i][1]-1)]
        #        num_activated = max(frequency_bins)/500 * self.segments[i][0] - 1

        
        ret = bytes(self.rgb_leds)
        return ret
        

        

