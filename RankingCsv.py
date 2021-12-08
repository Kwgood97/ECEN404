import numpy as np
import pandas as pd
import cv2
import os

coordinates = pd.read_csv('results.csv', index_col=0)
 # x = cv2.imread('predictions.jpg')

# makes col for area so dataframe (objects in image) can be ranked...ranked on area
coordinates['area'] = coordinates['width'] * coordinates['height']

num_objects = len(coordinates)
if num_objects < 5:
  coordinates.drop('area', axis=1, inplace=True)
  coordinates.to_csv('cover.csv')
else:
  coordinates.sort_values(by=['area'], inplace=True, ascending=True)
  obstacles = coordinates.iloc[0:2,:]
  obstacles.to_csv('obstacles.csv')
  cover = coordinates.iloc[2:,:]
  cover.to_csv('cover.csv')

   
# Spatial Density Algorithm was meant to identify thin sparse foilage that would be ranked as cover instead of obstacle...due to change in project due to drone complications the spatial density algorithm is not useful anymore because the new images form the pole flight do not have many objects in the image and also on top of that does not have true objects of cover and obstacles my model was trained on and the spatial density algorithm was designed for and tested for
   #  row, col, _ = image.shape

  #   for i in row:
    #     for j in col:
    #         temp = double(x(i,j))
     #        if (abs(double(x(i,j)) - double(x(i+1,j))) > 25) && (abs(double(x(i,j)) - double(x(i-1,j))) > 25) && (abs(double(x(i,j)) - double(x(i,j-1))) > 25) && (abs(double(x(i,j)) - double(x(i,j+1))) > 25) && (abs(double(x(i,j)) - double(x(i+1,j+1))) > 25) && (abs(double(x(i,j)) - double(x(i+1,j-1))) > 25) && (abs(double(x(i,j)) - double(x(i-1,j+1))) > 25) && (abs(double(x(i,j)) - double(x(i-1,j-1))) > 25):
     #            print("Sparse Cover")

