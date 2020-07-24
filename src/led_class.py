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
        self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.bins).astype(int)]

    def generate_pixels(self):
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


shape= [[12, 3],
        [14, 2],
        [20, 5],
        [34, 1],
        [15, 4]]
class Cloud(Device):
    def __init__(self, ear, device_type, ip, port, shape):
        super().__init__(ear, device_type, ip, port)
        self.segments = shape
        self.total_leds = sum([x[0] for x in self.segments])
        self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.total_leds).astype(int)]
        self.bins_per_segment = ear.visualizer.n_frequency_bins // len(self.segments)


    def generate_pixels(self):
        pixels = []

        
        return None
