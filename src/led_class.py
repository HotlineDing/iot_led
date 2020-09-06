import socket
import numpy as np



class Led: 
    '''
    Main led driver class. Meant to be a parent class for led devices.
    Maintains a list of led devices used to synchronize and perform complex and cool displays
    '''


    def __init__(self):
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
        self.cm2 = cm.cool
        #PuBu
        self.total_leds = self.height * self.bins
        self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.total_leds).astype(int)]
        self.colors = self.colors[::-1]
        self.beat_colors = [list((255*np.array(self.cm2(i))[:3]).astype(int)) for i in np.linspace(0,255,self.total_leds).astype(int)]
        self.beat_colors = self.beat_colors[::-1]
        self.beat_colors = [[255,0,0]] * self.total_leds
        self.beat_colors2 = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,10).astype(int)]
        self.colors = self.colors[10:] + self.colors[:10]
        self.time_clk = 0

        self.beat_detect = 0 
        self.beat = 0
        self.beat_len = 0
        self.beat_counter = 0
        self.max = 0
        self.energies = [0] * self.total_leds
        self.counter = 0
        self.past_energies = [0] * 20


    def generate_pixels(self):
        if self.time_clk == 50:
            self.time_clk -= 50
            self.colors = self.colors[1:] + self.colors[:1]
        else:
            self.time_clk += 1


        if np.min(self.ear.bin_mean_values) > 0:
            self.energies = 0.225 * self.ear.frequency_bin_energies / self.ear.bin_mean_values
        
        curr = np.round(self.energies[0] * 100, 2)
        self.past_energies = [curr] + self.past_energies[:-1]
       
       

        total_diff = 0
        for i in range(5):
            total_diff += self.past_energies[i] - self.past_energies[i+1]

        if self.beat == 0:
            if total_diff > 30:
                self.beat = 1
        else:
            self.beat_len += 1
            if self.beat_len > 15 or total_diff < -20:
                self.beat = 0
                self.beat_len = 0

        pixels = [round(item*(self.height)) for item in self.energies]
        pixels = pixels[::1]
        #print(pixels[:5])
        #pixels = [max(pixels[i:i+3]) for i in range(0, len(pixels), 3)]
        rgb_leds = []
       

        if self.beat and self.beat_detect:
            colors = self.beat_colors
            if self.beat_counter == 10:
                self.beat_counter = 0
            rgb_leds = self.beat_colors[self.beat_counter] * self.total_leds
            self.beat_counter += 1
            return bytes(rgb_leds)
        else:
            colors = self.colors

        for x in range(self.bins):
            for y in range(self.height):
                n = x*self.height + y
                if x%2==1:
                    y = self.height - 1 - y
                if(y<pixels[x]):
                    rgb_leds.append(colors[n][0])
                    rgb_leds.append(colors[n][1])
                    rgb_leds.append(colors[n][2])
                else:
                    rgb_leds += [0,0,0]



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
        

class Beat(Device):
    def __init__(self, ear, device_type, ip, port, num_leds):
        super().__init__(ear, device_type, ip, port)
        from matplotlib import cm
        import numpy as np
        self.cm = cm.cool
        self.num_leds = num_leds
        self.colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.num_leds).astype(int)]
        self.colors = self.colors[::-1] 
        self.energies = []
        self.samples = 20
        self.past_energy = [0] * self.samples
        self.beat = 0
        self.beat_len = 0

    def generate_pixels(self):
        self.energies = 0.225 * self.ear.frequency_bin_energies / self.ear.bin_mean_values
        self.energies = np.round(self.energies * 100, 2)
        

        curr = self.energies[0]
        self.past_energy = [curr] + self.past_energy[:-1]


        total_diff = 0
        for i in range(5):
            total_diff += self.past_energy[i] - self.past_energy[i+1]

        if self.beat == 0:
            if total_diff > 30:
                self.beat = 1
        else:
            self.beat_len += 1
            if self.beat_len > 15 or total_diff < -20:
                self.beat = 0
                self.beat_len = 0

        rgb_leds = []
        if self.beat == 1:
            for i in range(self.num_leds):
                rgb_leds.append(self.colors[i][0])
                rgb_leds.append(self.colors[i][1])
                rgb_leds.append(self.colors[i][2])
        else:
            rgb_leds = [0,0,0] * self.num_leds
            

        
        return bytes(rgb_leds)


