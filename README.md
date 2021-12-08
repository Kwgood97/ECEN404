# ECEN404
ECEN 404-902 Group 22 Senior Design

The integrated system was successful, with the drone mounted system feeding the data collected on the field to the environment subsystem. The data is then processed by the environment subsystem, where an image of the environment is created and fed to both the machine learning and pathfinding subsytems. The machine learning subsystem takes the information from the environment subsystem, namely the image, and runs its model on this image to find points of interest to work with. These points are then exported to a CSV that is process and fed to the pathfinding subsystem. The pathfinding subsystem takes both the image from the environment subsystem and the points of interest from the machine learning subsystems, and places markers over the points of interest as well as uses the image fed in from the environment subsystem as the background image to display. Image 5, provided below, demonstrates the final GUI output from this project. While the image is difficult to make out due to the small dimensions of this report, the final output image can be found in the Github repo titled “final_integrated.png”.


Files of note include -
1. ReportCode.py - Represents integration of Bingcheng, Ken, and Danny's subsystems
2. FinalArduino.ino - Arduino code that transimits the three sensors data
3. Pathfinding.py - Pathfinding Subsystem code
4. GaganMock.py - File to translate CSV to list objects that can be utilized in the pathfinding subsystem
5. final_integrated.png - Final output image from runnning integrated systems
6. coverplanneryolov4_training (2).py - Code of Yolov4 Model 
7. JSONtoCSV.py - Converts JSON file of predictions from Yolov4 Model to CSV file
8. RankingCSV.py - Converts CSV file to dataframe to rank the bounded boxes of the objects of the image for the strength of the cover from greatest to least
9. DroneImageDetection - JPG file of detections of the model on an image that replicates the Drone Path Flight
10. PoleFlightImage1 - JPG file of dtections of the model from the Pole Flight Test
11. PoleFlightImage2 - JPG file of dtections of the model from the Pole Flight Test

