import spidev

class MCP3008:    

    def __init__(self, device = 0):
            self.device = device
            self.spi = spidev.SpiDev()
            self.create()
            self.spi.max_speed_hz = 1000000 

    #create the MCP3008 Devices (0 or 1) on Bus 0
    def create(self):
        self.spi.open(0, self.device)
        self.spi.max_speed_hz = 1000000
        
    #read Data from the specific channel (0-7)
    def readData(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    #close the device
    def close(self):
        self.spi.close()
