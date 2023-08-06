import identifyPeople
import cv2 as cv
from identifyPeople import crop_subjects_from_segmented_image as identify
from matplotlib import pyplot as plt
import os
import shutil
from random import randint


def make_set():
    unfound = 0

    print("Starting... ")

    new_set = 'bestOf/resources/identifiedFaces'
    directory = 'bestOf/resources/lfw'

    if os.path.isdir(new_set):
        shutil.rmtree(new_set)

    os.mkdir(new_set)

    for folder in os.listdir(directory):
        os.mkdir(new_set + '/' + folder + '_Identified')
        for img in os.listdir(os.path.join(directory, folder)):

            pik = cv.imread(os.path.join(directory, folder, img))
            image = cv.cvtColor(pik, cv.COLOR_BGR2RGB)

            faces, bounds = identify(image)
            if len(faces) == 0:
                unfound += 1

            for i, face in enumerate(faces):
                strings = img.split('.')
                name = ""
                if i > 0:
                    name = strings[0] + '_Identified' + \
                        str(i) + '.' + strings[1]
                else:
                    name = strings[0] + '_Identified' + '.' + strings[1]

                cv.imwrite(os.path.join(
                    new_set, folder + '_Identified', name), face)

    print('Number of failed identifications: ', str(unfound))


def crop_all_images():
    counter = 0
    counter_cropped = 0
    print('Starting to crop all images...')
    new_set = 'bestOf/resources/identifiedFacesCropped'
    directory = 'bestOf/resources/identifiedFaces'

    if os.path.isdir(new_set):
        shutil.rmtree(new_set)

    os.mkdir(new_set)

    for folder in os.listdir(directory):
        os.mkdir(new_set + '/' + folder + '_Cropped')
        print("Working on: " + folder)
        for i, img in enumerate(os.listdir(os.path.join(directory, folder))):
            counter += 1
            strings = img.split('.')
            name = strings[0] + str(i) + '.' + strings[1]

            image = cv.imread(os.path.join(directory, folder, img))
            rand_x = randint(20, 25)
            rand_y = randint(20, 25)
            cropped_list = crop_an_image(image, rand_x / 100, rand_y / 100)

            index = randint(0, 3)
            cv.imwrite(os.path.join(new_set, folder +
                                    '_Cropped', name), cropped_list[index])
            counter_cropped += 1

        print("----Finished----\n")

    print("---------------------Done With Everything---------------------")
    print("Out of " + str(counter) + " images\n" +
          str(counter_cropped) + " cropped images were created")


def crop_an_image(image, x, y):
    height = int(image.shape[0] * y)
    length = int(image.shape[1] * x)
    b_height = (image.shape[0] - height)
    b_length = (image.shape[1] - length)

    left_cutoff = image[:, length:]
    top_cutoff = image[height:, :]
    right_cutoff = image[:, :b_length]
    bottom_cutoff = image[:b_height, :]

    return [left_cutoff, top_cutoff, right_cutoff, bottom_cutoff]


# make_set()
if __name__ == '__main__':
    crop_all_images()
