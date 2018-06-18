#!/usr/bin/python
"""
raspiomixHd.py 
Version modifiée de la classe raspiomix.py par Hervé Dugast  v 1.2
Date : 13-01-2017
Ajout de méthodes pour les convertisseurs analogique-numérique
   Méthode retournant le code (17 bits) correspondant à la tension analogique présente en entrée
   Méthode retournant le pourcentage proportionnel à la tension analogique présente en entrée
   Méthode retournant la date au format français, et ajout attributs annee, mois, jour, heures...
"""

class Raspiomix_Base:

    """
    RaspiOMix version 1.0.1
    IO0 = 7
    IO1 = 11
    IO2 = 13
    IO3 = 15

    DIP0 = 12
    DIP1 = 16
    """

    """
    RaspiOMix version 1.1.0
    """

    IO0 = 12
    IO1 = 11
    IO2 = 13
    IO3 = 15

    DIP0 = 7
    DIP1 = 16

    I2C_ADC_ADDRESS = 0x6E
    I2C_ADC0_ADDRESS = I2C_ADC_ADDRESS

    I2C_RTC_ADDRESS = 0x68

    ADC_CHANNELS = [ 0x9C, 0xBC, 0xDC, 0xFC ]
    ADC0_CHANNELS = ADC_CHANNELS

    # RaspiO'Mix+
    I2C_ADC1_ADDRESS = 0x6A
    ADC1_CHANNELS = [ 0xBC, 0x9C, 0xFC, 0xDC ]

    IO4 = 35
    IO5 = 33
    IO6 = 31
    IO7 = 29

    SERIAL_TX = 8
    SERIAL_RX = 10

    DEVICE = '/dev/ttyAMA0'

class RaspiomixHd(Raspiomix_Base):

    i2c = None
    i2c_bus = 0

    ADC_MULTIPLIER = 0.0000386

    def __init__(self):
        import re
        import smbus
        
        # detect i2C port number and assign to i2c_bus
        for line in open('/proc/cpuinfo').readlines():
            m = re.match('(.*?)\s*:\s*(.*)', line)
            if m:
                (name, value) = (m.group(1), m.group(2))
                if name == "Revision":
                    if value [-4:] in ('0002', '0003'):
                        self.i2c_bus = 0
                    else:
                        self.i2c_bus = 1
                    break

        self.i2c = smbus.SMBus(self.i2c_bus);
        self.annee = 17
        self.mois = 1
        self.jour = 13
        self.jourSemNum = 6             # vendredi
        self.jourSemText = "vendredi"   # vendredi
        self.heures = 21
        self.minutes = 41
        self.secondes = 40
        self.strJourDateHeure = "vendredi 13-01-2017 21:41:40"
        self.strDateHeure = "13-01-2017 21:41:40"
        self.strDate = "13-01-2017"
        self.strHeure = "21:41:40"

    def isPlus(self):
        """Detect if board si a RaspiO'Mix+
        """
        try: 
            self.i2c.read_i2c_block_data(self.I2C_ADC1_ADDRESS, 0) 
            return True
        except IOError:
            return False

    def readAdc(self, channels=(0, 1, 2, 3)):
        """Read analog channel
        Retour : tension analogique calculée en volt
        """

        def format(h, m, l):
            # shift bits to product result
            t = ((h & 0b00000001) << 16) | (m << 8) | l
            # check if positive or negative number and invert if needed
            if (h > 128):
                t = ~(0x020000 - t)
            return t * self.ADC_MULTIPLIER

        def read(i2c_address, channel):
            while True:
                data = self.i2c.read_i2c_block_data(i2c_address, channel)
                h, m, l, s = data[0:4]
                if not (s & 128):
                    break
            return format(h, m, l)

        out = []
        for channel in ((channels,) if type(channels) == int else channels):
            i2c_address = self.I2C_ADC0_ADDRESS if channel < 4 else self.I2C_ADC1_ADDRESS
            channel = self.ADC0_CHANNELS[channel] if channel < 4 else self.ADC1_CHANNELS[channel - 4]

            out.append(read(i2c_address, channel))

        return out[0] if type(channels) == int else out

    def readAdcCode(self, channels=(0, 1, 2, 3)):
        """Read analog channel (ajout Hervé Dugast)
        Retourne le code fourni par le CAN (résolution 17 bits), plage de 0 à 131071
        """

        def format(h, m, l):
            # shift bits to product result
            t = ((h & 0b00000001) << 16) | (m << 8) | l
            return t

        def read(i2c_address, channel):
            while True:
                data = self.i2c.read_i2c_block_data(i2c_address, channel)
                h, m, l, s = data[0:4]
                if not (s & 128):
                    break
            return format(h, m, l)

        out = []
        for channel in ((channels,) if type(channels) == int else channels):
            i2c_address = self.I2C_ADC0_ADDRESS if channel < 4 else self.I2C_ADC1_ADDRESS
            channel = self.ADC0_CHANNELS[channel] if channel < 4 else self.ADC1_CHANNELS[channel - 4]

            out.append(read(i2c_address, channel))

        return out[0] if type(channels) == int else out

    def readAdcPourcent(self, channels=(0, 1, 2, 3)):
        """Read analog channel (ajout Hervé Dugast)
        Retourne le code en pourcentage de la pleine échelle (0 à 5V -> 0 à 100%)
        """

        def format(h, m, l):
            # shift bits to product result
            t = ((h & 0b00000001) << 16) | (m << 8) | l
            t = round(t * 25 / 32768)
            return t

        def read(i2c_address, channel):
            while True:
                data = self.i2c.read_i2c_block_data(i2c_address, channel)
                h, m, l, s = data[0:4]
                if not (s & 128):
                    break
            return format(h, m, l)

        out = []
        for channel in ((channels,) if type(channels) == int else channels):
            i2c_address = self.I2C_ADC0_ADDRESS if channel < 4 else self.I2C_ADC1_ADDRESS
            channel = self.ADC0_CHANNELS[channel] if channel < 4 else self.ADC1_CHANNELS[channel - 4]

            out.append(read(i2c_address, channel))

        return out[0] if type(channels) == int else out

    def readRtc(self):
        """Read rtc clock
        """

        try:
            data = self.i2c.read_i2c_block_data(self.I2C_RTC_ADDRESS, 0x00)
        except IOError as e:
            raise IOError(str(e) + " (Maybe rtc_ds1307 module is loaded ?)")

        def bcd_to_int(bcd):
            """2x4bit BCD to integer
            """
            out = 0
            for d in (bcd >> 4, bcd):
                for p in (1, 2, 4 ,8):
                    if d & 1:
                        out += p
                    d >>= 1
                out *= 10
            return out / 10

        data[0] = bcd_to_int(data[0])
        data[1] = bcd_to_int(data[1])

        d = (data[2])
        if (d == 0x64):
            d = 0x40
        data[2] = bcd_to_int(d & 0x3F)

        for i, item in enumerate(data[3:7]):
            data[i + 3] = bcd_to_int(item)

        return '20%02d-%02d-%02dT%02d:%02d:%02d' % (data[6], data[5], data[4], data[2], data[1], data[0])

    def readRtcMem(self):
        """Read rtc clock
        """

        try:
            data = self.i2c.read_i2c_block_data(self.I2C_RTC_ADDRESS, 0x00)
        except IOError as e:
            raise IOError(str(e) + " (Maybe rtc_ds1307 module is loaded ?)")

        def bcd_to_int(bcd):
            """2x4bit BCD to integer
            """
            out = 0
            for d in (bcd >> 4, bcd):
                for p in (1, 2, 4 ,8):
                    if d & 1:
                        out += p
                    d >>= 1
                out *= 10
            return out / 10

        data[0] = bcd_to_int(data[0])
        data[1] = bcd_to_int(data[1])

        d = (data[2])
        if (d == 0x64):
            d = 0x40
        data[2] = bcd_to_int(d & 0x3F)

        for i, item in enumerate(data[3:7]):
            data[i + 3] = bcd_to_int(item)

        self.annee = int(data[6])
        self.mois = int(data[5])
        self.jour = int(data[4])
        self.jourSemNum = int(data[3])
        self.jourSemText = self.getDayTextFr(data[3])
        self.heures = int(data[2])
        self.minutes = int(data[1])
        self.secondes = int(data[0])
        self.strJourDateHeure = '%s %02d-%02d-20%02d %02d:%02d:%02d' % \
                                (self.jourSemText, data[4], data[5], data[6], data[2], \
                                 data[1], data[0])
        self.strDateHeure = '%02d-%02d-20%02d %02d:%02d:%02d' % \
                                (data[4], data[5], data[6], data[2], data[1], data[0])
        self.strDate = '%02d-%02d-20%02d' % (data[4], data[5], data[6])
        self.strHeure = '%02d:%02d:%02d' % (data[2], data[1], data[0])
        
        return self.strJourDateHeure
    
    def getDayTextFr(self, nb):
        """
        Retourne le jour en lettre de la date courante
        """
        switcher = {            # création d'un dictionary mapping
            1: "dimanche",
            2: "lundi",
            3: "mardi",
            4: "mercredi",
            5: "jeudi",
            6: "vendredi",
            7: "samedi",
        }
        return switcher.get(nb, "nothing")

if __name__ == '__main__':
    r = RaspiomixHd()
    print(r.readRtc())
    print(r.readRtcMem())
    print(r.readAdc(0))
    print(r.readAdc((0, 1, 2, 3)))

