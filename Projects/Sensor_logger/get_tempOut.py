# Temperature, Humidity, Sound, Light levels with our Raspberry Pi
# Modified by Jan
import time
import grovepi
import datetime
import traceback

# Connection
temperatureSensorIn = 3   # port D3
temperatureSensorOut = 4  # port D4
lightSensor = 0			# port A0
soundSensor = 1			# port A1

global int_lastSound

global float_tempInMax
global float_tempInMin

global float_tempOutMax
global float_tempOutMin

global int_currentHour


def init():
    global int_lastSound
    global float_tempOutMax
    global float_tempInMin

    global float_tempOutMax
    global float_tempOutMin

    global int_currentHour

    try:
        [temp,humidity] = grovepi.dht(temperatureSensorIn,0)
        float_tempOutMax = temp
        float_tempInMin = temp

        [temp,humidity] = grovepi.dht(temperatureSensorOut,1)
        float_tempOutMax = temp
        float_tempOutMin = temp

        int_lastSound  = grovepi.analogRead(soundSensor)

        int_currentHour = datetime.datetime.now().hour

    except:
        error(" init")
        init()

def error(err_message):
    timeNow = datetime.datetime.now()

    writeSingleLineFile("last_error","ERROR" + err_message + "\n")

    writeContFile("logs/log_err_%d_%d_%d.txt" %(timeNow.day,timeNow.month,timeNow.year),
                   timeNow.isoformat() + "   ERROR" + err_message + "\n")


def writeInFile(file ,str_log_write):
    try:

        file.write(str_log_write)
        file.close()
    except IOError:
        raise IOError

def writeContFile(str_fileName, str_toBeWritten):
    try:
        file = open(str_fileName,"a")
        writeInFile(file, str_toBeWritten)

    except IOError:
	print("Contious File ERROR")
	writeContFile(str_fileName, str_toBeWritten)

def writeSingleLineFile(str_fileName ,str_toBeWritten):
      try:

        file = open(str_fileName, "w")
        writeInFile(file, str_toBeWritten)

      except IOError:
        print("Single Line File ERROR")
        writeSingleLineFile(str_fileName ,str_toBeWritten)


def writeMinMax():
    global int_currentHour
    timeNow = datetime.datetime.now()

    if int_currentHour != timeNow.hour:
        int_currentHour = timeNow.hour
        writeContFile("logs/log_%d_%d_%d.txt" %(timeNow.day,timeNow.month,timeNow.year),
                   "HOUR: %d MIN / MAX TEMPS: ||| IN: %.2f / %.2f ||| OUT: %.2f / %.2f \n" %(int_currentHour,float_tempInMin,float_tempOutMax,float_tempOutMin,float_tempOutMax))
        init()

def writeSingleValues(tempIn, tempOut ,humIn ,humOut ,light ,lastSound):
    writeSingleLineFile("values/tempIn", "%.2f" %(tempIn))
    writeSingleLineFile("values/tempOut", "%.2f" %(tempOut))
    writeSingleLineFile("values/humIn", "%d" %(humIn))
    writeSingleLineFile("values/humOut", "%d" %(humOut))
    writeSingleLineFile("values/light", "%d" %(light))
    writeSingleLineFile("values/lastSound", "%d" %(lastSound))


init()

try:

    [temp,humidity] = grovepi.dht(temperatureSensorOut,1)
    tempOut = temp
    print(temp)
except IOError:
    pass
except:
    error(" Running" + traceback.format_exc())
