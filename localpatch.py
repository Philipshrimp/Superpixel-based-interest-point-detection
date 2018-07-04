import cv2
import os

def get_local_patch(img_path, list_intermediate_points):
    print("Making local patches...")

    # Load image
    input_image = cv2.imread(img_path)
    size_input_y = input_image.shape[0]
    size_input_x = input_image.shape[1]

    # Extract the index of input image
    split_input_path = img_path.split("/", 1)
    cropped_input = split_input_path[1].split(".", 1)

    local_patch_directory = "output/patch" + cropped_input[0] + "/"
    if not os.path.exists(local_patch_directory):
        os.makedirs(local_patch_directory)

    index = 0

    for k in range(len(list_intermediate_points)):
        x = list_intermediate_points[k][0]
        y = list_intermediate_points[k][1]

        if(x < 32 or y < 32 or x > (size_input_x-32) or y > (size_input_y-32)):
            continue
        else:
            local_patch = input_image[(y-32):(y+32), (x-32):(x+32)]
            index_str = "%04d" % index
            local_patch_filename = local_patch_directory + "patch_" + index_str + ".png"
            cv2.imwrite(local_patch_filename, local_patch)
            index += 1