class Car(object):
    def __init__(self):
        self._ENGINE = Engine()
        self._TRANSMISSION = Transmission()
        

class Engine(object):
    def __init__(self):
        self.__powerCurve = lambda: rpm -> rpm / 100.0
        self._IDLE = 700
        self._FINAL_DRIVE_RATIO = 0.1
        self._REV_LIMIT = 8150
        self._rpm = 0
        
    def start(self):
        self._rpm = self._IDLE

    def increaseSpeed(self):
        self._rpm += self.__powerCurve(self._rpm)

    def decreaseSpeed(self):
        self._rpm -= self.__powerCurve(self._rpm)

    def update(self):
        # TODO: Do something with the rev limiter
        
        
class Transmission(object):
    def __init__(self):
        self._GEAR_RATIOS = [-0.009, 0.0, 0.01, 0.015, 0.017, 0.02, 0.022]
        self._speed = 1

    def _setSpeed(self, speed):
        self._speed = speed % len(self._GEAR_RATIOS)
                    
    def upShift(self):
        self._setSpeed(self._speed + 1)

    def downShift(self):
        self._setSpeed(self._speed - 1)

    def getRatio(self):
        return self._GEAR_RATIOS[self._speed]
