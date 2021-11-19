# -*- coding: utf-8 -*-
"""
@author: Ken Good
"""

#modules
import time
import csv
import math
import numpy
import serial
import cv2
import os
from PIL import Image


#trip information
#1400 feet forward, then backwards => 2800 feet
#15 min = max flight time
#total flight time = 13 min => 720 seconds
#pace = 2800 / 720 => 3.89 ft per second
#avg walking pace is 4.16 ft per second
#updated due to flight limitations to 500 feet forward
#250 seconds for page of 4 ft per second

#distance in feet (single direction)
Distance_Surveyed = 500
#time in seconds (roundtrip) excluding turn time (turn time is 10 seconds)
Alloted_time = 250
#pace in feet per second * may need factor adjustment if program takes significant processing time
Pace = (Distance_Surveyed * 2 / Alloted_time) * 1


#intake data
#collect data once per foot
Data = numpy.zeros((Distance_Surveyed + 1, 5), dtype = int)
#Image = numpy.zeros((Distance_Surveyed + 1, 5), dtype = int)
Distance_Count = -1

#change com port depending on connection
ser = serial.Serial(
port='COM4',\
baudrate=9600,\
parity=serial.PARITY_NONE,\
stopbits=serial.STOPBITS_ONE,\
bytesize=serial.EIGHTBITS,\
    timeout=0)

Flight = False
StartFlight = input("Type 'Y' and 'Enter' to start: ")
while (Flight == False):
    if StartFlight == 'y' or 'Y':
        Flight = True


#print("connected to: " + ser.portstr)
while (Flight == True):
    time.sleep(1 / Pace)
    Distance_Count += 1
    count=1  
    try:
        while count < 2:
            Record_Data = False
            Data_Line = ""
            Comma_Count = 0
            for line in ser.readline():
                #print(chr(line))
                if chr(line) == "L":
                    Record_Data = True
                if Record_Data == True and (chr(line) != "R") and (chr(line) != "L" and (chr(line) != ",")):
                    Data_Line = Data_Line + str(chr(line))
                if chr(line) == "," and (Comma_Count == 1) and (Record_Data == True):
                    Middle_Sensor = Data_Line
                    Data_Line = ""
                if chr(line) == "," and (Comma_Count == 0) and (Record_Data == True):
                    Left_Sensor = Data_Line
                    Data_Line = ""
                    Comma_Count = 1
                if (chr(line) == "R") and (Record_Data == True):
                    Right_Sensor = Data_Line
                    #print("Distance " + str(Distance_Count) + ": L: " + str(Left_Sensor) + " M: " + str(Middle_Sensor) + " R: " + str(Right_Sensor))
                    Data_Line = ""
                    Record_Data = False     
                    Comma_Count = 0
                    break
                count = count + 1
    except:
        print("crash")
        Left_Sensor = 0
        Middle_Sensor = 0
        Right_Sensor = 0
        ser.close()

    
    #print(Distance_Count)
    if Distance_Count <= Distance_Surveyed:
        Data[Distance_Count][1] = Left_Sensor
        Data[Distance_Count][2] = Middle_Sensor
        Data[Distance_Count][3] = Right_Sensor
    if Distance_Count >= Distance_Surveyed:
        Data[Distance_Surveyed - Distance_Count][0] = Left_Sensor
        Data[Distance_Surveyed - Distance_Count][4] = Right_Sensor

    if (Distance_Count % 200 == 0) and (Distance_Count < Distance_Surveyed):
        print(str(Distance_Count) + " Feet")
    if ((Distance_Surveyed - Distance_Count) < 100) and (Distance_Count % 20 == 0) and (Distance_Count <= Distance_Surveyed):
        print(str(Distance_Count) + " Feet")
        print("prepare to stop")
    if Distance_Count == Distance_Surveyed:
        print("Stop")
        FlightReturn = False
        StartFlight = input("Type 'Y' and 'Enter' to start: ")
        while (FlightReturn == False):
            if StartFlight == 'y' or 'Y':
                FlightReturn = True
        print("Turn and Reach elevation in... \n10")
        time.sleep(1)
        print("9")
        time.sleep(1)
        print("8")
        time.sleep(1)
        print("7")
        time.sleep(1)
        print("6")
        time.sleep(1)
        print("5")
        time.sleep(1)
        print("4")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("Walk") 
    if Distance_Count >= Distance_Surveyed * 2:
        Flight = False
print("Flight complete")
print(Data)

#write data array to usuable excel file
y = "TwoDfile.csv"
finalFile = open(y, 'w', newline = '\n')
write = csv.writer(finalFile)
write.writerows(Data)
finalFile.close()

ser.close()

#function from https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python/46623632#46623632
def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

#VideoPath = input('Please insert MicroSD card \n Enter File Path:')
StartVideoProcess = input('Please insert MicroSD card and type Y when ready: ')
VideoStatus = False
while (VideoStatus == False):
    if StartVideoProcess == 'y' or 'Y':
        VideoStatus = True
listing = os.listdir(r'C:\Users\Ken Good\Documents\TAMU\2021 Fall\404\Video')
ImageCount=1
for vid in listing:
    vid = r"C:\Users\Ken Good\Documents\TAMU\2021 Fall\404\Video\\" +vid
    vidcap = cv2.VideoCapture(vid)
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite("C:\\Users\\Ken Good\\Documents\\TAMU\\2021 Fall\\404\\VideoImages\\Image" + str(ImageCount) + ".jpg", image) # Save frame as JPG file
        return hasFrames
    sec = 0
    frameRate = 2 # Change this number to 1 for each 1 second
    
    success = getFrame(sec)
    while success:
        ImageCount = ImageCount + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)

#image crop
count = 1
while count < ImageCount:
    OriginalImage = Image.open("C:\\Users\\Ken Good\\Documents\\TAMU\\2021 Fall\\404\\VideoImages\\image" + str(count) + ".jpg")
    left = 0
    right = 1920
    top = 300
    bottom = 780
    
    CropImage = OriginalImage.crop((left, top, right, bottom))
    CropImage.save("C:\\Users\\Ken Good\\Documents\\TAMU\\2021 Fall\\404\\VideoImages\\CroppedImage" + str(count) + ".jpg")
    #BlankImage = Image.new("RGB", (780 * ImageCount, 1920))
    if count == 1:
        StitchedImage = Image.open("C:\\Users\\Ken Good\\Documents\\TAMU\\2021 Fall\\404\\VideoImages\\CroppedImage" + str(count) + ".jpg")
        #BlankImage = BlankImage.paste(CropImage, (780 * count,0))
    else:
        StitchedImage = append_images([StitchedImage, CropImage], direction='vertical')
        #BlankImage = BlankImage.paste(CropImage, (780 * count,0))
        #print("StitchedImage")
    count = count + 1
    StitchedImage.save('C:\\Users\\Ken Good\\Documents\\TAMU\\2021 Fall\\404\\VideoImages\\FinalImage.jpg')
StitchedImage.save('C:\\Users\\Ken Good\\Documents\\TAMU\\2021 Fall\\404\\VideoImages\\FinalImage.jpg')
print("Stitching Complete")




#write image array to usuable jpeg file
#z = "DroneImage.jpg"
#DroneImage = open(y, 'w', newline = '\n')
#write = csv.writer(DroneImage)
#write.writerows(Image)





#
#
#       3D Environment Construction
#         (Distance Calculations)
#
#





#
#
#       Gagan's Identification and height application
#
#



#8 foot flyby
#convert test case to drone scan information
#this will not be necessary for actual implementation
#openTestCase = open('TwoDfile.csv', 'r')
#csvReader = csv.reader(openTestCase)
#eightFtTest = list(csvReader)
#above code is now data

#WideData is height expanded upon
WideData = numpy.zeros((Distance_Surveyed, 32), dtype = int)
i = 0
j = 0
while i < Distance_Surveyed:
    while j < 32:
        if (j < 8):
            WideData[i][j] = Data[i][0]
        elif (j < 16):
            WideData[i][j] = Data[i][1]
        elif (j == 16):
            WideData[i][j] = Data[i][2]
        elif j > 16:
            WideData[i][j] = Data[i][3]
        elif (j < 24):
            WideData[i][j] = Data[i][4]
        j += 1
    i += 1

openTestCase = open('TwoDfile.csv', 'r')
csvReader = csv.reader(openTestCase)
TwoDCopy = list(csvReader)

#Line of sight (LOS) determines minimum height of object to be detected at a distance
#below block sets threshold for detection
#eightFtLOS = list(eightFtTest)
eightFtLOS = numpy.zeros((Distance_Surveyed, 32), dtype = int)



i = 0
while i < Distance_Surveyed:
    j = 8
    while (j > 7) and (j < 25):
        #Left Sensor
        if j < 15:
            eightFtLOS[i][j] = (96 /8) * (j - 8)
            
        #Middle Sensor
        elif (j == 16):
            eightFtLOS[i][j] = 0
            
        #Right Sensor
        elif j > 16:
            eightFtLOS[i][j] = 96 - ((96/8) * (j - 16))
        j += 1
    i += 1

i = 0
while i < Distance_Surveyed:
    j = 8
    while (j > 7) and (j < 25):
        #Left Sensor
        if (j < 16) and (int(WideData[i][j]) > int(eightFtLOS[i][j])):
            WideData[i][j] = math.sqrt(2) * (96 - int(eightFtLOS[i][j]))
            
        elif (j < 16) and not(int(WideData[i][j]) > int(eightFtLOS[i][j])):
            WideData[i][j] = 0
            
        #Middle Sensor
        elif (j == 16) and (int(WideData[i][j]) > int(eightFtLOS[i][j])):
            WideData[i][j] = WideData[i][j]

        #Right Sensor
        elif j > 16  and (int(WideData[i][j]) > int(eightFtLOS[i][j])):
            WideData[i][j] = math.sqrt(2) * (96 - int(eightFtLOS[i][j]))
            
        elif (j < 16) and not(int(WideData[i][j]) > int(eightFtLOS[i][j])):
            WideData[i][j] = 0
        j += 1
    i += 1

#write array to usuable excel file
eight = "EightFtTest.csv"
eightFt = open(eight, 'w', newline = '\n')
write = csv.writer(eightFt)
write.writerows(WideData)

#input and claculation

#confirm code has run
print("finished")  
     
#close file
eightFt.close()


#16 foot flyby


#convert test case to drone scan information
#this will not be necessary for actual implementation
#below block sets threshold for detection
sixteenFtTest = list(WideData)

sixteenFtLOS = numpy.zeros((Distance_Surveyed, 32), dtype = int)

i = 0
while i < Distance_Surveyed:
    j = 0
    while (j < 32):
        #Left Sensor
        if j < 8:
            sixteenFtLOS[i][j] = (192 /16) * (j)
            
        #Right Sensor
        elif j > 24:
            sixteenFtLOS[i][j] = 192 - ((192/16) * (j - 16))
        j += 1
    i += 1

i = 0
while i < Distance_Surveyed:
    j = 0
    while (j < 32):
        #Left Sensor
        if (j < 8) and (int(sixteenFtTest[i][j]) > int(sixteenFtLOS[i][j])):
            sixteenFtTest[i][j] = math.sqrt(2) * (192 - int(sixteenFtLOS[i][j]))
            
        elif (j < 8) and not(int(sixteenFtTest[i][j]) > int(sixteenFtLOS[i][j])):
            sixteenFtTest[i][j] = 0
            
        #Right Sensor
        elif ((j > 24) and (j < 32))  and (int(sixteenFtTest[i][j]) > int(sixteenFtLOS[i][j])):
            sixteenFtTest[i][j] = math.sqrt(2) * (192 - int(sixteenFtLOS[i][j]))
            
        elif ((j > 24) and (j < 32))  and not(int(sixteenFtTest[i][j]) > int(sixteenFtLOS[i][j])):
            sixteenFtTest[i][j] = 0
        j += 1
    i += 1

#write array to usuable excel file
sixteen = "sixteenFtTest.csv"
sixteenFt = open(sixteen, 'w', newline = '\n')
write = csv.writer(sixteenFt)
write.writerows(sixteenFtTest)


#grab sensor input (simulated by grabbing points from above data set)
#iterate through data and writes it if it is in los
SensorArray = numpy.zeros((Distance_Surveyed, 5), dtype = int)

#for 8ft pass
i = 0
while i < Distance_Surveyed:
    j = 8
    jLeft = 0
    jRight = 32
    while (j > 7) and (j < 25):
        #Left Sensor
        if (j < 15) and (sixteenFtTest[i][j] != 0) and (j > jLeft):
            SensorArray[i][1] = sixteenFtTest[i][j]
            jLeft = j
            
        #Middle Sensor
        elif (j == 16):
            SensorArray[i][2] = sixteenFtTest[i][j]
            
        #Right Sensor
        elif (j > 16) and (sixteenFtTest[i][j] != 0) and (j < jRight):
            SensorArray[i][3] = sixteenFtTest[i][j]
            jRight = j
        j += 1
    i += 1
    
#for 16ft pass
i = 0
while i < Distance_Surveyed:
    j = 0
    jLeft = 0
    jRight = 32
    while (j < 32):
        #Left Sensor
        if (j < 8) and (sixteenFtTest[i][j] != 0) and (j > jLeft):
            SensorArray[i][0] = sixteenFtTest[i][j]
            jLeft = j
            
        #Right Sensor
        elif (j > 24) and (j < 32) and (sixteenFtTest[i][j] != 0) and (j < jRight):
            SensorArray[i][4] = sixteenFtTest[i][j]
            jRight = j
        j += 1
    i += 1


SensorValues = "SensorInput.csv"
SensorTemp = open(SensorValues, 'w', newline = '\n')
write = csv.writer(SensorTemp)
write.writerows(SensorArray)


#Sensor Data Processing (convert to height and distance)
#Height Array
ObjectHeight  = numpy.zeros((Distance_Surveyed, 5), dtype = int) 
i = 0
while i < Distance_Surveyed:
    j = 0
    while (j < 5):
        if j == 0:
            if SensorArray[i][j] == 0:
                ObjectHeight[i][j] = 0
            else:
                ObjectHeight[i][j] = 192 - (SensorArray[i][j] / math.sqrt(2))
        if j == 1:
            if SensorArray[i][j] == 0:
                ObjectHeight[i][j] = 0
            else:
               ObjectHeight[i][j] = 96 - (SensorArray[i][j] / math.sqrt(2))
        if j == 2:
            ObjectHeight[i][j] = SensorArray[i][j]
        if j == 3:
            if SensorArray[i][j] == 0:
                ObjectHeight[i][j] = 0
            else:
                ObjectHeight[i][j] = 96 - (SensorArray[i][j] / math.sqrt(2))
        if j == 4:
            if SensorArray[i][j] == 0:
                ObjectHeight[i][j] = 0
            else:
                ObjectHeight[i][j] = 192 - (SensorArray[i][j] / math.sqrt(2))
        j += 1
    i += 1
    
ObjHeight = "ObjectHeight.csv"
HeightTemp = open(ObjHeight, 'w', newline = '\n')
write = csv.writer(HeightTemp)
write.writerows(ObjectHeight)

#Distance Array
#Saves distances as coordinate points
#these 5 data points are representative of the actual inputs that will be received
#(one for each sensor per pass)
ObjectDistance  = numpy.zeros((Distance_Surveyed, 5), dtype = int) 
i = 0
while i < Distance_Surveyed:
    j = 0
    while (j < 5):
        if j == 0:
            if SensorArray[i][j] == 0:
                ObjectDistance[i][j] = 0
            else:
                ObjectDistance[i][j] = int (16 - ( (SensorArray[i][j] / math.sqrt(2))) /12)
        if j == 1:
            if SensorArray[i][j] == 0:
                ObjectDistance[i][j] = 0
            else:
               ObjectDistance[i][j] = int (16 - ( (SensorArray[i][j] / math.sqrt(2)))/12)
        if j == 2:
           ObjectDistance[i][j] = 16
        if j == 3:
            if SensorArray[i][j] == 0:
                ObjectDistance[i][j] = 0
            else:
                ObjectDistance[i][j] = int (16 + ((SensorArray[i][j] / math.sqrt(2)))/12)
        if j == 4:
            if SensorArray[i][j] == 0:
                ObjectDistance[i][j] = 0
            else:
                ObjectDistance[i][j] = int(16 +  ((SensorArray[i][j] / math.sqrt(2)))/12)
        j += 1
    i += 1
    
ObjDistance = "ObjectDistance.csv"
DistanceTemp = open(ObjDistance, 'w', newline = '\n')
write = csv.writer(DistanceTemp)
write.writerows(ObjectDistance)


#seperate objects from background with thresholding in 404
#threshold ground (remove objects smaller than 2 feet tall)


#pick out objects from background and 
i = 1
ObjectRow = numpy.zeros((1000), dtype = int) #max area of detectable object is 1000 Square feet
ObjectCol = numpy.zeros((1000), dtype = int)
ObjectArray = numpy.zeros((Distance_Surveyed, 32), dtype = int)
TwoDCopy = list(numpy.float_(TwoDCopy))

#TwoDCopy is assumed simulated data, but in 404 will be inputs from
#image recognition subsystem.
#c = 0
#while c < Distance_Surveyed:
#    d = 0
#    while d < 32:
#        if d < 8:
#            if  (ObjectDistance[c][0] > 0) and (TwoDCopy[c][d] != 0):
#                ObjectArray[c][d]  = ObjectHeight[c][0]
#        if d > 7 and d < 16:
#            if  (ObjectDistance[c][1] > 0) and (TwoDCopy[c][d] != 0):
#                ObjectArray[c][d]  = ObjectHeight[c][1]
#        if d == 16:
#            if  (ObjectDistance[c][2] > 0) and (TwoDCopy[c][d] != 0):
#                ObjectArray[c][d]  = ObjectHeight[c][2]
#        if d > 16 and d < 24:
#            if  (ObjectDistance[c][3] > 0) and (TwoDCopy[c][d] != 0):
#                ObjectArray[c][d]  = ObjectHeight[c][3]
#        if d > 23:
#            if  (ObjectDistance[c][4] > 0) and (TwoDCopy[c][d] != 0):
#                ObjectArray[c][d] = ObjectHeight[c][4]
#        d += 1
#    c += 1

#write array to usuable excel file
ObjectsFinal = "ObjectsFinal.csv"
ObjectTemp = open(ObjectsFinal, 'w', newline = '\n')
write = csv.writer(ObjectTemp)
write.writerows(ObjectArray)

#
#
#       Danny's Pathfinding algorithm
#
#



ObjectTemp.close()
sixteenFt.close()
finalFile.close()
DroneImage.close()
#confirm code has run
print("finished1") 
