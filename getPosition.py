import math
import cv2

def get_center_position(superpixel_centers):
    list_center_position = []

    print("Finding the position of centers...")

    for i in range(superpixel_centers.shape[0]):
        for j in range(superpixel_centers.shape[1]):
            if superpixel_centers[i][j] != 0:
                list_center_position.append((j,i))

    # Test whether center positions are copied correctly
    '''
    max_index = int(len(list_center_position))

    test_image = numpy.zeros((superpixel_centers.shape[0], superpixel_centers.shape[1], 1), numpy.uint8)
    list_index = 0

    for i in range(superpixel_centers.shape[0]):
        for j in range(superpixel_centers.shape[1]):
            if (list_index >= max_index):
                break

            if (i == list_center_position[list_index][0] and j == list_center_position[list_index][1]):
                test_image[i][j] = 255
                list_index += 1

    cv2.imwrite("test.png", test_image)
    '''

    return list_center_position


def find_center_position(center_superpixel_val, superpixel_value):
    for k in range(len(center_superpixel_val)):
        if(superpixel_value == center_superpixel_val[k][2]):
            return k

    return -1


def find_nearest_neighbors(superpixel_segmentation, list_center_position):
    print("Finding nearest neighbors...")

    # Save superpixel values and its corresponding positions
    center_superpixel_val = []

    for k in range(len(list_center_position)):
        position_x = list_center_position[k][0]
        position_y = list_center_position[k][1]
        center_superpixel_val.append((position_x, position_y, superpixel_segmentation[position_y][position_x]))

    # Remove duplicated center values
    temp_saved_val = []
    is_duplicated = False
    loop = 0

    while loop < len(center_superpixel_val):
        if (is_duplicated):
            is_duplicated = False

        if(loop >= len(center_superpixel_val)):
            break
        if(loop == 0):
            is_duplicated = False
            temp_saved_val.append(center_superpixel_val[loop][2])
        else:
            for temp in range(len(temp_saved_val)):
                if ((temp + 1) == len(temp_saved_val)):
                    temp_saved_val.append(center_superpixel_val[loop][2])
                elif(temp_saved_val[temp] == center_superpixel_val[loop][2]):
                    center_superpixel_val.remove(center_superpixel_val[loop])
                    is_duplicated = True
                    break

        if(is_duplicated == False):
            loop += 1

    # Reset the list of center positions
    list_center_position = []

    for k in range(len(center_superpixel_val)):
        list_center_position.append([center_superpixel_val[k][0], center_superpixel_val[k][1]])

    # Find the nearest neighbor
    nearest_neighbor = []
    nearest_position = -1

    for i in range(len(list_center_position)):
        distance = []

        for j in range(len(list_center_position)):
            if(i==j):
                continue
            else:
                dist_val = math.pow((list_center_position[i][0] - list_center_position[j][0]), 2) + math.pow((list_center_position[i][1] - list_center_position[j][1]), 2)
                distance.append(dist_val)

        minimum_distance = min(distance)

        for j in range(len(distance)):
            if(distance[j] == minimum_distance and i != j):
                nearest_position = j
                break

        if(nearest_position == -1):
            print("Finding the nearest neighbor : Error!!")

        nearest_neighbor.append([list_center_position[nearest_position][0], list_center_position[nearest_position][1]])

    return list_center_position, nearest_neighbor

def find_intermediate_positions(img_path, list_center_position, nearest_neighbor):
    print("Finding intermediate points...")

    # Load color image
    input_image = cv2.imread(img_path)

    # Find the intermediate position
    list_intermediate_position = []

    for k in range(len(list_center_position)):
        center_x = list_center_position[k][0]
        center_y = list_center_position[k][1]
        neighbor_x = nearest_neighbor[k][0]
        neighbor_y = nearest_neighbor[k][1]

        intermediate_x = int((center_x + neighbor_x) / 2)
        intermediate_y = int((center_y + neighbor_y) / 2)

        list_intermediate_position.append([intermediate_x, intermediate_y])

        # If the color threshold is needed, use below code!
        '''
        diff_b = abs(input_image[center_y][center_x][0] - input_image[neighbor_y][neighbor_x][0])
        diff_g = abs(input_image[center_y][center_x][1] - input_image[neighbor_y][neighbor_x][1])
        diff_r = abs(input_image[center_y][center_x][2] - input_image[neighbor_y][neighbor_x][2])
        diff_sum = diff_b + diff_g + diff_r

        if (diff_sum > 0):
            intermediate_x = int((center_x + neighbor_x) / 2)
            intermediate_y = int((center_y + neighbor_y) / 2)

            list_intermediate_position.append([intermediate_x, intermediate_y])
        '''

    return list_intermediate_position