import csv

with open('Obstacles.csv', 'r', encoding='utf-8-sig') as obstacle_csv: # open the object
  csv_reader_obstacles = csv.reader(obstacle_csv) 
  obstacles = list(csv_reader_obstacles) # save the rows as lists in the list of lists

with open('Covers.csv', 'r', encoding='utf-8-sig') as cover_csv: # open the object
  csv_reader_cover = csv.reader(cover_csv) 
  covers = list(csv_reader_cover) # save the rows as lists in the list of lists

# create a list to hold all the points we will use as obstacles
obstacles_list = []
cover_list = []

# iterate through each row and save the obstacles
for x, y, width, height in obstacles:
    # for each point, we want to create a block and extend it in the obstacles array
    for i in range(int(x), int(x) + int(width) + 1):
        for j in range(int(y), int(y) + int(height) + 1):
            obstacles_list.append([i, j])

# iterate through each row and save the covers
for x, y, width, height in covers:
    # for each point, we want to create a block and extend it in the obstacles array
    for i in range(int(x), int(x) + int(width) + 1):
        for j in range(int(y), int(y) + int(height) + 1):
            cover_list.append([i, j])