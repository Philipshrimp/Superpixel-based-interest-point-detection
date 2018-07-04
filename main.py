import slic
import getPosition
import localpatch
import brief
import time

import os
import cv2

the_number_of_sequences = 2

for num in range(the_number_of_sequences):
    print("Frame number : " + str(num))

    # Change the file name first!!
    '''
    input_index = "%03d" % num
    img_path = "input/test_" + input_index + ".jpg"
    '''
    img_path = "input/" + str(num) + ".png"

    if not os.path.exists("output/"):
        os.makedirs("output/")

    start_time = time.time()

    superpixel_segmentation, superpixel_centers = slic.slic_superpixel(img_path)

    list_center_position = getPosition.get_center_position(superpixel_centers)
    list_center_position, nearest_neighbor = getPosition.find_nearest_neighbors(superpixel_segmentation, list_center_position)
    list_intermediate_position = getPosition.find_intermediate_positions(img_path, list_center_position, nearest_neighbor)

    # Show the result of intermediate point selection (x, y)
    length = len(list_intermediate_position)
    feature_result = cv2.imread(img_path)

    for i in range(length):
        cv2.circle(feature_result, (list_intermediate_position[i][0], list_intermediate_position[i][1]), 1, (0, 255, 255), -1)

    feature_visualization_string = "output/features/" + str(num) + ".png"
    cv2.imwrite(feature_visualization_string, feature_result)

    localpatch.get_local_patch(img_path, list_intermediate_position)
    descriptor = brief.BRIEF_descriptor(img_path, list_intermediate_position)

    print("Running time: ", (time.time() - start_time), " seconds")

    # Save descriptors as the txt file
    print("Saving descriptors...")

    descriptor_file_string = "output/descriptor/" + str(num) + ".txt"
    descriptor_file = open(descriptor_file_string, 'w')

    for i in range(descriptor.shape[0]):
        for j in range(descriptor.shape[1]):
            if(descriptor[i][j] == True):
                descriptor_file.write('1')
            else:
                descriptor_file.write('0')
        descriptor_file.write("\n")
    descriptor_file.close()

    # Below code is for the matching test
    #if num != 0:
    #    plot_brief.matching_features(prev_img_path, img_path, prev_features, list_intermediate_position, prev_descriptor, descriptor)

    # Change the previous descriptor to the current ones
    prev_img_path = img_path
    prev_features = list_intermediate_position
    prev_descriptor = descriptor

print("Done!")