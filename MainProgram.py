from tkinter import *
import io
from PIL import Image, ImageTk, ImageGrab
from functools import partial
from time import sleep
import GaganMock
import os 

# make a function here to set the obstacles array by extending the values of the bounded boxes (get all of them)
# we can do for-loops and maybe math?
# We will need to get this information from a csv, and will use that information to find the points 

''' Make the locations global variables so we can easily change with Gagan's values '''

# the 'goodness' of the cover nodes can be imported from Gagan's file
global_goodness = 50

# we will be fed in 44520x1920
# since this image size is too large, we will need to reduce its ratio in the GUI and zoom in 
# scale it down by a factor of 24 - this is simply changing the dimensions of the GUI, not the image.
# resize by a factor of 2.5 - so we can save as image
global_width = 4452
global_height = 192

# to keep track of the paths taken thus far
# TODO: implement this logic
global_paths_completed = 0

# offset is used to ensure we start the paths at the bottom of the pins and not top left 
offset = [19, 33]
# offset = [0, 0]
# 4452 and 192

# we place the images without offsets - don't really need to error check, but we will anyway
# global_start_1_image = [100, 100]
# global_start_2_image = [900, 100]
# global_start_3_image = [100, 600]
# global_end_image = [500, 500] 
# # we draw the paths with offsets
# global_start_1 = [global_start_1_image[0] + offset[0], global_start_1_image[1] + offset[1]] 
# global_start_2 = [global_start_2_image[0] + offset[0], global_start_2_image[1] + offset[1]] 
# global_start_3 = [global_start_3_image[0] + offset[0], global_start_3_image[1] + offset[1]]
# global_end = [global_end_image[0] + offset[0], global_end_image[1] + offset[1]] 

global_start_1_image = [0, 10]
global_start_2_image = [30, 12]
global_start_3_image = [200, 10]
global_end_image = [4000, 100] 
# we draw the paths with offsets
global_start_1 = [global_start_1_image[0] + offset[0], global_start_1_image[1] + offset[1]] 
global_start_2 = [global_start_2_image[0] + offset[0], global_start_2_image[1] + offset[1]] 
global_start_3 = [global_start_3_image[0] + offset[0], global_start_3_image[1] + offset[1]]
global_end = [global_end_image[0] + offset[0], global_end_image[1] + offset[1]] 

# list of lists for the covers and obstacles
global_covers = GaganMock.cover_list
global_obstacles = GaganMock.obstacles_list

# print(global_covers)
# print(global_obstacles)

# func for the window
def app_window(app, root, canvas, start_color, end_color, cover_color, obstacle_color, path_color, 
start1, start2, start3, end, covers, obstacles):

    geo = str(global_width) + 'x' + str(global_height)
    root.geometry(geo) # for the size of the GUI

    # create the icon [top left of the GUI]
    icon = PhotoImage(file = 'images/drone.png')
    root.iconphoto(False, icon)

    # place the starting squad node on the map image
    canvas.create_image((start1), image=start_color, anchor=NW)
    canvas.create_image((start2), image=start_color, anchor=NW)
    canvas.create_image((start3), image=start_color, anchor=NW)

    # place the end node node on the map
    canvas.create_image((end), image=end_color, anchor=NW)

    # position for the cover nodes 
    for cover in covers:
        canvas.create_image((cover), image=cover_color, anchor=NW)

    # place magenta over the obstacle nodes
    for obstacle in obstacles: 
        canvas.create_image((obstacle), image=obstacle_color, anchor=NW)
    
class App:
    def __init__(self, root, canvas, start_color, end_color, cover_color, obstacle_color, path_color):
        
        root.wm_title("404 Project - Fifth Run")
        
        # check global variables before assigning, and change the values if necessary
        # check that the points are valid before continuing
        # this will output a statement with more information on what to do if your input is out of bounds
        self.check_valid_point(global_start_1, 0, 'start1')
        self.check_valid_point(global_start_2, 0, 'start2')
        self.check_valid_point(global_start_3, 0, 'start3')
        self.check_valid_point(global_end, 0, 'end')
        # self.check_valid_point(global_start_1_image, 0, 'start1')
        # self.check_valid_point(global_start_2_image, 0, 'start2')
        # self.check_valid_point(global_start_3_image, 0, 'start3')
        # self.check_valid_point(global_end_image, 0, 'end')
        for index, obstacle in enumerate(global_obstacles):
            self.check_valid_point(obstacle, index, 'obstacle')
        for index, cover in enumerate(global_covers):
            self.check_valid_point(cover, index, 'cover')

        # print('a', global_obstacles)
        # print('a', global_covers)

        self.root = root
        self.canvas = canvas
        self.start_color = start_color
        self.end_color = end_color
        self.cover_color = cover_color
        self.obstacle_color = obstacle_color
        self.path_color = path_color
        self.start1 = global_start_1        
        self.start2 = global_start_2     
        self.start3 = global_start_3

        self.end = global_end         

        self.obstacles = global_obstacles
        self.covers = global_covers

        # create the pop-up window
        root.update_idletasks()
        app_window(self, root, canvas, start_color, end_color, cover_color, obstacle_color, path_color, 
        global_start_1_image, global_start_2_image, global_start_3_image, global_end_image, global_covers, global_obstacles)

    # error checking - check that all points are within the - may clean this up later if we have time
    # the x parameter needs to be within 0 and global_width - 1, inclusive
    # the y parameter needs to be within 0 and global_height - 1, inclusive 
    # if the point is under or over the parameters, we place it on the border
    def check_valid_point(self, point, index, name):
        difference = 2
        x = point[0]
        y = point[1]
        
        if name == 'cover':
            if x < 0:
                global_covers[index][0] = difference
            if y < 0:
                global_covers[index][1] = difference
            if global_width <= x:
                global_covers[index][0] = global_width - difference
            if global_height <= y:
                global_covers[index][1] = global_height - difference

        if name == 'obstacle':
            if x < 0:
                global_obstacles[index][0] = difference
            if y < 0:
                global_obstacles[index][1] = difference
            if global_width <= x:
                global_obstacles[index][0] = global_width - difference
            if global_height <= y:
                global_obstacles[index][1] = global_height - difference

        if name == 'start1':
            if x < 0:
                global_start_1[0] = difference
            if y < 0:
                global_start_1[1] = difference
            if global_width <= x:
                global_start_1[0] = global_width - difference
            if global_height <= y:
                global_start_1[1] = global_height - difference
        
        if name == 'start2':
            if x < 0:
                global_start_2[0] = difference
            if y < 0:
                global_start_2[1] = difference
            if global_width <= x:
                global_start_2[0] = global_width - difference
            if global_height <= y:
                global_start_2[1] = global_height - difference

        if name == 'start3':
            if x < 0:
                global_start_3[0] = difference
            if y < 0:
                global_start_3[1] = difference
            if global_width <= x:
                global_start_3[0] = global_width - difference
            if global_height <= y:
                global_start_3[1] = global_height - difference
        
        if name == 'end':
            if x < 0:
                global_end[0] = difference
            if y < 0:
                global_end[1] = difference
            if global_width <= x:
                global_end[0] = global_width - difference
            if global_height <= y:
                global_end[1] = global_height - difference

    def heuristic(self, node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1]-node2[1])

    # function to abstract checking the neighbors so we have less code
    def check_neighboring_nodes(self, main_node):
        # can do something like
        for obstacle in global_obstacles:
            if 0 <= main_node[1] < global_width and main_node != obstacle:
                return True
        return False

    # function to find the neighbors -
    def find_neighbors(self, current):
        # create an empty list for the neighbors
        neighbors = []

        right_neighbor = current[:] 
        right_neighbor[1] = current[1] + 1 
        if self.check_neighboring_nodes(right_neighbor):
            neighbors.append(right_neighbor)
            neighbors.append(right_neighbor)

        left_neighbor = current[:]
        left_neighbor[1] = current[1] - 1
        if self.check_neighboring_nodes(left_neighbor):
            neighbors.append(left_neighbor)

        up_neighbor = current[:]
        up_neighbor[0] = current[0] + 1
        if self.check_neighboring_nodes(up_neighbor):
            neighbors.append(up_neighbor)

        down_neighbor = current[:]
        down_neighbor[0] = current[0] - 1
        if self.check_neighboring_nodes(down_neighbor):
            neighbors.append(down_neighbor)

        down_right_neighbor = current[:]
        down_right_neighbor[0] = current[0] + 1
        down_right_neighbor[1] = current[1] + 1
        if self.check_neighboring_nodes(down_right_neighbor):
            neighbors.append(down_right_neighbor)

        up_right_neighbor = current[:]
        up_right_neighbor[0] = current[0] - 1
        up_right_neighbor[1] = current[1] + 1
        if self.check_neighboring_nodes(up_right_neighbor):
            neighbors.append(up_right_neighbor)

        up_left_neighbor = current[:]
        up_left_neighbor[0] = current[0] - 1
        up_left_neighbor[1] = current[1] - 1
        if self.check_neighboring_nodes(up_left_neighbor):
            neighbors.append(up_left_neighbor)

        down_left_neighbor = current[:]
        down_left_neighbor[0] = current[0] + 1
        down_left_neighbor[1] = current[1] - 1
        if self.check_neighboring_nodes(down_left_neighbor):
            neighbors.append(down_left_neighbor)
        return neighbors

    # to sort the set
    def sort_open_set(self, open_set, f_score):
        # The index of the list is the same as the index in the open set
        # and the value of the index is the f_score of it
        index_to_fscore = []
        for node in open_set:
            f_score_of_node = f_score[node[0]][node[1]]
            index_to_fscore.append(f_score_of_node)

        sorted_copy = index_to_fscore.copy()
        sorted_copy.sort()
        sorted_open_set = []

        for value in sorted_copy:
            min_ = index_to_fscore.index(value)
            sorted_open_set.append(open_set[min_])
            # We mark that we have transferred this value to the sorted array
            index_to_fscore[min_] = float('inf')

        return sorted_open_set

    # implement the actual algorithm
    def a_star_algorithm(self, canvas, start, end):
        # create an open set for the start nodes
        open_set = [start] 
        g_score = [] # cost so far to reach the node
        f_score = [] # total estimated cost of path through node  
        came_from = []

        # Initializations of f_score, g_score and came_from - make these lists full of infinitely large numbers 
        for i in range(global_width):
            f_score.append([])
            g_score.append([])
            came_from.append([])
            for j in range(global_height):
                infinity = float('inf')
                came_from[i].append([])
                g_score[i].append(infinity)  # set it to infinity
                f_score[i].append(infinity)  # set it to infinity

        # the starting cost (g_score) is 0, the f score is the expected cost [from the current node to the end - using the heuristic]
        g_score[start[0]][start[1]] = 0
        f_score[start[0]][start[1]] = self.heuristic(start, end)

        while len(open_set) > 0:
            self.root.update_idletasks() # Enter event loop until all idle tasks have been completed - this is used to display each path when it is completed - safer than update()
            sleep(0.02)

            # sort the open set
            open_set = self.sort_open_set(open_set, f_score)
            current = open_set[0]
            current_row = current[0]
            current_column = current[1]

            # once we have reached the end, construct the best path
            if current == end:
                return self.reconstruct_path(canvas, came_from, current)

            # find the neighbors of the current node
            open_set.remove(current)
            neighbors = self.find_neighbors(current)

            for node in neighbors:
                node_row = node[0]
                node_column = node[1]

                # when we check the neighbor, we can't make the points one less than the corner, because then the neighbor would be oob, so we need to make it 2 less
                # print('nr', node_row)
                # print('nc', node_column)
                # print()

                # node is a list of [x,y], with the values inside being ints, so is cover. We can compare the values inside to see if going to that cover makes sense or not- cover is of 50 pts less

                # The weight of every edge is 1
                tentative_gScore = g_score[current_row][current_column] + 1

                # if the tentative g score (ie g score plus 1) is less than the current g score of the node
                # then we append the current nodes row and colum to the came_from list
                # then, update the g score to the new, lower score
                # and update the f score to be the g score plus the heuristic (h(n))
                if tentative_gScore < g_score[node_row][node_column]:
                    came_from[node_row][node_column].append(current_row)
                    came_from[node_row][node_column].append(current_column)
                    g_score[node_row][node_column] = tentative_gScore
                    f_score[node_row][node_column] = g_score[node_row][node_column] + self.heuristic(node, end) # changed end from self.end
                    if node not in open_set:
                        open_set.append(node[:])

    def cover_logic(self, path, start, cover_number, goodness):
        #TODO: import the 'goodness' of cover from Gagan
        if path == self.heuristic(start, cover_number) and cover_number[0] < max(self.end[0], start[0]) + goodness and \
            cover_number[0] > min(self.end[0], start[0]) - goodness and \
            cover_number[1] < max(self.end[1], start[1]) + goodness and \
            cover_number[1] > min(self.end[1], start[1]) - goodness:
            return True
        return False

    def connect_cover(self, start, cover):
        self.a_star_algorithm(self.canvas, start, cover) 
        self.a_star_algorithm(self.canvas, cover, self.end) 

    def find_cover_to_take(self, path, start):
        # iterate through the cover nodes and check all of them, as soon as we find one, break out of the loop 
        # once we have all three paths, we can close out
        cover_taken = False
        for cover in global_covers:  
            # this is checking all cover nodes, and will take a path if it is convenient to do so
            if self.cover_logic(path, start, cover, global_goodness):
                cover_taken = True
                self.connect_cover(start, cover) 
        if not cover_taken:
            self.connect_cover(start, global_end_image)


    # find the paths needed - ADD COVER LOGIC HERE
    def find_path(self, event):        
        # compare the distances for all five cover nodes from the starting nodes
        path1 = min(self.heuristic(self.start1, cover) for cover in global_covers)
        path2 = min(self.heuristic(self.start2, cover) for cover in global_covers)
        path3 = min(self.heuristic(self.start3, cover) for cover in global_covers)

        self.find_cover_to_take(path1, self.start1)
        self.find_cover_to_take(path2, self.start2)
        self.find_cover_to_take(path3, self.start3)
        
    # function to make the path
    def reconstruct_path(self, canvas, came_from, current):
        total_path = []
        while current: # reconstruct the three paths
            canvas.create_image((current), image=self.path_color, anchor=NW) # getting an out of range error in this line
            total_path.append(current[:])
            current = came_from[current[0]][current[1]]
        # save the image after every path has been reconstructed
        # cannot save on images more than 20000 pixels wide, so we can reduce the image some
        self.save(self.canvas, self.root)
        print("Path found!")

    def save(self, canvas, root):
        canvas.update()
        canvas.postscript(file="images/output.ps", colormode='color')
        self.save_image()

    def save_image(self):
        TARGET_BOUNDS = (global_width, global_height)

        pic = Image.open('images/output.ps')
        pic.load(scale=10)

        if pic.mode in ('P', '1'):
            pic = pic.convert("RGB")

        ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                    TARGET_BOUNDS[1] / pic.size[1])
        new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

        pic = pic.resize(new_size, Image.ANTIALIAS)

        pic.save("images/final.png")

def main():

    # create the root
    root = Tk()
    Image.MAX_IMAGE_PIXELS = None   

    # convert the image to greyscale - take in the input and save as grayscale
    bg_gray = Image.open('images/img_ken.jpeg').convert('L')
    bg_gray.save('images/greyscale_bg.png')

    # for the background image - needed to pass it globally
    bg = PhotoImage(file = 'images/greyscale_bg.png') # to add the background image

    canvas = Canvas(width = global_width, height = global_height)
    canvas.pack(fill = 'both', expand = True)
    canvas.create_image(0,0,image = bg, anchor = 'nw')

    # --- load the colors (as png images of 1x1 pixel)  --- #
    # load the color used for the starting squads [green]
    start_color = PhotoImage(file = 'images/good_start.png')
    # load the color used for the end node [red]
    end_color = PhotoImage(file = 'images/good_end.png')
    # load the color used for the cover node [green]
    cover_color = PhotoImage(file = 'images/cover.png')
    # load the color used for the obstacle node [magenta]
    obstacle_color = PhotoImage(file = 'images/obstacle.png')
    # load the color used for the path node [turquoise]
    path_color = PhotoImage(file = 'images/start.png')

    # pass the images to the app class - create the GUI
    app = App(root, canvas, start_color, end_color, cover_color, obstacle_color, path_color)

    # start the algorithm when 'enter' is pressed
    root.bind('<Return>', app.find_path)

    # start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()