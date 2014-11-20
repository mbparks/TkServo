############################################################################
#Program: TkServo.py
#Language:  Python
#Date:  2014-10-31
#
#Description: Test app to understand I/O functionality of Phidgets.
#Program looks for a Phidget 8/8/8 interface kit and Advanced Servo kit.
#Reads an displays analog input 0 and contract a servo.
#Uses Tkinter to create rudimentary GUI
############################################################################


#Import Python Libraries___________________________________________________
import Tkinter

# Import Phidgets Libraries________________________________________________
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Devices.AdvancedServo import AdvancedServo


#Define GUI parameters____________________________________________________
mywindow = Tkinter.Tk()
mywindow.geometry("300x250")
mywindow.title("Phidget Tester")
positionlabel = Tkinter.Label(mywindow, text = "Servo Position")
sliderLabel = Tkinter.Label(mywindow, text = "Slider Position")


#Define Global Variables__________________________________________________
LED0=Tkinter.IntVar()
LED1=Tkinter.IntVar()


# Function Definitions____________________________________________________
def turnRight():
    global myservoposition
    myservoposition += 10
    try:
        advancedServo.setPosition(0, myservoposition)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Servo at right-most position.")
        myservoposition -= 10
    positionlabeltext = ("Servo Position: %d" % myservoposition)
    positionlabel.configure(text = positionlabeltext)


def turnLeft():
    global myservoposition
    myservoposition -= 10
    try:
        advancedServo.setPosition(0, myservoposition)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Servo at left-most position.")
        myservoposition += 10
    positionlabeltext = ("Servo Position: %d" % myservoposition)
    positionlabel.configure(text = positionlabeltext)

def updateSliderInfo(sliderVal):
        sliderLabelText = ("SliderPosition: %d  " % sliderVal)
        sliderLabel.configure(text = sliderLabelText)

def toggleLED(LEDnum, LEDstatus):
    interfaceKit.setOutputState(LEDnum,LEDstatus)

def exitProgram():
    print("Closing Phidgets...")
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    try:
        advancedServo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Program successfully shutdown.  Goodbye.")
    exit(0)





def interfaceKitAttached(e):
    attached = e.device
    print("InterfaceKit %i Attached!" % (attached.getSerialNum()))


def interfaceKitDetached(e):
    detached = e.device
    print("InterfaceKit %i Detached!" % (detached.getSerialNum()))


def interfaceKitError(e):
    try:
        source = e.device
        print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))


def interfaceKitInputChanged(e):
    source = e.device
    print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))


def interfaceKitSensorChanged(e):
    source = e.device
    print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))
    if e.index == 0:
        updateSliderInfo(e.value)


def interfaceKitOutputChanged(e):
    source = e.device
    print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))





#Create and Initialize AdvancedServo object_______________________
print("Initialzing Servo...")
try:
    advancedServo = AdvancedServo()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

try:
    advancedServo.openPhidget()
    advancedServo.waitForAttach(10000)
    advancedServo.setEngaged(0, True)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        advancedServo.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

myservoposition = 0
advancedServo.setPosition(0, 0)
print("Servo initialized.")



#Create  an initialize an interfacekit object_______________________
print("Initialzing Interface Kit...")
try:
    interfaceKit = InterfaceKit()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

try:
    interfaceKit.setOnAttachHandler(interfaceKitAttached)
    interfaceKit.setOnDetachHandler(interfaceKitDetached)
    interfaceKit.setOnErrorhandler(interfaceKitError)
    interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
    interfaceKit.setOnOutputChangeHandler(interfaceKitOutputChanged)
    interfaceKit.setOnSensorChangeHandler(interfaceKitSensorChanged)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:
    interfaceKit.openPhidget()
    interfaceKit.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    print("Interface Kit initialized.")
    print("Ready to go!")



#Main________________________________________________________
def main():
    checkbox_0 = Tkinter.Checkbutton(mywindow, text='LED0', variable=LED0, command=lambda: toggleLED(0,LED0.get()))
    checkbox_0.place(x=5, y=5)

    checkbox_1 = Tkinter.Checkbutton(mywindow, text='LED1', variable=LED1, command=lambda: toggleLED(1,LED1.get()))
    checkbox_1.place(x=5, y=30)

    leftButton = Tkinter.Button(mywindow, text="Turn Left", command=turnLeft)
    leftButton.place(x=50, y= 150)

    rightButton = Tkinter.Button(mywindow, text="Turn Right", command=turnRight)
    rightButton.place(x=150, y= 150)

    exitButton = Tkinter.Button(mywindow, text="Exit", command=exitProgram)
    exitButton.place(x=235, y= 200)

    positionlabel.place(x=100, y=120)
    sliderLabel.place(x=150, y=5)
                            
    mywindow.mainloop()

if __name__ == '__main__':
    main()