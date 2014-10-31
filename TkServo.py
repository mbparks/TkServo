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
mywindow.geometry("300x400")
positionlabel = Tkinter.Label(mywindow, text = "Servo Position")
sliderLabel = Tkinter.Label(mywindow, text = "Slider Position")


# Function Definitions_______________________________________________________
def turnup():
    global myservoposition
    myservoposition += 10
    try:
        advancedServo.setPosition(0, myservoposition)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Servo at maximum position.")
        myservoposition -= 10
    positionlabeltext = ("Servo Position: %d" % myservoposition)
    positionlabel.configure(text = positionlabeltext)


def turndown():
    global myservoposition
    myservoposition -= 10
    try:
        advancedServo.setPosition(0, myservoposition)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Servo at minimum position.")
        myservoposition += 10
    positionlabeltext = ("Servo Position: %d" % myservoposition)
    positionlabel.configure(text = positionlabeltext)


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


def updateSliderInfo(sliderVal):
        sliderLabelText = ("SliderPosition: %d" % sliderVal)
        sliderLabel.configure(text = sliderLabelText)



#Setup______________________________________________________________

#Create a AdvancedServo object___
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

#Initialize servo
myservoposition = 0
advancedServo.setPosition(0, 0)
print("Servo initialized.")



#Create an interfacekit object____
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

upbutton = Tkinter.Button(mywindow, text="Up", command=turnup)
downbutton = Tkinter.Button(mywindow, text="Down", command=turndown)
exitButton = Tkinter.Button(mywindow, text="Exit", command=exitProgram)

upbutton.pack(padx=10,pady=20)
downbutton.pack(padx=10,pady=20)
positionlabel.pack(padx=10,pady=20)
sliderLabel.pack(padx=10,pady=20)
exitButton.pack(padx=10,pady=20)
                            
mywindow.mainloop()
