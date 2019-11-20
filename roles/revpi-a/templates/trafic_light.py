from state import Light
import time
import revpimodio2

class TraficLight:

    def changeState(self, newState):
        self.state = newState
        self.updateState()

    def updateState(self):
        green  = False
        orange = False
        red    = False
        if(self.state == Light.green):
            green = True
        elif(self.state == Light.orange):
            orange = True
        else:
            red = True
        
        self.revPi.io[self.ioGreen].value  = green
        self.revPi.io[self.ioOrange].value = orange
        self.revPi.io[self.ioRed].value    = red
        #print('Green: ' + str(green) + ' Orange: ' + str(orange) + ' Red: ' + str(red))

    def cleanUp(self):
        self.revPi.io[self.ioGreen].value  = False
        self.revPi.io[self.ioOrange].value = False
        self.revPi.io[self.ioRed].value    = False


    def __init__(self, revPi, ioGreen, ioOrange, ioRed):
        self.waitTimes = [10, 5, 10]
        self.state     = Light.green

        self.revPi     = revPi
        self.ioGreen   = ioGreen
        self.ioOrange  = ioOrange
        self.ioRed     = ioRed
        #self.buzzer    = 'PWM_14'
        #self.buzzer_p  = 'O_13'
