import json
import csv

with open(result (9).json') as file:
  jsonData = json.load(file)

objects = jsonData[0]['objects']
columnNames = ['center_x', 'center_y', 'width', 'height']
rows = []
for object in objects:
  relative_coordinates = object['relative_coordinates']
  row = list(relative_coordinates.values())
  rows.append(row)

#name of csv file
filename = "results.csv"

# writing to a csv file
with open('/content/drive/MyDrive/results.csv', "w") as csvfile:
  #creating a csv writer object
  csvwriter = csv.writer(csvfile)

  # writing the fields
  csvwriter.writerow(columnNames)

  # writing the data rows
  csvwriter.writerows(rows)