from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io

import cv2
from PIL import Image
from PIL import ImageDraw


def slic_superpixel(img_path):
    # Load image and set the number of segments
    print("Loading an image...")
    image = img_as_float(io.imread(img_path))
    numSegments = 500

    # SLIC segmentation
    print("Making SLIC superpixels...")
    # segments = slic(image, n_segments=numSegments, sigma=5)
    segments = slic(image, sigma=5)

    # Show the result of segmentation
    '''
    fig = plt.figure("Superpixels -- %d segments" % (numSegments))
    ax = fig.add_subplot(1,1,1)

    ax.imshow(mark_boundaries(image, segments))
    plt.axis("off")
    plt.show()
    '''

    # Upscale the value of superpixel (If necessary)
    '''
    for i in range(segments.shape[0]):
        for j in range(segments.shape[1]):
            segments[i][j] = segments[i][j] * 2
    '''

    # Save and load the boundaries
    superpixel_boundaries = Image.new('RGB', (image.shape[1], image.shape[0]))
    padding_draw = ImageDraw.Draw(superpixel_boundaries)
    padding_draw.line((0,0) + (image.shape[1]-1, 0), fill=255)
    padding_draw.line((0,0) + (0, image.shape[0]-1), fill=255)
    padding_draw.line((image.shape[1]-1, 0) + (image.shape[1]-1, image.shape[0]-1), fill=255)
    padding_draw.line((0, image.shape[0]-1) + (image.shape[1]-1, image.shape[0]-1), fill=255)
    del padding_draw

    superpixel_boundaries = mark_boundaries(superpixel_boundaries, segments)
    blank_image = Image.new('RGB', (image.shape[1], image.shape[0]))
    io.imsave("output/boundaries.png", superpixel_boundaries)
    io.imsave("output/centers.png", blank_image)
    cv2.imwrite("output/segments.png", segments)

    superpixel_segmented = cv2.imread("output/boundaries.png", cv2.CV_8UC1)
    superpixel_centers = cv2.imread("output/centers.png", cv2.CV_8UC1)

    # Find contours
    print("Finding superpixel centers...")
    contour_image, superpixel_contours, hierarchy = cv2.findContours(superpixel_segmented, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, superpixel_contours, -1, (0, 255, 0), 1)

    for contour in superpixel_contours:
        # Compute the center
        superpixel_moments = cv2.moments(contour)
        contour_X = int(superpixel_moments["m10"] / superpixel_moments["m00"])
        contour_Y = int(superpixel_moments["m01"] / superpixel_moments["m00"])

        # Draw and show
        cv2.circle(image, (contour_X, contour_Y), 2, (0, 255, 255), -1)
        cv2.circle(superpixel_segmented, (contour_X, contour_Y), 0, 255, -1)
        cv2.circle(superpixel_centers, (contour_X, contour_Y), 0, 255, -1)

    cv2.imwrite("output/boundary_with_center.png", superpixel_segmented)
    cv2.imwrite("output/centers.png", superpixel_centers)
    cv2.imwrite("output/segmentation_result.png", image)

    return segments, superpixel_centers