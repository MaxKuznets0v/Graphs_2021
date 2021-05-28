from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True


def metrics(path1, path2):
    im1 = Image.open(path1)
    width1 = im1.size[0]
    height1 = im1.size[1]
    image1 = im1.load()

    im2 = Image.open(path2)
    width2 = im2.size[0]
    height2 = im2.size[1]
    image2 = im2.load()

    if width1 != width2 or height1 != height2:
        print("Different sizes")
        return

    common_pixels = 0
    obj_1 = 0
    obj_2 = 0
    common_pixels_obj = 0
    for i in range(width1):
        for j in range(height2):
            if type(image1[i, j]) is not int:
                int1 = image1[i, j][0] + image1[i, j][1] + image1[i, j][2]
            else:
                int1 = image1[i, j]
            if type(image2[i, j]) is not int:
                int2 = image2[i, j][0] + image2[i, j][1] + image2[i, j][2]
            else:
                int2 = image2[i, j]

            if int1 == int2:
                common_pixels += 1
                if int2 != 0:
                    common_pixels_obj += 1
            if int1 == 255:
                obj_1 += 1
            if int2 != 0:
                obj_2 += 1
    print("Accuracy:", common_pixels / (width1 * height1))
    print("Jaccard:", common_pixels_obj / (obj_1 + obj_2 - common_pixels_obj))
    print(common_pixels, obj_1, obj_2, common_pixels_obj)
    

metrics(r'C:\Users\Administrator\Documents\GitHub\Graphs_2021\results\banana1-gr-320.jpg', 
                  r'C:\Users\Administrator\Documents\GitHub\Graphs_2021\image-segments-320\banana1-320.jpg')