import serial

ser = serial.Serial(
    port='COM4',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
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
                print("Line " + str(count) + ": L: " + str(Left_Sensor) + " M: " + str(Middle_Sensor) + " R: " + str(Right_Sensor))
                Data_Line = ""
                Record_Data = False     
                Comma_Count = 0
                break
            count = count + 1
except:
    print("crash")
    ser.close()

print("Done")
ser.close()


#        for line in ser.readline():
#            print(chr(line))
#            count = count+1

#        for line in ser.readlines():
#            print(line.decode("utf-8"))
#            count = count+1


#import serial
#
#ser = serial.Serial(
#    port='COM4',\
#    baudrate=9600,\
#    parity=serial.PARITY_NONE,\
#    stopbits=serial.STOPBITS_ONE,\
#    bytesize=serial.EIGHTBITS,\
#        timeout=0)
#
#print("connected to: " + ser.portstr)
#count=1
#
#while count <20:
#    try:
#        for line in ser.readline():
#            print(chr(line))
#            count = count+1
#    except:
#        print("crash")
#        ser.close()
#        count = 21
#
#ser.close()
#


# working code 11/6/21 1:49 pm
#import serial
#
#ser = serial.Serial(
#    port='COM4',\
#    baudrate=9600,\
#    parity=serial.PARITY_NONE,\
#    stopbits=serial.STOPBITS_ONE,\
#    bytesize=serial.EIGHTBITS,\
#        timeout=0)
#
#print("connected to: " + ser.portstr)
#count=1
#
#try:
#    while count < 20:
#        Record_Data = False
#        Data_Line = ""
#        for line in ser.readline():
#            if chr(line) == "L":
#                Record_Data = True         
#            if Record_Data == True and (chr(line) != "R") and (chr(line) != "L"):
#                Data_Line = Data_Line + str(chr(line))
#            if chr(line) == "R":
#                print("Line " + str(count) + ": " + Data_Line)
#                Data_Line = ""
#                Record_Data = False          
#            count = count+1
#except:
#    print("crash")
#    ser.close()
#
#ser.close()



