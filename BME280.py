import smbus2
import bme280
from csv import writer
from datetime import datetime

#smbus2 is the package that allows the pi to talk to the bus
#this was added by using the terminal and typing 'sudo pip3 install smbus2
#bme280 is the driver for my environmental sensor
#this was added by using the terminal and typing 'sudo pip3 install bme280'
#csv allows us to easily edit our csv file
#datetime allows us to easily get and format the current date and time

#creates a connection to the sensor by assigning the port and address then calling SMBus()
#I remoted into my pi by using RDP in windows and xrdp
#this was installed by using the terminal and running 'sudo apt install xrdp'
#As a heads up, you must allow i2c connections which I did by going to START>PREFERENCES>RASPBERRY PI CONFIGURATION>INTERFACES and selecting the enable button beside I2C
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

#this will actually get the data by using the bus, address, and calibration parameters
data = bme280.sample(bus, address, calibration_params)

#Get and convert data to imperial units
def getValues():
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%m/%d/%y %H:%M:%S")
    temperatureF = data.temperature * (9/5) + 32
    pressure_mmHg = (data.pressure / 3386) * 100
    humidityPercentage = data.humidity
    dataList = [timestamp,'%.f'%temperatureF,'%.2f'%pressure_mmHg,'%.f'%humidityPercentage + "%"]
    return dataList

#writes to the csv
def manageFile(dataList):
    with open('records.csv', 'a+', newline='') as write_obj:
        write_obj.seek(0)
        line = write_obj.readline().strip()
        header = ["Timestamp","Temperature (F)","Pressure (mmHg)","Humidity (%)"]
        headerString = ','.join(header)
        csv_writer = writer(write_obj)
        if line == headerString: #if the first line includes the header, just write the data list
            csv_writer.writerow(dataList)
        else: #if the first line does not include the header, write the header then data list
            csv_writer.writerow(header)
            csv_writer.writerow(dataList)

#get the values
dataList = getValues()
#call the file manager
manageFile(dataList)